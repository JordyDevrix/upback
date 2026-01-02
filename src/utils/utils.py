import json
import time
from datetime import datetime, timezone
from pathlib import Path
from cron_descriptor import get_description
from apscheduler.triggers.cron import CronTrigger

from src.constants.constants import SYSTEM_TIME_ZONE


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
    trigger = CronTrigger.from_crontab(cron_expr)
    return trigger.get_next_fire_time(None, datetime.now())

def stream_next_cron(cron: str):
    try:
        while True:
            next_run = get_next_run(cron)

            delta = next_run - datetime.now(SYSTEM_TIME_ZONE)
            seconds_left = max(int(delta.total_seconds()), 0)


            if seconds_left == 0:
                yield sse(
                    data={
                        "next_run": next_run.isoformat(),
                        "seconds_remaining": seconds_left,
                        "human_readable": get_cron_description(cron),
                        "sync_run": True,
                    },
                    event="next_run",
                    id=None,
                )


            yield sse(
                data={
                    "next_run": next_run.isoformat(),
                    "seconds_remaining": seconds_left,
                    "human_readable": get_cron_description(cron),
                    "sync_run": False,
                },
                event="next_run",
                id=None,
            )

            time.sleep(1)  # 5s is plenty

    except GeneratorExit:
        # Client disconnected
        return
