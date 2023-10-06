from flask import request
from flask_restful import Resource, reqparse
from requests import Response

from api.biz.exchange_rate_service import ExchangeRateService
from api.biz.error import DataValidationError
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiExchangeRate(Resource):
    @inject_service()
    def __init__(self, exchange_rate_service: ExchangeRateService) -> None:
        self._exchange_rate_service = exchange_rate_service

    def get(self) -> Response:
        # 提取參數
        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, help='You need to enter source', required=True,location='args')
        parser.add_argument('target', type=str, help='You need to enter target', required=True,location='args')
        parser.add_argument('amount', type=str, help='You need to enter amount', required=True,location='args')

        args = parser.parse_args()
        # 參數格式檢查
        self._check_parameter(args)
        # 匯率轉換
        res=self._exchange_rate_service.exchange_rate(args['source'],args['target'],args['amount'])
        
        return api_response(message="Success", amount=res)
    @staticmethod
    def _check_parameter(args) -> None:
        for arg in ["source", "target","amount"]:
            if arg not in args:
                raise DataValidationError(f"缺少 {arg} 參數.")
            if not isinstance(arg, str):
                raise DataValidationError(f"{arg} 應為字串型態.")
            if arg == "amount":
                if args["amount"][0] != "$":
                    raise DataValidationError(f"{arg} 應以 $ 開頭 例如 $12.45")
                if not args["amount"].replace('$','').replace(',','').replace('.','',1).isdigit() :
                    raise DataValidationError(f"{arg} 應以 $後面應為數字 例如 $12.45")
