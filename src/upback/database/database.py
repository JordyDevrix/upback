import sqlite3
from pathlib import Path
from typing import List
from uuid import UUID

from upback.models.models import TrackedApp, Backup


class DB:
    def __init__(self):
        self.db_tracked_apps_path = Path(__file__).parent.parent.parent.parent / "upback_data" / "tracked_apps.db"
        self.db_tracked_apps_path.parent.mkdir(parents=True, exist_ok=True)  # ensure directory exists

        self.db_backups_path = Path(__file__).parent.parent.parent.parent / "upback_data" / "backups.db"
        self.db_backups_path.parent.mkdir(parents=True, exist_ok=True)  # ensure directory exists

    def init_db(self):
        tracked_apps_sql = """
        CREATE TABLE IF NOT EXISTS tracked_apps (
            uuid TEXT PRIMARY KEY NOT NULL,
            file_path TEXT NOT NULL,
            auto_update BOOLEAN NOT NULL,
            cron TEXT NOT NULL
        )
        """

        backups_sql = """
        CREATE TABLE IF NOT EXISTS backups (
            uuid TEXT PRIMARY KEY NOT NULL,
            app_id TEXT NOT NULL,
            file_path TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """

        with sqlite3.connect(self.db_tracked_apps_path) as conn:
            conn.execute(tracked_apps_sql)
            conn.commit()

        with sqlite3.connect(self.db_backups_path) as conn:
            conn.execute(backups_sql)
            conn.commit()

    def save_tracked_app(self, tracked_app: TrackedApp):
        sql = """
        INSERT INTO tracked_apps (uuid, file_path, auto_update, cron)
        VALUES (?, ?, ?, ?)
        """
        try:
            with sqlite3.connect(self.db_tracked_apps_path) as conn:
                conn.execute(sql, (str(tracked_app.uuid), tracked_app.file_path, tracked_app.auto_update, tracked_app.cron))
                conn.commit()
        except Exception as e:
            print("DB Error:", e)

    def save_backup(self, backup: Backup):
        sql = """
        INSERT INTO backups (uuid, app_id, file_path, timestamp)
        VALUES (?, ?, ?, ?)
        """
        try:
            with sqlite3.connect(self.db_backups_path) as conn:
                conn.execute(sql, (backup.backup_id, backup.app_id, backup.file_path, backup.timestamp))
                conn.commit()
        except Exception as e:
            print("DB Error:", e)

    def get_backups(self, app_id: UUID) -> List[tuple]:
        sql = "SELECT * FROM backups WHERE app_id = ?"
        with sqlite3.connect(self.db_backups_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (app_id,))
            return cursor.fetchall()

    def get_tracked_apps(self):
        sql = "SELECT * FROM tracked_apps"
        with sqlite3.connect(self.db_tracked_apps_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()

    def get_tracked_app_by_file_path(self, file_path: str) -> tuple:
        sql = "SELECT * FROM tracked_apps WHERE file_path = ?"
        with sqlite3.connect(self.db_tracked_apps_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (file_path,))
            return cursor.fetchone()

    def get_tracked_app_by_uuid(self, service_uuid: UUID) -> tuple:
        sql = "SELECT * FROM tracked_apps WHERE uuid = ?"
        with sqlite3.connect(self.db_tracked_apps_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (str(service_uuid),))
            return cursor.fetchone()



