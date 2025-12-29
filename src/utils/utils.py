from pathlib import Path


def sse(data=None, event=None, id=None, retry=None):
    msg = ""
    if id is not None:
        msg += f"id: {id}\n"
    if event is not None:
        msg += f"event: {event}\n"
    if retry is not None:
        msg += f"retry: {retry}\n"
    if data is not None:
        msg += f"data: {data}\n"
    return msg + "\n"


def normalize_path(path: str) -> str:
    return Path(path).expanduser().resolve().as_posix()
