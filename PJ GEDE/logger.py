"""
Logger module: logs to local sqlite DB and can POST to website endpoint.
"""

import sqlite3
import json
import time
import os
import requests

DB_PATH = "sealen_logs.db"

class Logger:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Create database table if not exists."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            image TEXT,
            detections TEXT,
            decision TEXT
        )
        """)
        conn.commit()
        conn.close()

    def log_event(self, event_dict):
        """Save event to DB and optionally send to endpoint."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Insert log entry
        c.execute("""
        INSERT INTO logs (timestamp, image, detections, decision)
        VALUES (?, ?, ?, ?)
        """, (
            event_dict.get("timestamp", time.time()),
            json.dumps(event_dict.get("image")),
            json.dumps(event_dict.get("detections")),
            json.dumps(event_dict.get("decision")),
        ))

        conn.commit()
        conn.close()

        # Optional send to website API
        endpoint = os.getenv('SEALEN_ENDPOINT')
        if endpoint:
            try:
                requests.post(endpoint, json=event_dict, timeout=5)
            except Exception as e:
                print("Failed to send to endpoint:", e)
