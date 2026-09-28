import sqlite3
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DB_PATH

def get_candidate_ticket_ids(category: str = None) -> list[int]:
    """Runs exact-match SQL filters to narrow the candidate ticket set."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT ticket_id FROM tickets WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category.lower())

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]
    
def get_full_ticket_text(ticket_ids: list[int]) -> dict:
    """Fetches full description and resolution from SQL for context assembly."""
    if not ticket_ids:
        return {}
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the correct number of ? placeholders for the IN clause
    placeholders = ",".join("?" * len(ticket_ids))
    query = f"SELECT ticket_id, description, resolution FROM ticket_text WHERE ticket_id IN ({placeholders})"
    
    cursor.execute(query, ticket_ids)
    rows = cursor.fetchall()
    conn.close()
    
    return {row[0]: {"description": row[1], "resolution": row[2]} for row in rows}