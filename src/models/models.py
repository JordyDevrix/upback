from dataclasses import dataclass
from uuid import UUID


@dataclass
class TrackedApp:
    uuid: UUID
    file_path: str
    auto_update: bool
