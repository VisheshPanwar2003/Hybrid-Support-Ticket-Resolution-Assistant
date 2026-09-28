import sys
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import EMBEDDING_MODEL

def calculate_similarity():
    print(f"Loading embedding model: {EMBEDDING_MODEL}...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    query = "How did we fix the mobile app login timeout?"
    
    # Target chunk (Ticket 1042)
    chunk_1 = "Description: User reports repeated timeout errors when logging in via the mobile app after the 2.3.1 update. Resolution: Root cause was an expired session token not being refreshed on app resume. Fixed by adding token refresh check on app-foreground event."
    
    # Unrelated chunk (Ticket 1044)
    chunk_2 = "Description: Dark mode text is unreadable on the settings page. Resolution: Updated CSS contrast ratio for settings-dark-mode class to meet accessibility standards."
    
    print("\nGenerating mathematical vectors (384 dimensions)...")
    vec_query = model.encode(query)
    vec_chunk_1 = model.encode(chunk_1)
    vec_chunk_2 = model.encode(chunk_2)
    
    # Calculate Cosine Distance (0.0 is a perfect match, 1.0 is completely unrelated)
    # Cosine Similarity = 1 - Cosine Distance
    dist_1 = cosine(vec_query, vec_chunk_1)
    dist_2 = cosine(vec_query, vec_chunk_2)
    
    print("\n===========================================")
    print(" 🧮 VECTOR SIMILARITY ANALYSIS")
    print("===========================================")
    print(f"Query: '{query}'\n")
    
    print(f"Target: Ticket 1042 (Login Timeout)")
    print(f"Cosine Distance: {dist_1:.4f} (Similarity: {(1 - dist_1) * 100:.1f}%)")
    
    print(f"\nTarget: Ticket 1044 (UI Dark Mode)")
    print(f"Cosine Distance: {dist_2:.4f} (Similarity: {(1 - dist_2) * 100:.1f}%)")
    print("===========================================")
    
    if dist_1 < dist_2:
        print("\n✅ Math confirms: Ticket 1042 is significantly closer to the query in vector space.")

if __name__ == "__main__":
    calculate_similarity()