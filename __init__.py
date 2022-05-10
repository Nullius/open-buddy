import logging
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token="")

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(["Test"])
    await message.answer("Push me")

@dp.message_handler(lambda message: message.text == "Test")
async def test_handler(message: types.Message):
    await message.reply("Pushed")
