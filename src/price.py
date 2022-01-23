import requests

def __get_price():
    """
    Get the current price rates from coinbase for BTC
    """
    try:
        r = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=BTC', timeout=5)
        price_rates = r.json()['data']['rates']
        return price_rates
    except requests.exceptions.RequestException as e:  
        raise SystemExit(e)

def get_prices():
    """
    Get the current Euro/CHF/USD price for BTC
    """
    price_rates = __get_price()
    price_usd = float(price_rates['USD'])
    price_eur = float(price_rates['EUR'])
    price_chf = float(price_rates['CHF'])
    return price_usd, price_eur, price_chf

def get_sats_per_currency(currency, currency_amount):
    """
    Get the amount of sats for specified euro amount
    """
    price_rates = __get_price()
    price_currency = float(price_rates[currency])
    return int(currency_amount/price_currency * 100000000)

def get_currency_per_sats(currency, sats_amount):
    """
    Get the amount of euro for specified sats amount
    """
    price_rates = __get_price()
    price_eur = float(price_rates[currency])
    return float(price_eur / 100000000 * sats_amount)

def moscow_time():
    """
    Get the current moscow time (and also coresponding eur/chf counterpart)
    """
    price_rates = __get_price()
    price_usd = float(price_rates['USD'])
    price_eur = float(price_rates['EUR'])
    price_chf = float(price_rates['CHF'])
    mt_usd = int(1/price_usd * 100000000)
    mt_eur = int(1/price_eur * 100000000)
    mt_chf = int(1/price_chf * 100000000)
    return mt_usd,mt_eur,mt_chf
