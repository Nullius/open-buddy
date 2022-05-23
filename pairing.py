import asyncio
from aiogram import types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random

from data_layer import get_users, write_pair
from buddy import send_message

INVITE = 'Invite to meeting message'
def invite_message(user):
  uid, name, surname, username, phone, email = user
  return 'Твой бадди на две недели {} {} @{} {}. Ему тоже пришло уведомление с твоими контактами'.format(
    name, surname, username, phone
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

def run_pairing():
  users = get_users()
  print(users)
  uids = [user[0] for user in users]

  if (len(uids) % 2 == 1):
    lone = uids.pop()
    # TODO write to DB (or maybe not)

  while len(uids) > 0:
    print(uids)
    to_pair = uids.pop(0)
    buddy = random.choice(uids)
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

    if (user_to_pair[3] != 'OpenBuddyBot'):
      asyncio.run(send_message(to_pair, invite_message(user_buddy)), keyboard)
    if (user_buddy[3] != 'OpenBuddyBot'):
      asyncio.run(send_message(buddy, invite_message(user_to_pair)), keyboard)

'''
@periodic(2)
async def do_something(*args, **kwargs):
    await asyncio.sleep(5)  # Do some heavy calculation
    print(time.time())
'''

if __name__ == '__main__':
  scheduler = AsyncIOScheduler()
  scheduler.add_job(run_pairing, 'interval', minutes=1)
  scheduler.start()

  try:
    asyncio.get_event_loop().run_forever()
  except (KeyboardInterrupt, SystemExit):
    pass 