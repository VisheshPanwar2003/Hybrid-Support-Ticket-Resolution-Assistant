import sqlite3
import pandas as pd
import os
import sys

# Ensure Python can find the clean module when running from the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ingestion.clean import clean_tickets

def init_db(db_path: str, schema_path: str) -> sqlite3.Connection:
    """Initializes the SQLite database using the schema file."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    return conn

def load_tickets_to_sql(df: pd.DataFrame, conn: sqlite3.Connection):
    """Splits the dataframe and loads it into the normalized SQL tables."""
    tickets_df = df[['ticket_id', 'category', 'priority', 'status', 'created_date', 'resolved_date']]
    ticket_text_df = df[['ticket_id', 'description', 'resolution']]

    tickets_df.to_sql('tickets', conn, if_exists='append', index=False)
    ticket_text_df.to_sql('ticket_text', conn, if_exists='append', index=False)
    
    print(f"✅ Successfully cleaned and loaded {len(df)} tickets into SQLite.")
    conn.close()

if __name__ == "__main__":
    DB_PATH = "database/tickets.db"
    SCHEMA_PATH = "database/schema.sql"
    CSV_PATH = "data/raw_tickets.csv"

    print("Starting Phase 1: Data Ingestion...")
    cleaned_df = clean_tickets(CSV_PATH)
    connection = init_db(DB_PATH, SCHEMA_PATH)
    load_tickets_to_sql(cleaned_df, connection)