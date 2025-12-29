import os
from datetime import datetime
from pathlib import Path
import shutil
from http import HTTPStatus
from typing import List
from uuid import UUID

import uuid

from apscheduler.triggers.cron import CronTrigger

from src.models.models import TrackedApp

from src.database.database import DB
from src.utils.utils import sse, normalize_path


class UpBackFacade:
    def __init__(self):
        self.db = DB()

    def init_db(self):
        self.db.init_db()

    def get_tracked_app_by_file_path(self, file_path: str) -> TrackedApp | None:
        data = self.db.get_tracked_app_by_file_path(normalize_path(file_path))

        if data is None:
            return None

        return TrackedApp(
            uuid=data[0],
            file_path=data[1],
            auto_update=bool(data[2]),
            cron=str(data[3])
        )

    def get_tracked_app_by_uuid(self, service_uuid: UUID) -> TrackedApp | None:
        data = self.db.get_tracked_app_by_uuid(service_uuid)

        if data is None:
            return None

        return TrackedApp(
            uuid=data[0],
            file_path=data[1],
            auto_update=bool(data[2]),
            cron=str(data[3])
        )

    def save_tracked_apps(self, data: dict) -> HTTPStatus:
        try:
            generated_uuid: UUID = uuid.uuid4()
            file_path: str = normalize_path(data["file_path"])
            CronTrigger.from_crontab(data["cron"])

            tracked_app = TrackedApp(
                uuid=generated_uuid,
                file_path=str(file_path),
                auto_update=bool(data["auto_update"]),
                cron=str(data["cron"]),
            )

            existing_app = self.get_tracked_app_by_file_path(file_path)

            if existing_app is None:
                self.db.save_tracked_app(tracked_app)
                return HTTPStatus.CREATED
            else:
                return HTTPStatus.CONFLICT
        except KeyError:
            return HTTPStatus.BAD_REQUEST
        except Exception as e:
            print(e)
            return HTTPStatus.INTERNAL_SERVER_ERROR

    def get_tracked_apps(self) -> List[TrackedApp]:
        raw_rows = self.db.get_tracked_apps()
        tracked_apps: List[TrackedApp] = [
            TrackedApp(
                uuid=row[0],
                file_path=row[1],
                auto_update=bool(row[2]),
                cron=str(row[3])
            )
            for row in raw_rows
        ]
        return tracked_apps

    def sync_app(self, tracked_app: TrackedApp):
        source_dir = Path(tracked_app.file_path)
        folder_name = source_dir.stem
        backup_dir = Path(__file__).parent.parent.joinpath("backups").joinpath(folder_name)
        backup_dir.mkdir(parents=True, exist_ok=True)

        if not source_dir.is_dir():
            raise FileNotFoundError(f"{source_dir} could not be found")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        archive_base = backup_dir.joinpath(f"{timestamp}_{folder_name}")

        shutil.make_archive(
            base_name=str(archive_base),
            format="zip",
            root_dir=source_dir.parent,
            base_dir=source_dir.name
        )

    def sync_all_apps(self):
        tracked_apps = self.get_tracked_apps()
        synced_apps: List[TrackedApp] = []
        for idx, tracked_app in enumerate(tracked_apps):
            try:
                yield sse(
                    data={
                        "index": idx + 1,
                        "amount": len(tracked_apps),
                        "uuid": tracked_app.uuid,
                        "file_path": tracked_app.file_path,
                        "status": "starting"
                    },
                    event="progress",
                    id=idx
                )

                self.sync_app(tracked_app)

                yield sse(
                    data={
                        "index": idx + 1,
                        "amount": len(tracked_apps),
                        "uuid": tracked_app.uuid,
                        "file_path": tracked_app.file_path,
                        "status": "success"
                    },
                    event="progress",
                    id=idx
                )
                synced_apps.append(tracked_app)
            except Exception as e:
                yield sse(
                    data={
                        "status": f"{e.__class__.__name__}: {str(e)}",
                    },
                    event="error",
                    id=1
                )

        yield sse(
            data={
                "status": "finished",
                "amount_synced": len(synced_apps),
                "amount_failed": len(tracked_apps) - len(synced_apps)
            },
            event="done",
            id=0
        )
