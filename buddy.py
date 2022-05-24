import os
import sys
import logging
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv

import data_layer
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
  await message.answer_audio(open('static/what-it-is.mp3', 'rb'))

@dp.message_handler(lambda message: message.text == "Как это работает?")
async def how_this_works(message: types.Message):
  # await message.answer(replies.how_this_works)
  await message.answer('https://www.youtube.com/watch?v=JGulAZnnTKA')

@dp.message_handler(lambda message: message.text == "Какие результаты?")
async def what_results(message: types.Message):
  await message.answer(replies.what_results)
  await message.answer_video(open('static/open-buddy.mp4', 'rb'))

@dp.message_handler(lambda message: message.text == "Встреча прошла круто!")
async def good_feedback(message: types.Message):
  data_layer.send_feedback(message.chat.id, data_layer.FEEDBACK_GOOD)
  await message.answer(replies.good_feedback, reply_markup=types.ReplyKeyboardRemove)

@dp.message_handler(lambda message: message.text == "Встреча прошла не очень")
async def bad_feedback(message: types.Message):
  data_layer.send_feedback(message.chat.id, data_layer.FEEDBACK_BAD)
  await message.answer(replies.bad_feedback, reply_markup=types.ReplyKeyboardRemove)

@dp.message_handler(lambda message: message.text == "Бадди не отвечает :((")
async def no_reply_feedback(message: types.Message):
  data_layer.send_feedback(message.chat.id, data_layer.FEEDBACK_NO_REPLY)
  await message.answer(replies.bad_feedback, reply_markup=types.ReplyKeyboardRemove)

class Buddy(StatesGroup):
  email = State()
  name = State()
  surname = State()
  position = State()
  phone = State()

@dp.message_handler(lambda message: message.text == "Отменить регистрацию", state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
  current_state = await state.get_state()
  if current_state is None:
    return
  
  await state.finish()
  await message.answer('Регистрация отменена', reply_markup=types.ReplyKeyboardRemove())

def cancel_button():
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  buttons = ["Отменить регистрацию",]
  keyboard.add(*buttons)
  return keyboard

# Registration entry point
@dp.message_handler(lambda message: message.text == 'Давай начнем!')
async def registration_start(message: types.Message):
  await Buddy.email.set()
  await message.answer("Ваш e-mail:", reply_markup=cancel_button())

@dp.message_handler(state=Buddy.email)
async def process_email(message: types.Message, state: FSMContext):
  pattern = re.compile('^.+@open\.ru$', flags=re.I)
  if (not pattern.match(message.text)):
    await Buddy.email.set()
    await message.answer("Бот предназначен только для сотрудников банка «Открытие». Пожалуйста введите ваш рабочий e-mail.")
  else:
    async with state.proxy() as data:
      data['email'] = message.text

    await Buddy.next()
    await message.answer('Ваше имя:')

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
    data_layer.new_user(dict(data))

    await bot.send_message(
      message.chat.id,
      replies.finish,
      reply_markup=types.ReplyKeyboardRemove()
    )
    await state.finish()

async def send_message(uid, message, keyboard=None):
  await bot.send_message(
    uid,
    message,
    reply_markup=keyboard 
  )

if __name__ == '__main__':
    data_layer.create_users()
    data_layer.create_buddies()
    data_layer.create_feedback()
    executor.start_polling(dp, skip_updates=True)
