import requests
import json
from config import keys

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Function dose not allow to convert the same currenscies {base}')
    
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Unsuccssefully currency elaboration {quote}')
        
        try:
            base_ticker = keys[base]
        except:
            raise APIException(f'Unsuccssefully currency elaboration {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Amount must be float value')

        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={quote_ticker}&symbols={base_ticker}")
        total_amount = json.loads(r.content) 
        return "{0:.3f}".format(total_amount['rates'][base_ticker] * amount), total_amount['date']
