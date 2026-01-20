import json
import os
import time
from datetime import datetime
from pathlib import Path

import croniter
from cron_descriptor import get_description
from apscheduler.triggers.cron import CronTrigger

from upback.constants.constants import SYSTEM_TIME_ZONE
from upback.exceptions.exceptions import ApiException


def sse(data=None, event=None, id=None, retry=None):
    msg = ""
    if id is not None:
        msg += f"id: {id}\n"
    if event is not None:
        msg += f"event: {event}\n"
    if retry is not None:
        msg += f"retry: {retry}\n"
    if data is not None:
        payload = json.dumps(data)
        msg += f"data: {payload}\n"
    return msg + "\n"


def normalize_path(path: str) -> str:
    return Path(path).expanduser().resolve().as_posix()


def get_cron_description(cron: str) -> str:
    return get_description(cron)


def get_next_run(cron_expr: str):
    parts = cron_expr.split()

    # Map standard cron digits to names to bypass APScheduler's 0-index issue
    # Standard: 0=Sun, 1=Mon, ..., 7=Sun
    cron_mapping = {
        '0': 'sun', '1': 'mon', '2': 'tue', '3': 'wed',
        '4': 'thu', '5': 'fri', '6': 'sat', '7': 'sun'
    }

    # check if the last part (Day of Week) is a single digit
    if len(parts) == 5 and parts[4] in cron_mapping:
        parts[4] = cron_mapping[parts[4]]
        cron_expr = " ".join(parts)

    now = datetime.now(SYSTEM_TIME_ZONE)
    trigger = CronTrigger.from_crontab(cron_expr, timezone=SYSTEM_TIME_ZONE)
    return trigger.get_next_fire_time(None, now)


def stream_next_cron(cron_expr: str):
    try:
        while True:
            now = datetime.now(SYSTEM_TIME_ZONE)

            next_run = get_next_run(cron_expr)

            if next_run is None:
                break

            delta = next_run - now
            seconds_left = max(int(delta.total_seconds()), 0)

            yield sse(
                data={
                    "next_run": next_run.isoformat(),
                    "seconds_remaining": seconds_left,
                    "human_readable": get_description(cron_expr),
                    "sync_run": seconds_left == 0
                },
                id=None,
                event="next_run",
            )

            time.sleep(1)
    except GeneratorExit:
        return


def get_folder_data(path: str) -> list[dict]:
    if not os.path.exists(path) or not os.path.isdir(path):
        raise ApiException("Invalid path", code=400)

    items = []
    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        items.append({
            "name": name,
            "path": full_path,
            "is_dir": os.path.isdir(full_path)
        })

    return items


def get_home_directory() -> Path:
    return Path.home()


def sort_by_cron(apps):
    return sorted(
        apps,
        key=lambda app: get_next_run(app.cron)
    )
