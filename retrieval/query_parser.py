def parse_query_constraints(query: str) -> dict:
    """Lightweight extraction of structured constraints from a natural language query."""
    query_lower = query.lower()
    constraints = {}
    
    # Simple keyword matching based on our dataset categories
    categories = ['login', 'billing', 'ui', 'hardware']
    for cat in categories:
        if cat in query_lower:
            constraints['category'] = cat
            break 
            
    return constraints