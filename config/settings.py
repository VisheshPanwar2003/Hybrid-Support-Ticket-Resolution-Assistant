import os

# Project Root Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database & Vector Store Paths
DB_PATH = os.path.join(BASE_DIR, "database", "tickets.db")
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

# Models
EMBEDDING_MODEL = "all-MiniLM-L6-v2"