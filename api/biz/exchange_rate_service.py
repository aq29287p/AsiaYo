
from .static import EXCHANGE_RATE
from decimal import Decimal, ROUND_HALF_UP
from api.biz.error import BusinessError
from api.common.amount_utils import dollar_amount_2_number, number_2_dollar_amount
class ExchangeRateService:
    def __init__(self) -> None:
        self._exchange_rate : dict = EXCHANGE_RATE

    def exchange_rate(self,source: str, target:str, amount:str)-> str:
        # 檢查是否支援貨幣
        self._check_parameter(source,target)
        # 金額轉型
        amount =dollar_amount_2_number(amount)
        # 乘上匯率
        res= Decimal(self._exchange_rate["currencies"][source][target])*amount
        
        # 四捨五入
        res = res.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return number_2_dollar_amount(res)

    @staticmethod
    def _check_parameter(source:str, target:str) -> None:
        for currency_type in [source,target]:
            if currency_type not in EXCHANGE_RATE["currencies"]:
                raise BusinessError(f"{currency_type} is not support")