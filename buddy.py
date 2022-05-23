import os
import sys
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv

from data_layer import new_user, create_buddies, create_users, create_feedback
import replies

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
  buttons = ["Что это?", "Как это работает?", "Какие результаты?", "Давай начнем!"]
  keyboard.add(*buttons)
  await message.answer(replies.start, reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Что это?")
async def what_is_this(message: types.Message):
  # bot.send_photo(chat_id=message.chat.id, photo=open('static/what-is-this.png', 'rb'))
  await message.answer_photo(open('static/what-is-this.png', 'rb'))
  await message.answer("Послушай это :)")
  await message.answer_audio(open('static/sample.mp3', 'rb'))

@dp.message_handler(lambda message: message.text == "Как это работает?")
async def how_this_works(message: types.Message):
  await message.answer(replies.how_this_works)

@dp.message_handler(lambda message: message.text == "Какие результаты?")
async def what_results(message: types.Message):
  await message.answer(replies.what_results)
  await message.answer_video(open('static/sample.mkv', 'rb'))

class Buddy(StatesGroup):
  email = State()
  name = State()
  surname = State()
  position = State()
  phone = State()

# Registration entry point
@dp.message_handler(commands='new_buddy')
@dp.message_handler(lambda message: message.text == 'Давай начнем!')
async def name_start(message: types.Message):
  await Buddy.email.set()
  await message.answer("Ваш e-mail:", reply_markup=types.ReplyKeyboardRemove())

'''
@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
  current_state = await state.get_state()
  if current_state is None:
    return
  
  # await state.finish()
  await message.answer('Отменено', reply_markup=types.ReplyKeyboardRemove())
  await Buddy.previous()

def cancel_button():
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  buttons = ["\cancel",]
  keyboard.add(*buttons)
  return keyboard
'''

@dp.message_handler(state=Buddy.email)
async def process_email(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['email'] = message.text

  await Buddy.next()
  await message.answer('Ваше имя:', reply_markup=cancel_button())

@dp.message_handler(state=Buddy.name)
async def process_name(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['name'] = message.text

  await Buddy.next()
  await message.answer("Ваша фамилия:")

@dp.message_handler(state=Buddy.surname)
async def process_surname(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['surname'] = message.text

  await Buddy.next()
  await message.answer("Ваша должность:")

@dp.message_handler(state=Buddy.position)
async def process_position(message: types.Message, state=FSMContext):
  await Buddy.next()
  await state.update_data(position=message.text)
  await message.answer("Ваш телефон:")

@dp.message_handler(state=Buddy.phone)
async def process_phone(message: types.Message, state=FSMContext):
  async with state.proxy() as data:
    data['phone'] = message.text
    data['uid'] = message.chat.id
    data['active'] = True
    data['username'] = message.chat.username
    new_user(dict(data))

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Встреча прошла круто!", "Встреча прошла не очень", "Бадди не отвечает :(("]
    keyboard.add(*buttons)
    await bot.send_message(
      message.chat.id,
      replies.finish,
      reply_markup=keyboard
    )
    await state.finish()

async def send_message(uid, message):
  await bot.send_message(
    uid,
    message
  )

if __name__ == '__main__':
    create_users()
    create_buddies()
    create_feedback()
    executor.start_polling(dp, skip_updates=True)
