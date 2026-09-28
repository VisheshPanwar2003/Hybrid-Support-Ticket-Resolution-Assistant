import sys
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import EMBEDDING_MODEL

def run_experiment():
    print(f"Loading embedding model: {EMBEDDING_MODEL}...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    # The target ticket chunk (Ticket 1042)
    target_chunk = "Description: User reports repeated timeout errors when logging in via the mobile app after the 2.3.1 update. Resolution: Root cause was an expired session token not being refreshed on app resume. Fixed by adding token refresh check on app-foreground event."

    # Different ways a user might ask for the same ticket
    queries = {
        "Exact Keywords": "How did we fix the mobile app login timeout?",
        "Semantic Match (Different Words)": "Users can't sign in on their phones, the session expires.",
        "Vague Symptom": "The authentication keeps failing after the new update.",
        "Completely Unrelated": "The office printer is jammed and needs ink."
    }

    print("Encoding target chunk and queries...")
    vec_target = model.encode(target_chunk)

    print("\n===========================================")
    print(" 🧪 EMBEDDING WORDING EXPERIMENT")
    print("===========================================")
    print(f"Target Ticket: {target_chunk[:75]}...\n")

    for label, query in queries.items():
        vec_query = model.encode(query)
        sim = (1 - cosine(vec_target, vec_query)) * 100
        print(f"[{label}]")
        print(f"Query: '{query}'")
        print(f"Similarity: {sim:.1f}%\n")

    print("===========================================")
    print("💡 Takeaway: Vector embeddings understand meaning, not just keywords.")
    print("Even when using different words ('sign in' vs 'login', 'phones' vs 'mobile'),")
    print("the embedding model successfully groups the related concepts together.")

if __name__ == "__main__":
    run_experiment()