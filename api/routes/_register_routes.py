from flask import Flask
from flask_restful import Api

from api.routes.api_home import ApiHome
from api.routes.api_exchange_rate import ApiExchangeRate

from api.routes.open_api_spec import OpenApiSpec

from config.api_config import Config


def setup_routes(app: Flask):
    if Config.ENV_SET.lower() in ["dev", 'local']:
        @app.route('/open-api-spec', defaults={'path': None})
        @app.route('/open-api-spec/', defaults={'path': None})
        @app.route('/open-api-spec/<path:path>')
        def send_open_api_spec(path: str):
            return OpenApiSpec.resolve_content(path)

    api = Api(app)
    api.add_resource(ApiHome, "/")

    # 匯率轉換
    api.add_resource(ApiExchangeRate,"/exchange-rate", endpoint="exchange-rate")
