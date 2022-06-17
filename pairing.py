import sys
import asyncio
from aiogram import types
from aiogram.utils.markdown import escape_md
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random

from data_layer import get_users, get_buddies, write_pair
from buddy import send_message
import replies

INVITE = 'Invite to meeting message'
def invite_message(user):
  uid, name, surname, username, phone, email, position = user
  return '''Еху! ❤️🔆🎉

✨ Твой бадди на неделю {} {}, {}

✨ Его контакты {}, {}, {}

✨ Ему тоже пришло уведомление с твоими контактами.

✨ Темы для первого разговора и обязательные ритуалы поддержки [здесь](https://docs.google.com/document/d/13dZHH0m6F6VN42U2ohsSNrsFJl8REzrGGQTGL3iPxWY/edit?usp=sharing) :)


Не жди, напиши своему бадди первым ❤️'''.format(
  name, surname, position,
  escape_md('@{}'.format(username)), phone, email
)

def get_user_by_id (uid, users):
  user = list(filter(lambda user: user[0] == uid, users))
  if len(user) > 0:
    return user[0]
  return None

def periodic(period):
  def scheduler(fcn):
    async def wrapper(*args, **kwargs):
      while True:
        asyncio.create_task(fcn(*args, **kwargs))
        await asyncio.sleep(period)
    return wrapper

  return scheduler

def generate_buddy(user_id, uids):
  old_buddies = get_buddies(user_id)
  new_buddies = [buddy for buddy in uids if buddy not in old_buddies]
  if (len(new_buddies) > 0):
    return random.choice(new_buddies)
  else:
    return random.choice(uids)

async def run_pairing():
  users = get_users()
  print(users)
  uids = [user[0] for user in users]

  if (len(uids) % 2 == 1):
    lone = uids.pop()
    try:
      await send_message(lone, replies.lone_user)
    except:
      print('lone user message can\'t be sent')
    # TODO write to DB (or maybe not)

  while len(uids) > 0:
    print(uids)
    to_pair = uids.pop(0)
    buddy = generate_buddy(to_pair, uids)
    uids.remove(buddy)
    print(to_pair, buddy)
    print(get_user_by_id(to_pair, users), get_user_by_id(buddy, users))
    # TODO write to pair table
    write_pair(to_pair, buddy)
    
    user_to_pair = get_user_by_id(to_pair, users)
    user_buddy = get_user_by_id(buddy, users)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Встреча прошла круто!", "Встреча прошла не очень", "Бадди не отвечает :(("]
    keyboard.add(*buttons)

    try:
      if (user_to_pair[3] != 'OpenBuddyBot'):
        await send_message(to_pair, invite_message(user_buddy), keyboard)
    except e:
      print(e)
    try:
      if (user_buddy[3] != 'OpenBuddyBot'):
        await send_message(buddy, invite_message(user_to_pair), keyboard)
    except e:
      print(e)

'''
@periodic(2)
async def do_something(*args, **kwargs):
    await asyncio.sleep(5)  # Do some heavy calculation
    print(time.time())
'''

if __name__ == '__main__':
  scheduler = AsyncIOScheduler()
  scheduler.add_job(run_pairing, 'interval', days=1)
  scheduler.start()

  try:
    asyncio.get_event_loop().run_forever()
  except (KeyboardInterrupt, SystemExit):
    pass 