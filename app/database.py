import sqlite3

DATABASE_NAME = "store.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def create_tables():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        visitor_id TEXT,
        camera_id TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_event(event):
    conn = get_connection()

    conn.execute("""
    INSERT INTO events (event_type, visitor_id, camera_id, timestamp)
    VALUES (?, ?, ?, ?)
    """, (
        event.event_type,
        event.visitor_id,
        event.camera_id,
        event.timestamp
    ))

    conn.commit()
    conn.close()