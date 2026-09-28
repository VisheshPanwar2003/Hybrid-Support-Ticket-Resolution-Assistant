import sys
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import EMBEDDING_MODEL

def compare_chunking():
    print(f"Loading embedding model: {EMBEDDING_MODEL}...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    query = "How did we fix the mobile app login timeout?"
    
    # Strategy 1: Whole-Ticket Chunking (Our architecture)
    whole_ticket = "Description: User reports repeated timeout errors when logging in via the mobile app after the 2.3.1 update. Resolution: Root cause was an expired session token not being refreshed on app resume. Fixed by adding token refresh check on app-foreground event."
    
    # Strategy 2: Split Chunking (Description and Resolution separated)
    chunk_desc_only = "Description: User reports repeated timeout errors when logging in via the mobile app after the 2.3.1 update."
    chunk_res_only = "Resolution: Root cause was an expired session token not being refreshed on app resume. Fixed by adding token refresh check on app-foreground event."
    
    print("\nEncoding vectors...")
    vec_query = model.encode(query)
    vec_whole = model.encode(whole_ticket)
    vec_desc = model.encode(chunk_desc_only)
    vec_res = model.encode(chunk_res_only)
    
    sim_whole = (1 - cosine(vec_query, vec_whole)) * 100
    sim_desc = (1 - cosine(vec_query, vec_desc)) * 100
    sim_res = (1 - cosine(vec_query, vec_res)) * 100
    
    print("\n===========================================")
    print(" 🧩 CHUNKING STRATEGY COMPARISON")
    print("===========================================")
    print(f"Query: '{query}'\n")
    
    print(f"Strategy 1: Whole-Ticket Chunk (Context preserved)")
    print(f"Similarity: {sim_whole:.1f}%\n")
    
    print(f"Strategy 2A: Description Chunk Only (Context lost)")
    print(f"Similarity: {sim_desc:.1f}%\n")
    
    print(f"Strategy 2B: Resolution Chunk Only (Context lost)")
    print(f"Similarity: {sim_res:.1f}%")
    print("===========================================")
    
    print("\n💡 Takeaway: If you split the ticket, ChromaDB might retrieve the 'Description' chunk which has high similarity but no answer, or completely miss the 'Resolution' chunk because it lacks the 'login timeout' keywords.")

if __name__ == "__main__":
    compare_chunking()