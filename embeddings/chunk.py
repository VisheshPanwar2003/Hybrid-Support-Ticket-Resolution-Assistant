def create_whole_ticket_chunk(description: str, resolution: str) -> str:
    """Concatenates description and resolution for whole-ticket embedding."""
    desc = description.strip() if description else ""
    res = resolution.strip() if resolution else ""
    
    if desc and res:
        return f"Description: {desc} Resolution: {res}"
    elif desc:
        return f"Description: {desc}"
    else:
        return ""