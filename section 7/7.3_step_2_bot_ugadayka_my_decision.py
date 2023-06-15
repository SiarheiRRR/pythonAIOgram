from os import getenv
import random
from random import randint
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
API_TOKEN: str = getenv('API_TOKEN')


class Session:
    def __init__(self, set_num_try: int = 5, curr_num_try: int = 0,
                 is_game_started: bool = False, win_counter: int = 0, loose_counter: int = 0):
        self.__number = self.random_number()
        self.__set_num_try = set_num_try
        self.__is_game_started = is_game_started
        self.__curr_num_try = curr_num_try
        self.__win_counter = win_counter
        self.__loose_counter = loose_counter

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        self.__number = value

    @property
    def set_num_try(self):
        return self.__set_num_try

    @set_num_try.setter
    def set_num_try(self, value):
        self.__set_num_try = value

    @property
    def is_game_started(self):
        return self.__is_game_started

    @is_game_started.setter
    def is_game_started(self, value):
        self.__is_game_started = value

    @property
    def curr_num_try(self):
        return self.__curr_num_try

    @curr_num_try.setter
    def curr_num_try(self, value):
        self.__curr_num_try = value

    @property
    def win_counter(self):
        return self.__win_counter

    @win_counter.setter
    def win_counter(self, value):
        self.__win_counter = value

    @property
    def loose_counter(self):
        return self.__loose_counter

    @loose_counter.setter
    def loose_counter(self, value):
        self.__loose_counter = value

    def session_finalyze(self, win_ind: bool = True) -> None:
        self.is_game_started = False
        self.curr_num_try = 0
        self.number = self.random_number()
        if win_ind:
            self.win_counter += 1
        else:
            self.loose_counter += 1

    @staticmethod
    def random_number():
        return randint(1, 100)


bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()
session = Session()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('''Привет!\nМеня зовут бот "Угадай число"! Если хочешь узнать правила игры - набери /help.
Введи /yes что бы играть или /no что бы отказаться''')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        f'''Бот загадывает число от 0 до 100. Твоя задача угадать это число за {session.set_num_try} попыток''')


@dp.message(Command(commands=["yes"]))
async def process_yes_command(message: Message):
    if session.is_game_started:
        await message.answer(
            '''Игра уже началась, вводите число от 0 до 100, либо /cancel если хотите прекратить игру.''')
    else:
        session.is_game_started = True
        await message.answer(
            '''Итак, игра началась! Вводите число от 0 до 100, либо /cancel если хотите прекратить игру.''')


@dp.message(Command(commands=["no"]))
async def process_yes_command(message: Message):
    if session.is_game_started:
        await message.answer(
            '''Игра уже началась, вводите число от 0 до 100, либо /cancel если хотите прекратить игру.''')
    else:
        await message.answer('''Ок, если всё же захотите сыграть - наберите /yes''')


@dp.message(Command(commands=["cancel"]))
async def process_cancel_command(message: Message):
    if session.is_game_started:
        session.session_finalyze(False)
        await message.answer(
            '''Вы отказались от поединка, а следовательно проиграли. Если хотите сыграть еще раз введите /yes''')


@dp.message(Command(commands=["stat"]))
async def process_cancel_command(message: Message):
    if not session.is_game_started:
        await message.answer(
            f'''Статистика вашей игровой сессии следующая:
Количество ваших побед: {session.win_counter}
Количество поражений: {session.loose_counter}''')
    else:
        await message.answer(f'''Закончите текущую игру и потом сможете запросить статистику''')


@dp.message(lambda x: x.text and x.text.isdigit() and 0 <= int(x.text) <= 100)
async def process_nums_command(message: Message):
    if not session.is_game_started:
        await message.answer('''Игра не запущена. 
Если хотите сыграть - введите /yes
Если хотите просмотреть статистику ваших побед/поражений введите /stat''')
        return
    session.curr_num_try += 1
    if session.number == int(message.text):
        session.session_finalyze()
        await message.answer('''Поздравляю! Вы победили. 
Если хотите сыграть еще раз введите /yes
Если хотите просмотреть статистику ваших побед/поражений введите /stat''')
    elif session.curr_num_try == session.set_num_try:
        await message.answer(f'''К сожалению, Вы проиграли. Загаданное число было равно {session.number}.
Если хотите сыграть еще раз введите /yes
Если хотите просмотреть статистику ваших побед/поражений введите /stat''')
        session.session_finalyze(False)
    elif session.number < int(message.text):
        await message.answer(f'''Загаданное число меньше введенного тобой!{session.number} {session.curr_num_try}''')
    else:
        await message.answer(f'''Загаданное число больше введенного тобой!{session.number} {session.curr_num_try}''')


@dp.message()
async def other_messages(message: Message):
    await message.answer('''Вы ввели неизвестное мне значение. Если вы не знаете что делать введите /help''')


if __name__ == '__main__':
    dp.run_polling(bot)
