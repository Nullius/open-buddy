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
      uid INTEGER PRIMARY KEY,
      name TEXT,
      surname TEXT,
      position TEXT,
      phone TEXT,
      username TEXT,
      active BOOLEAN)
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
      VALUES (:uid, :name, :surname, :position, :phone, :active, :username)
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
    cur.execute('''SELECT uid, name, surname, username, phone FROM users WHERE active = 1''')
    result = cur.fetchall()
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()
    return result