import schedule
import time
import requests

def test():
    print("Hello World")
    print(time.ctime())

def get_btc_price():
    print("=====BTC=====")
    url = 'https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    response = requests.get(url=url).json()
    # print(response)
    """Нужно из переменной response вытащить стоимость биткоина
    и вывести его таким образом 
    (Стоимость биткоина на {текущее время} {цена биткоина}$)
    """
    price  = response.get('price')
    print(f"Стоимость биткоина на {time.ctime()}- {price}$ ")

# schedule.every(10).seconds.do(test)
# schedule.every(1).minutes.do(test)
# schedule.every().day.at("18:23").do(test)
# schedule.every().thursday.at("18:25").do(test)
# schedule.every().day.at("18:31").do(test)
schedule.every(2).seconds.do(get_btc_price)

while True:
    schedule.run_pending()