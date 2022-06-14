import sqlite3
from sqlite3 import Error

db_name = 'buddy.db'

def create_connection():
  conn = None
  try:
    conn = sqlite3.connect(db_name)
  except Error as e:
    print(e)
  return conn

def create_users():
  try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE if NOT EXISTS users (
      id INTEGER PRIMARY KEY,
      uid INTEGER UNIQUE NOT NULL,
      name TEXT NOT NULL,
      surname TEXT NOT NULL,
      position TEXT NOT NULL,
      phone TEXT NOT NULL,
      username TEXT NOT NULL,
      active BOOLEAN NOT NULL,
      pair_count INTEGER NOT NULL,
      pair_date DATE,
      email TEXT NOT NULL
    )
    ''')
    conn.commit()
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()

def create_feedback():
  try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE if NOT EXISTS feedback (
      id INTEGER PRIMARY KEY,
      uid INTEGER NOT NULL,
      date DATE NOT NULL,
      feedback_status
    )
    ''')
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()

FEEDBACK_GOOD = 1
FEEDBACK_BAD = 2
FEEDBACK_NO_REPLY = 3
def send_feedback(uid, feedback_status):
  try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''INSERT INTO feedback
      (uid, date, feedback_status)
      VALUES (?, date(), ?)
      ''', (uid, feedback_status)
    )
    conn.commit()
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()

def create_buddies():
  try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE if NOT EXISTS buddies (
      uid1 INTEGER,
      uid2 INTEGER,
      date TEXT)
    ''')
    conn.commit()
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()

def get_buddies(uid):
  try: 
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''SELECT DISTINCT uid2 FROM buddies WHERE uid1=?''', (uid,))
    result = cur.fetchall()
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()
  return [uid for result[0] in result]

def new_user(data):
  print(data)
  try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''INSERT INTO users
      (uid, name, surname, position, phone, username, active, pair_count, email)
      VALUES (:uid, :name, :surname, :position, :phone, :username, :active, 0, :email)
      ''', data)
    conn.commit()
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()

def get_users():
  result = None
  try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''SELECT uid, name, surname, username, phone, email, position
      FROM users
      WHERE active = 1
      ORDER BY
        pair_date ASC,
        pair_count ASC 
    ''')
    result = cur.fetchall()
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()
    return result

def write_pair(uid1, uid2):
  update_date_query = 'UPDATE users SET pair_date = date(), pair_count = pair_count + 1 WHERE uid = ?'
  insert_buddy_query = 'INSERT INTO buddies (uid1, uid2) VALUES(?, ?)'
  try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(update_date_query, (uid1,))
    cur.execute(update_date_query, (uid2,))
    cur.execute(insert_buddy_query, (uid1, uid2))
    cur.execute(insert_buddy_query, (uid2, uid1))
    conn.commit()
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()

def set_active(uid, isActive):
  query ='UPDATE users SET active = ? WHERE uid = ?';
  try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(query, (isActive, uid))
    conn.commit()
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()