import threading
import time
import zipfile
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from http import HTTPStatus
from typing import List
from uuid import UUID

import uuid

from apscheduler.triggers.cron import CronTrigger

from src.exceptions.exceptions import ApiException
from src.models.models import TrackedApp, Backup, SyncStatus

from src.database.database import DB
from src.services.synchronization_service import running_syncs
from src.utils.utils import sse, normalize_path


class UpBackFacade:
    def __init__(self):
        self.db = DB()

    def init_db(self):
        self.db.init_db()

    def get_tracked_app_by_file_path(self, file_path: str) -> TrackedApp | None:
        data = self.db.get_tracked_app_by_file_path(normalize_path(file_path))

        if data is None:
            raise ApiException("Tracked app not found", code=404)

        return TrackedApp(
            uuid=data[0],
            file_path=data[1],
            auto_update=bool(data[2]),
            cron=str(data[3])
        )

    def get_tracked_app_by_uuid(self, service_uuid: UUID) -> TrackedApp | None:
        data = self.db.get_tracked_app_by_uuid(service_uuid)

        if data is None:
            raise ApiException("Tracked app not found", code=404)

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

            existing_app = None
            try:
                existing_app = self.get_tracked_app_by_file_path(file_path)
            except ApiException as e:
                print(e)

            if existing_app is None:
                self.db.save_tracked_app(tracked_app)
                return HTTPStatus.CREATED
            else:
                raise ApiException("Tracked app already exists", code=HTTPStatus.CONFLICT)
        except KeyError:
            raise ApiException("Invalid parameters", code=400)

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

    def __sync_app(self, tracked_app: TrackedApp, sync_id):
        source_dir = Path(tracked_app.file_path)
        folder_name = source_dir.stem
        backup_dir = Path(__file__).parent.parent / "backups" / folder_name
        backup_dir.mkdir(parents=True, exist_ok=True)

        if not source_dir.is_dir():
            raise FileNotFoundError(f"{source_dir} could not be found")

        timestamp = datetime.now().timestamp()
        zip_path = backup_dir / f"{sync_id}_{folder_name}.zip"

        self.db.save_backup(Backup(
            backup_id=sync_id,
            app_id=str(tracked_app.uuid),
            file_path=normalize_path(str(zip_path)),
            timestamp=str(timestamp)
        ))

        files = [p for p in source_dir.rglob("*") if p.is_file()]
        total_files = len(files)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for idx, file in enumerate(files, start=1):
                arcname = file.relative_to(source_dir.parent)
                zipf.write(file, arcname)

                sync_status = SyncStatus(
                    app_id=str(tracked_app.uuid),
                    current=idx,
                    total=total_files,
                    file=str(file),
                )

                running_syncs[sync_id] = sync_status

                yield sync_status

                if idx == total_files:
                    running_syncs.pop(sync_id)

    def sync_all_apps(self):
        tracked_apps = self.get_tracked_apps()

        def __sync():
            for app_index, tracked_app in enumerate(tracked_apps):
                app_sync_id = str(uuid.uuid4())

                for _ in self.__sync_app(tracked_app, app_sync_id):
                    pass

        threading.Thread(target=__sync).start()

        return HTTPStatus.ACCEPTED.value


    def sync_app_by_uuid(self, service_uuid: UUID):
        tracked_app = self.get_tracked_app_by_uuid(service_uuid)
        sync_id = str(uuid.uuid4())

        if tracked_app is None:
            raise ApiException("No tracked app found", code=HTTPStatus.NOT_FOUND.value)

        def __sync(_sync_id):
            for _ in self.__sync_app(tracked_app, _sync_id):
                pass

        threading.Thread(target=__sync, args=(sync_id,)).start()

        return HTTPStatus.ACCEPTED.value

    def stream_all_syncs(self):
        while True:
            current_syncs = {sid: asdict(status) for sid, status in running_syncs.items()}

            if not current_syncs:
                yield sse(
                    data={
                        "current_app_syncs": {}
                    },
                    event="progress",
                )
            else:
                yield sse(
                    data={
                        "current_app_syncs": current_syncs
                    },
                    event="progress",
                )
            time.sleep(1)

    def get_app_backups(self, app_id: UUID) -> List[Backup]:
        backup_data = self.db.get_backups(app_id)

        backups: List[Backup] = []

        for backup in backup_data:
            backups.append(Backup(
                backup_id=backup[0],
                app_id=backup[1],
                file_path=backup[2].split("/")[-1],
                timestamp=backup[3],
            ))

        return backups
