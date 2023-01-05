
import time
import logging

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(filename="logging.log", level=logging.INFO)

TOKEN = ""
MSG = "Поиграем в крестики-нолики?\nИгрок1 ходит X, Игрок2 ходит 0\n"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
user_id = ""


check_list = list(range(1, 10))
list1 = list(range(1, 10))


def win(list):
    if list[0] == list[1] == list[2] or \
            list[3] == list[4] == list[5] or \
            list[6] == list[7] == list[8] or \
            list[0] == list[3] == list[6] or \
            list[1] == list[4] == list[7] or \
            list[2] == list[5] == list[8] or \
            list[1] == list[4] == list[8] or \
            list[2] == list[4] == list[6]:
        return 1


def draw(list):
    if list == []:
        return 1


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    global user_id
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_name = message.from_user.first_name
    logging.info(f"{user_id=} {user_full_name=} , {time.asctime()} ")
    await message.reply(f"Привет, {user_full_name}")

    await bot.send_message(user_id, MSG.format(user_name))
    global check_list
    global list1
    check_list = list(range(1, 10))
    list1 = list(range(1, 10))
    await bot.send_message(user_id, f"\n Игровая таблица\n\
      {list1[0]} | {list1[1]} | {list1[2]}\n   ___________\n\
      {list1[3]} | {list1[4]} | {list1[5]}\n   ___________\n\
      {list1[6]} | {list1[7]} | {list1[8]}\n")
    await bot.send_message(user_id, "\n Введите номер поля для X: ")

    @dp.message_handler(lambda message: not message.text.isdigit())
    async def process_invalid(message: types.Message):
        return await message.reply("Введите числа от 1 до 9")

    @dp.message_handler(lambda message: int(message.text) not in check_list)
    async def check_empty(message: types.Message):
        return await message.reply("Такое место уже занято или не в диапазоне от 1 до 9")

    @dp.message_handler(lambda message: int(message.text) in check_list)
    async def check_handler(message: types.Message):
        global user_id
        gamer_turn = int(message.text)
        global check_list
        global list1
        if len(check_list) % 2 != 0:
            turn = "X"
        else:
            turn = "0"

        list1[gamer_turn-1] = turn
        check_list.remove(gamer_turn)

        await bot.send_message(user_id, f"\n Игровая таблица\n\
      {list1[0]} | {list1[1]} | {list1[2]}\n   ___________\n\
      {list1[3]} | {list1[4]} | {list1[5]}\n   ___________\n\
      {list1[6]} | {list1[7]} | {list1[8]}\n")

        if win(list1):
            await bot.send_message(user_id, f"\n Победил Игрок, который ходил {turn}: ")
            await bot.send_message(user_id, "Конец игре")
            check_list = list(range(1, 10))
            list1 = list(range(1, 10))
            await bot.send_message(user_id, "Нажми /start")
        elif draw(list1):
            await bot.send_message(user_id, "\n Ничья")
            await bot.send_message(user_id, "Конец игре")
            check_list = list(range(1, 10))
            list1 = list(range(1, 10))
            await bot.send_message(user_id, "Нажми /start")
        else:
            if len(check_list) % 2 != 0:
                turn = "X"
            else:
                turn = "0"
            await bot.send_message(user_id, f"\n Введите номер поля для {turn}: ")


if __name__ == "__main__":
    executor.start_polling(dp)
