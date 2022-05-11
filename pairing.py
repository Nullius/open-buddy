import random

from data_layer import get_users
from buddy import send_message

INVITE = 'Invite to meeting message'

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
    # TODO send message
    # TODO write to DB

  while len(uids) > 0:
    print(uids)
    to_pair = uids.pop(0)
    buddy = random.choice(uids)
    uids.remove(buddy)
    print(to_pair, buddy)
    print(get_user_by_id(to_pair, users), get_user_by_id(buddy, users))
    # TODO send message
    # TODO write to DB
    send_message(to_pair, INVITE)
    send_message(buddy, INVITE)