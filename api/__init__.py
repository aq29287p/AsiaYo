import base64
from http import HTTPStatus

from flask import Flask, request, jsonify
from flask_cors import CORS


from api.biz.error import BaseError, BusinessError

from api.common.logger import Logging
from api.common.response_utils import api_response
from api.containers.services_container import ServicesContainer
from config.api_config import Config


def create_app():  # noqa: C901
    from .routes import setup_routes
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='templates/static',
        static_url_path='/static'
    )
    app.config.from_object(Config)

    CORS(app)
    Logging(app)
    ServicesContainer(app)
    setup_routes(app)



    @app.errorhandler(Exception)
    def handle_exception(e):
        from jsonschema import ValidationError
        from werkzeug.exceptions import HTTPException

        if isinstance(e, (BusinessError, BaseError)):
            return api_response(
                http_status=e.http_status_code,
                message=e.description,
                code=e.code or e.http_status_code,
                data=e.data,
            )

        if isinstance(e, ValidationError):
            path = '.'.join(['[{}]'.format(p) if not isinstance(p, str) else p for p in list(e.path)])
            msg = '`{}`: {}'.format(path, e.message)
            return api_response(http_status=422, message=msg)

        if isinstance(e, HTTPException):
            return api_response(http_status=e.code, message=e.description)

        msg_tail = ""
        max_len = 1024
        data = request.get_data()
        if data:
            if isinstance(data, bytes):
                try:
                    data_str = data[0:max_len].decode('utf-8')
                except Exception:
                    data_str = None
                if not data_str:
                    try:
                        data_str = f'b64encoded:{base64.b64encode(data[0:max_len])}'
                    except Exception:
                        data_str = f'raw:{data[0:max_len]}'
            else:
                data_str = data[0:max_len]
            msg_tail = f"\nPayload: {data_str}"

        request_uri = request.path
        query_string = request.query_string.decode()
        if query_string:
            request_uri += f"?{query_string}"

        referer = request.headers.get("Referer")
        ref_msg = ''
        if referer:
            ref_msg = f'\nReferer: {referer}'

        user_agent = request.headers.get('User-Agent')
        user_agent_msg = ''
        if user_agent:
            user_agent_msg = f'\nUser-Agent: {user_agent}'

        app.logger.error(
            f'Exception on [{request.method}] {request_uri} from '
            f'{list(request.access_route)}{ref_msg}{user_agent_msg}{msg_tail}',
            exc_info=e
        )
        msg = str(e) if app.debug else HTTPStatus(HTTPStatus.INTERNAL_SERVER_ERROR).phrase

        return api_response(http_status=500, message=msg)

    return app
