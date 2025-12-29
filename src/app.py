from typing import List
from flask import Flask, Response, request
from src.facade import UpBackFacade
from src.scheduled import scheduled
from src.models.models import TrackedApp

app = Flask(__name__)


@app.route("/tracked-apps", methods=["GET"])
def get_tracked_apps() -> List[TrackedApp]:
    return upBackFacade.get_tracked_apps()


@app.route("/tracked-apps", methods=["POST"])
def save_tracked_apps():
    data = request.get_json()
    return Response(status=upBackFacade.save_tracked_apps(data))


@app.route("/tracked-apps/sync", methods=["POST"])
def sync_tracked_apps():
    return Response(
        upBackFacade.sync_all_apps(),
        mimetype="text/event-stream"
    )


if __name__ == '__main__':
    upBackFacade = UpBackFacade()
    upBackFacade.init_db()

    scheduled.load_backup_jobs()
    scheduled.start_scheduler()

    app.run(host='0.0.0.0', port=8080, debug=False)
