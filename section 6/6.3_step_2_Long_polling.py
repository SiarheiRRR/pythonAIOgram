import requests
import time


API_URL: str = 'https://api.telegram.org/bot'
BOT_TOKEN: str = '6227598425:AAEwerbJVV00gAGYICc8O1GbM5Zx-qwCd-E'
offset: int = -2
timeout: float = 100
updates: dict


def do_something() -> None:
    print('Был апдейт')


while True:
    start_time = time.time()
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&timeout={timeout}').json()

    if updates['result']:
        for result in updates['result']:
            from aiogram import Bot, Dispatcher
            from aiogram.filters import Command
            from aiogram.types import Message

            # Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
            API_TOKEN: str = 'BOT TOKEN HERE'

            # Создаем объекты бота и диспетчера
            bot: Bot = Bot(token=API_TOKEN)
            dp: Dispatcher = Dispatcher()


            # Этот хэндлер будет срабатывать на команду "/start"
            @dp.message(Command(commands=["start"]))
            async def process_start_command(message: Message):
                await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


            # Этот хэндлер будет срабатывать на команду "/help"
            @dp.message(Command(commands=['help']))
            async def process_help_command(message: Message):
                await message.answer('Напиши мне что-нибудь и в ответ '
                                     'я пришлю тебе твое сообщение')


            # Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
            # кроме команд "/start" и "/help"
            @dp.message()
            async def send_echo(message: Message):
                await message.reply(text=message.text)


            if __name__ == '__main__':
                dp.run_polling(bot)
            offset = result['update_id']
            do_something()

    end_time = time.time()
    print(f'Время между запросами к Telegram Bot API: {end_time - start_time}')