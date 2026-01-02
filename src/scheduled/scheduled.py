from uuid import UUID

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.facade import UpBackFacade
from src.models.models import TrackedApp

scheduler = BackgroundScheduler()
upBackFacade = UpBackFacade()


def load_backup_jobs():
    print("Loading backup jobs")
    services: list[TrackedApp] = upBackFacade.get_tracked_apps()

    for service in services:
        print("Backing up service: ", service.file_path)
        if not service.auto_update:
            continue

        scheduler.add_job(
            backup_service,
            CronTrigger.from_crontab(service.cron),
            args=[service.uuid],
            id=f"backup-{service.uuid}",
            replace_existing=True,
            max_instances=1,
            coalesce=True
        )

    print([job.id for job in scheduler.get_jobs()])

def start_scheduler():
    print("Starting scheduler")
    scheduler.start()


def backup_service(service_uuid: UUID):
    upBackFacade.sync_app_by_uuid(service_uuid)
