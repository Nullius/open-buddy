import asyncio
import random

from data_layer import get_users
from buddy import send_message

INVITE = 'Invite to meeting message'
def invite_message(user):
  uid, name, surname, username, phone = user
  return 'Твой бадди на две недели {} {} @{} {}. Ему тоже пришло уведомление с твоими контактами'.format(
    name, surname, username, phone
  )

def get_user_by_id (uid, users):
  user = list(filter(lambda user: user[0] == uid, users))
  if len(user) > 0:
    return user[0]
  return None

if __name__ == '__main__':
  users = get_users()
  print(users)
  uids = [user[0] for user in users]

  if (len(uids) % 2 == 1):
    lone = uids.pop()
    # TODO write to DB

  while len(uids) > 0:
    print(uids)
    to_pair = uids.pop(0)
    buddy = random.choice(uids)
    uids.remove(buddy)
    print(to_pair, buddy)
    print(get_user_by_id(to_pair, users), get_user_by_id(buddy, users))
    # TODO write to DB
    
    user_to_pair = get_user_by_id(to_pair, users)
    user_buddy = get_user_by_id(buddy, users)

    if (user_to_pair[3] != 'OpenBuddyBot'):
      asyncio.run(send_message(to_pair, invite_message(to_pair)))
    if (user_buddy[3] != 'OpenBuddyBot'):
      asyncio.run(send_message(buddy, invite_message(to_pair)))