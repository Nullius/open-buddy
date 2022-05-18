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
      pair_date DATE
    )
    ''')
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

def new_user(data):
  print(data)
  try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''INSERT INTO users
      (uid, name, surname, position, phone, username, active, pair_count)
      VALUES (:uid, :name, :surname, :position, :phone, :username, :active, 0)
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
    cur.execute('''SELECT uid, name, surname, username, phone
      FROM users
      WHERE active = 1
      ORDER BY
        pair_date DESC,
        pair_count DESC
    ''')
    result = cur.fetchall()
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()
    return result

def write_pair(uid1, uid2):
  update_date_query = 'UPDATE users SET pair_date = date() WHERE uid = ?'
  try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(update_date_query, (uid1,))
    cur.execute(update_date_query, (uid2,))
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()