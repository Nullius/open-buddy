import os
import sys
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv

from data_layer import new_user, create_buddies, create_users

load_dotenv()
bot_token = os.getenv("BUDDY_TOKEN")
if not bot_token:
    sys.exit("Error: no token")


bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Test", "/new_buddy"]
    keyboard.add(*buttons)
    await message.answer("Push me", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Test")
async def test_handler(message: types.Message):
    await message.reply("Pushed")

class Buddy(StatesGroup):
  name = State()
  surname = State()
  position = State()
  phone = State()

# Registration entry point
@dp.message_handler(commands='new_buddy')
async def name_start(message: types.Message):
  await Buddy.name.set()
  await message.answer("Ваше имя:", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
  current_state = await state.get_state()
  if current_state is None:
    return
  
  await state.finish()
  await message.reply('Отменено', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=Buddy.name)
async def process_name(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['name'] = message.text

  await Buddy.next()
  await message.reply("Ваша фамилия:")

@dp.message_handler(state=Buddy.surname)
async def process_surname(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['surname'] = message.text

  await Buddy.next()
  await message.reply("Ваша должность:")

@dp.message_handler(state=Buddy.position)
async def process_position(message: types.Message, state=FSMContext):
  await Buddy.next()
  await state.update_data(position=message.text)
  await message.reply("Ваш телефон:")

@dp.message_handler(state=Buddy.phone)
async def process_phone(message: types.Message, state=FSMContext):
  async with state.proxy() as data:
    data['phone'] = message.text
    data['uid'] = message.chat.id
    data['active'] = True
    new_user(data)
    await bot.send_message(
      message.chat.id,
      'Finished!'
    )
    await state.finish()

if __name__ == '__main__':
    create_users()
    create_buddies()
    executor.start_polling(dp, skip_updates=True)