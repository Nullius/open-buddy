from data_layer import new_user, create_users

data = [
  {
    'uid': 0,
    'name': 'Гомер',
    'surname': 'Симпсон',
    'position': 'Оператор',
    'phone': '111-111-1',
    'username': 'OpenBuddyBot',
    'active': 1,
    'email': '0@open.ru',
  },
  {
    'uid': 1,
    'name': 'мистер',
    'surname': 'Бернс',
    'position': 'Босс',
    'phone': '111-111-2',
    'username': 'OpenBuddyBot',
    'active': 1,
    'email': '1@open.ru',
  },
  {
    'uid': 2,
    'name': 'Сеймур',
    'surname': 'Скиннер',
    'position': 'Учитель',
    'phone': '111-111-3',
    'username': 'OpenBuddyBot',
    'active': 1,
    'email': '2@open.ru',
  },
  {
    'uid': 3,
    'name': 'Барт',
    'surname': 'Симпсон',
    'position': 'Ученик',
    'phone': '111-111-4',
    'username': 'OpenBuddyBot',
    'active': 1,
    'email': '3@open.ru',
  },
  {
    'uid': 4,
    'name': 'Барни',
    'surname': 'Гамбл',
    'position': 'Собутыльник',
    'phone': '111-111-5',
    'username': 'OpenBuddyBot',
    'active': 1,
    'email': '4@open.ru',
  },
  {
    'uid': 5,
    'name': 'Мо',
    'surname': 'Сизлак',
    'position': 'Бармен',
    'phone': '111-111-6',
    'username': 'OpenBuddyBot',
    'active': 1,
    'email': '5@open.ru',
  },
  {
    'uid': 6,
    'name': 'Мардж',
    'surname': 'Симпсон',
    'position': 'Домохозяйка',
    'phone': '111-111-7',
    'username': 'OpenBuddyBot',
    'active': 1,
    'email': '6@open.ru',
  },
]

if __name__ == '__main__':
  create_users()
  for user in data:
    new_user(user)