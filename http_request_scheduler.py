import schedule
import time
import requests

def perform_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f'Успех: Запрос к {url} выполнен успешно')
        else:
            print(f'Ошибка: Запрос к {url} завершился с кодом состояния {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Ошибка: Запрос к {url} завершился неудачно - {e}')

    
def main():
    url = "https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT"  

    initial_delay = 10

    request_interval = 10

    schedule.every(initial_delay).seconds.do(perform_request, url)

    while True:
        schedule.run_pending()
        time.sleep(request_interval)

if __name__ == "__main__":
    main()
