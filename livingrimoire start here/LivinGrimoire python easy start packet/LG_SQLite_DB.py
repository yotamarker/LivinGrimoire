import sqlite3
from pathlib import Path

from LivinGrimoirePacket.LivinGrimoire import AbsDictionaryDB


class SQLiteDictionaryDB(AbsDictionaryDB):
    def __init__(self, db_path: str = "dictionary.db"):
        self.db_path = Path(db_path)
        self._ensure_db()

    def _ensure_db(self):
        """Create DB file and table if not exists."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS kv_store (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def save(self, key: str, value: str):
        """Insert or update a key/value pair."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO kv_store (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, value))
        conn.commit()
        conn.close()
        return f"saved:{key}"

    def load(self, key: str) -> str:
        """Return the value for a key, or 'null' if missing."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT value FROM kv_store WHERE key=?", (key,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else "null"

    def dataExists(self, key: str) -> bool:
        """Check if a key exists in the DB."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM kv_store WHERE key=?", (key,))
        exists = cur.fetchone() is not None
        conn.close()
        return exists