import os
import sys
import logging

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

import new_buddy

load_dotenv()
bot_token = os.getenv("BUDDY_TOKEN")
if not bot_token:
    sys.exit("Error: no token")


bot = Bot(token=bot_token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Test", "new_buddy"]
    keyboard.add(*buttons)
    await message.answer("Push me", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Test")
async def test_handler(message: types.Message):
    await message.reply("Pushed")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)