import chromadb
from chromadb.utils import embedding_functions
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import CHROMA_PATH, EMBEDDING_MODEL
from database.db import get_candidate_ticket_ids, get_full_ticket_text
from retrieval.query_parser import parse_query_constraints

# Suppress Chroma telemetry warnings
os.environ["CHROMA_TELEMETRY_ANONYMIZED"] = "False"
os.environ["ANONYMIZED_TELEMETRY"] = "False"

def retrieve_context(query: str, top_k: int = 3, distance_threshold: float = 1.0) -> list[dict]:
    print(f"\n[1] Parsing query: '{query}'")
    constraints = parse_query_constraints(query)
    print(f"    Extracted constraints: {constraints}")
    
    print("[2] Running SQL Filter...")
    candidate_ids = get_candidate_ticket_ids(category=constraints.get('category'))
    
    if not candidate_ids:
        print("    ❌ No tickets matched the SQL constraints. Stopping here.")
        return []
        
    print(f"    SQL found {len(candidate_ids)} candidate(s): {candidate_ids}")
    
    print("[3] Running Vector Search (ChromaDB)...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    collection = chroma_client.get_collection(name="ticket_resolutions", embedding_function=transformer_ef)
    
    # Format metadata filter for ChromaDB
    if len(candidate_ids) == 1:
        where_clause = {"ticket_id": candidate_ids[0]}
    else:
        where_clause = {"ticket_id": {"$in": candidate_ids}}
    
    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, len(candidate_ids)),
        where=where_clause,
        include=["metadatas", "distances"]
    )
    
    if not results['ids'][0]:
         print("    ❌ No semantic matches found.")
         return []
         
    ticket_ids_to_fetch = []
    for i in range(len(results['ids'][0])):
        t_id = results['metadatas'][0][i]['ticket_id']
        dist = results['distances'][0][i]  # Lower distance = higher similarity
        
        if dist <= distance_threshold:
            ticket_ids_to_fetch.append(t_id)
        else:
            print(f"    Ignoring Ticket {t_id} (Distance {dist:.2f} > Threshold {distance_threshold})")
    
    if not ticket_ids_to_fetch:
        print("    ❌ No sufficiently similar tickets found.")
        return []
        
    print("[4] Assembling Final Context...")
    full_texts = get_full_ticket_text(ticket_ids_to_fetch)
    
    final_context = []
    for t_id in ticket_ids_to_fetch:
        final_context.append({
            "ticket_id": t_id,
            "description": full_texts[t_id]['description'],
            "resolution": full_texts[t_id]['resolution']
        })
        print(f"    ✅ Retrieved Ticket {t_id} for LLM Context")
        
    return final_context

if __name__ == "__main__":
    # Test 1: Should extract 'login', run SQL, and find Ticket 1042
    retrieve_context("How did we fix the mobile app login timeout?")
    
    # Test 2: Should extract 'hardware', run SQL, find 0 candidates, and STOP immediately
    retrieve_context("What hardware issues did we have?")