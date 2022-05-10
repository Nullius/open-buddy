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
    cur.execute('''CREATE TABLE users (
      uid INTEGER PRIMARY KEY,
      name TEXT,
      surname TEXT,
      position TEXT,
      phone TEXT,
      active BOOLEAN)
      ''')
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()

def create_buddies():
  try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE buddies (
      uid1 INTEGER,
      uid2 INTEGER,
      date TEXT)
    ''')
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()

def new_user(uid: int, name: str, surname: str, position: str, phone: str):
  try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''INSERT INTO users
      VALUES (?, ?, ?, ?, ?, ?)
      ''', uid, name, surname, position, phone)
  except Error as e:
    print(e)
  finally:
    cur.close()
    conn.close()
