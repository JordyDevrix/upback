from flask import jsonify, Flask
from src.exceptions.exceptions import ApiException


class GlobalExceptionHandler:
    def __init__(self, app: Flask):
        self.app = app
        app.register_error_handler(Exception, self.handle_error)

    def handle_error(self, e):
        if isinstance(e, ApiException):
            return jsonify(error=e.message, code=e.code), e.code

        self.app.logger.exception(e)
        return jsonify(error="Internal Server Error", code=500), 500

