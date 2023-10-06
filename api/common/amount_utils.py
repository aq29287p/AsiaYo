from decimal import Decimal
def dollar_amount_2_number(amount:str)-> Decimal:
    """
    $1,234.56 -> 1234.56
    """
    return Decimal(amount.replace('$','').replace(',',''))

def number_2_dollar_amount(amount:Decimal)-> str:
    """
    $1,234.56 <- 1234.56
    """
    return '$'+f'{amount:,}'