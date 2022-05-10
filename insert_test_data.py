from data_layer import new_user

data = [
  {
    'uid': 0,
    'name': 'Гомер',
    'surname': 'Симпсон',
    'position': 'Оператор',
    'phone': '111-111-1',
    'username': 'OpenBuddyBot',
    'active': 1,
  },
  {
    'uid': 1,
    'name': 'мистер',
    'surname': 'Бернс',
    'position': 'Босс',
    'phone': '111-111-2',
    'username': 'OpenBuddyBot',
    'active': 1,
  },
  {
    'uid': 2,
    'name': 'Сеймур',
    'surname': 'Скиннер',
    'position': 'Учитель',
    'phone': '111-111-3',
    'username': 'OpenBuddyBot',
    'active': 1,
  },
  {
    'uid': 3,
    'name': 'Барт',
    'surname': 'Симпсон',
    'position': 'Ученик',
    'phone': '111-111-4',
    'username': 'OpenBuddyBot',
    'active': 1,
  },
  {
    'uid': 4,
    'name': 'Барни',
    'surname': 'Гамбл',
    'position': 'Собутыльник',
    'phone': '111-111-5',
    'username': 'OpenBuddyBot',
    'active': 1,
  },
  {
    'uid': 5,
    'name': 'Мо',
    'surname': 'Сизлак',
    'position': 'Бармен',
    'phone': '111-111-6',
    'username': 'OpenBuddyBot',
    'active': 1,
  },
  {
    'uid': 6,
    'name': 'Мардж',
    'surname': 'Симпсон',
    'position': 'Домохозяйка',
    'phone': '111-111-7',
    'username': 'OpenBuddyBot',
    'active': 1,
  },
]

if __name__ == '__main__':
  for user in data:
    new_user(user)