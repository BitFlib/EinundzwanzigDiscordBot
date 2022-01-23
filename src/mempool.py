import requests

def blocktime():
    """
    Get the current tip height of mainnet blockchain
    """
    try:
        r = requests.get('https://mempool.space/api/blocks/tip/height', timeout=5)
        print(type(r.json()))
        print(r.json())
        return r.json()
    except requests.exceptions.RequestException as e:
        print(e)  
        return "Server nicht erreichbar. Bitte versuche es später erneut"