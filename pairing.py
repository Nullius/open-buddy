import random

from data_layer import get_users

if __name__ == '__main__':
  users = get_users()
  print(users)
  uids = [user[0] for user in users]

  if (len(uids) % 2 == 1):
    lone = uids.pop()
    # TODO send message

  while len(uids) > 0:
    print(uids)
    to_pair = uids.pop(0)
    buddy = random.choice(uids)
    uids.remove(buddy)
    print(to_pair, buddy)