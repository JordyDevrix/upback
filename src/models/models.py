from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class TrackedApp:
    uuid: UUID
    file_path: str
    auto_update: bool
    cron: str

@dataclass
class Backup:
    backup_id: str
    app_id: str
    file_path: str
    timestamp: str

@dataclass
class SyncStatus:
    app_id: str
    current: int
    total: int
    file: str

