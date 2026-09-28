import pandas as pd

def clean_tickets(csv_path: str) -> pd.DataFrame:
    """Loads and sanitizes raw ticket data."""
    df = pd.read_csv(csv_path)

    for col in ['category', 'priority', 'status']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()

    df = df.dropna(subset=['description'])

    if 'resolution' in df.columns:
        df['resolution'] = df['resolution'].fillna('')
        df = df.drop_duplicates(subset=['description', 'resolution'])
        df['resolution'] = df['resolution'].replace('', None)

    df['created_date'] = pd.to_datetime(df['created_date']).dt.strftime('%Y-%m-%d')
    if 'resolved_date' in df.columns:
        df['resolved_date'] = pd.to_datetime(df['resolved_date']).dt.strftime('%Y-%m-%d')

    return df