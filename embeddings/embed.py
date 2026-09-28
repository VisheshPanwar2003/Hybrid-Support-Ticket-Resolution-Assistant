import sqlite3
import chromadb
from chromadb.utils import embedding_functions
import sys
import os

# Ensure Python can find our custom modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DB_PATH, CHROMA_PATH, EMBEDDING_MODEL
from embeddings.chunk import create_whole_ticket_chunk

def embed_and_store():
    # 1. Fetch text and metadata from SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = """
        SELECT t.ticket_id, t.category, tt.description, tt.resolution 
        FROM tickets t
        JOIN ticket_text tt ON t.ticket_id = tt.ticket_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("No tickets found in the database.")
        return
        
    documents = []
    metadatas = []
    ids = []
    
    # 2. Process and chunk the text
    for row in rows:
        ticket_id, category, desc, res = row
        chunk = create_whole_ticket_chunk(desc, res)
        
        if chunk:
            documents.append(chunk)
            # Store ticket_id and category as metadata for pre-filtering
            metadatas.append({"ticket_id": ticket_id, "category": category})
            ids.append(str(ticket_id))
    
    print(f"Generating embeddings for {len(documents)} tickets...")
    
    # 3. Initialize ChromaDB and the HuggingFace Embedding Model
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    
    # Create vector collection, explicitly enforcing Cosine Similarity
    collection = chroma_client.get_or_create_collection(
        name="ticket_resolutions",
        embedding_function=transformer_ef,
        metadata={"hnsw:space": "cosine"} 
    )
    
    # 4. Upsert vectors to the database
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"✅ Successfully embedded and stored {len(documents)} tickets in ChromaDB.")

if __name__ == "__main__":
    embed_and_store()