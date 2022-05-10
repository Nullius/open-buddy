from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from __init__ import dp, bot

class Buddy(StatesGroup):
  name = State()
  position = State()
  phone = State()

@dp.message_handler(commands='new_buddy')
async def name_start(message: types.Message):
  await Buddy.name.set()
  await message.answer("Ваше имя и фамилия:")

@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
  current_state = await state.get_state()
  if current_state is None:
    return
  
  # logging.info

  await state.finish()
  await message.reply('Отменено', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=Buddy.name)
async def process_name(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['name'] = message.text

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
    await bot.send_message(
      message.chat.id,
      'Finished!'
    )