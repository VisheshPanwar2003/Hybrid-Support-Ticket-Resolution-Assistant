DROP TABLE IF EXISTS ticket_text;
DROP TABLE IF EXISTS tickets;

CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    created_date DATE NOT NULL,
    resolved_date DATE
);

CREATE TABLE ticket_text (
    ticket_id INTEGER PRIMARY KEY REFERENCES tickets(ticket_id),
    description TEXT NOT NULL,
    resolution TEXT
);