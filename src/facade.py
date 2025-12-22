from typing import List
from uuid import UUID

import uuid

from src.models.models import TrackedApp

from src.database.database import DB


class UpBackFacade:
    def __init__(self):
        self.db = DB()

    def init_db(self):
        self.db.init_db()

    def save_tracked_apps(self, data: dict):
        generated_uuid: UUID = uuid.uuid4()
        tracked_app = TrackedApp(
            uuid=generated_uuid,
            file_path=str(data["file_path"]),
            auto_update=bool(data["auto_update"])
        )
        self.db.save_tracked_app(tracked_app)

    def get_tracked_apps(self) -> List[TrackedApp]:
        raw_rows = self.db.get_tracked_apps()
        tracked_apps: List[TrackedApp] = [
            TrackedApp(
                uuid=row[0],
                file_path=row[1],
                auto_update=bool(row[2])
            )
            for row in raw_rows
        ]
        return tracked_apps
