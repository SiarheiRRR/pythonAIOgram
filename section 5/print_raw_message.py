import requests
import time
import json

API_URL: str = 'https://api.telegram.org/bot'
BOT_TOKEN: str = '6227598425:AAEwerbJVV00gAGYICc8O1GbM5Zx-qwCd-E'
offset: int = -2
updates: dict
timeout: int = 50

def do_something(result) -> None:
    print(json.dumps(result, indent=4))


while True:
    start_time = time.time()
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&timeout={timeout}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            do_something(result)
    end_time = time.time()
    # print(f'Время между запросами к Telegram Bot API: {end_time - start_time}')