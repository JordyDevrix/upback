import argparse
import os
from dataclasses import asdict
from typing import List
from uuid import UUID
from flask import Flask, Response, request, render_template, jsonify, current_app

from upback.config.global_exception_handler import GlobalExceptionHandler
from upback.facades.facade import UpBackFacade
from upback.scheduled import scheduled
from upback.models.models import TrackedApp
from upback.services.synchronization_service import running_syncs
from upback.utils.utils import get_cron_description, stream_next_cron, get_folder_data, get_home_directory, sort_by_cron

here = os.path.dirname(os.path.abspath(__file__))
print(here)
app = Flask(
    __name__,
    template_folder=os.path.join(here, "templates"),
    static_folder=os.path.join(here, "static")
)
upBackFacade = UpBackFacade()
global_exception_handler = GlobalExceptionHandler(app)


@app.route("/api/tracked-apps", methods=["GET"])
def get_tracked_apps_api() -> List[TrackedApp]:
    return upBackFacade.get_tracked_apps()

@app.route("/api/tracked-apps/<uuid>", methods=["GET"])
def get_tracked_app_api(uuid: UUID) -> Response:
    return jsonify(asdict(upBackFacade.get_tracked_app_by_uuid(uuid)))

@app.route("/api/tracked-apps/<uuid>/status", methods=["GET"])
def get_tracked_app_status_api(uuid: UUID) -> Response:
    return jsonify({"enabled": upBackFacade.get_tracked_app_status(uuid)})


@app.route("/api/tracked-apps/update/<uuid>", methods=["PUT"])
def update_tracked_app_api(uuid: UUID) -> Response:
    data = request.get_json()
    upBackFacade.update_tracked_app(data, uuid)
    scheduled.load_backup_jobs()
    return Response(status=200)


@app.route("/api/tracked-apps", methods=["POST"])
def save_tracked_apps_api():
    data = request.get_json()
    status = upBackFacade.save_tracked_apps(data)
    scheduled.load_backup_jobs()
    return Response(status=status)


@app.route("/api/tracked-apps/sync", methods=["POST"])
def sync_all_tracked_apps_api():
    return Response(status=upBackFacade.sync_all_apps())


@app.route("/api/tracked-apps/sync/<uuid>", methods=["POST"])
def sync_tracked_app_api(uuid: UUID):
    return Response(status=upBackFacade.sync_app_by_uuid(uuid))


@app.route("/api/tracked-apps/<uuid>/backups", methods=["GET"])
def get_tracked_apps_backups_api(uuid: UUID):
    backups = upBackFacade.get_app_backups(uuid)
    return jsonify({
        "backups": [
            {
                "file_path": b.file_path,
                "timestamp": b.timestamp,
                "backup_id": b.backup_id
            }
            for b in backups
        ]
    })


@app.route("/api/tracked-apps/syncs", methods=["GET"])
def stream_all_syncs():
    return Response(
        upBackFacade.stream_all_syncs(),
        mimetype="text/event-stream"
    )


@app.route("/api/tracked-apps/next-cron/<uuid>", methods=["GET"])
def get_tracked_apps_next_cron_api(uuid: UUID):
    tracked_app = upBackFacade.get_tracked_app_by_uuid(uuid)

    return Response(
        stream_next_cron(tracked_app.cron),
        mimetype="text/event-stream"
    )


@app.route("/api/file-system/api-path", methods=["GET"])
def get_file_system_api_path_api():
    return jsonify({"path": str(get_home_directory())})


@app.route("/api/file-system", methods=["GET"])
def get_file_system_api():
    path = request.args.get("path")
    return jsonify(get_folder_data(path))


@app.route("/api/tracked-apps/<uuid>", methods=["DELETE"])
def delete_tracked_api(uuid: UUID):
    upBackFacade.delete_tracked_app_by_uuid(uuid)
    scheduled.load_backup_jobs()
    return Response(status=200)


# Frontend routes
@app.route("/", methods=["GET"])
def home_web():
    tracked_apps = upBackFacade.get_tracked_apps()
    backups = upBackFacade.get_all_backups()
    found_backup_files = []
    size_bytes = 0

    for backup in backups:
        files = upBackFacade.get_backup_files(backup.backup_id)
        if files is not None:
            found_backup_files.append(files)
            size_bytes += files.file_size

    if size_bytes >= 1_000_000_000:
        total_filesize = f"{size_bytes / 1_000_000_000:.2f} GB"
    else:
        total_filesize = f"{size_bytes / 1_000_000:.2f} MB"

    return render_template(
        "index.html",
        tracked_apps=sort_by_cron(tracked_apps),
        tracked_apps_enabled=[_app for _app in tracked_apps if _app.auto_update == True],
        tracked_apps_amount=len(tracked_apps),
        backups=backups,
        backups_amount=len(backups),
        backup_files_found_amount=len(found_backup_files),
        backup_files_size=total_filesize
    )


@app.route("/settings", methods=["GET"])
def settings_web():
    return render_template("settings.html")


@app.route("/tracked-apps", methods=["GET"])
def get_tracked_apps_web():
    return render_template("tracked_apps.html", tracked_apps=upBackFacade.get_tracked_apps())


@app.route("/tracked-apps/<uuid>", methods=["GET"])
def get_tracked_app_web(uuid: UUID):
    tracked_app = upBackFacade.get_tracked_app_by_uuid(uuid)
    return render_template(
        "tracked_app.html",
        tracked_app=tracked_app,
        human_cron=get_cron_description(tracked_app.cron),
        active_syncs=list(set(running_syncs.keys()))
    )


@app.route("/add-tracked-app", methods=["GET"])
def add_tracked_app_web():
    return render_template("add_tracked_app.html")


@app.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("favicon.ico")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", type=int, default=8080)
    args = parser.parse_args()

    upBackFacade.init_db()

    scheduled.load_backup_jobs()
    scheduled.start_scheduler()

    app.run(host='0.0.0.0', port=args.port, threaded=True)


if __name__ == '__main__':
    main()
