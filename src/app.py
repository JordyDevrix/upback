from typing import List

from flask import Flask, Response, jsonify, request
from src.facade import UpBackFacade
from src.models.models import TrackedApp

app = Flask(__name__)


@app.route("/tracked-apps", methods=["GET"])
def get_tracked_apps() -> List[TrackedApp]:
    return upBackFacade.get_tracked_apps()

@app.route("/tracked-apps", methods=["POST"])
def save_tracked_apps():
    data = request.get_json()

    if not data:
        return Response(status=400)

    return Response(upBackFacade.save_tracked_apps(data))


if __name__ == '__main__':
    upBackFacade = UpBackFacade()
    upBackFacade.init_db()
    app.run(host='0.0.0.0', port=8080, debug=False)
