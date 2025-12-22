import sqlite3
from pathlib import Path
from src.models.models import TrackedApp


class DB:
    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "upback_data" / "tracked_apps.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)  # ensure directory exists

    def init_db(self):
        sql = """
        CREATE TABLE IF NOT EXISTS tracked_apps (
            uuid TEXT PRIMARY KEY NOT NULL,
            file_path TEXT NOT NULL,
            auto_update BOOLEAN NOT NULL
        )
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(sql)
            conn.commit()

    def save_tracked_app(self, tracked_app: TrackedApp):
        sql = """
        INSERT INTO tracked_apps (uuid, file_path, auto_update)
        VALUES (?, ?, ?)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(sql, (str(tracked_app.uuid), tracked_app.file_path, tracked_app.auto_update))
                conn.commit()
        except Exception as e:
            print("DB Error:", e)

    def get_tracked_apps(self):
        sql = "SELECT * FROM tracked_apps"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
