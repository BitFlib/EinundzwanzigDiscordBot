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

def get_price_euro():
    """
    Get the current Euro price for BTC
    """
    price_rates = __get_price()
    price_eur = price_rates['EUR']
    return float(price_eur)

def get_sats_per_euro(euro_amount):
    """
    Get the amount of sats for specified euro amount
    """
    price_rates = __get_price()
    price_eur = float(price_rates['EUR'])
    return int(euro_amount/price_eur * 100000000)

def get_euro_per_sats(sats_amount):
    """
    Get the amount of euro for specified sats amount
    """
    price_rates = __get_price()
    price_eur = float(price_rates['EUR'])
    return float(price_eur / 100000000 * sats_amount)