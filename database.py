import sqlite3

conn = sqlite3.connect('health.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(

id INTEGER PRIMARY KEY AUTOINCREMENT,

username TEXT,

email TEXT UNIQUE,

password TEXT,

profile_pic TEXT DEFAULT 'default.png',

smoke_streak INTEGER DEFAULT 0,

alcohol_streak INTEGER DEFAULT 0

)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS habits(

id INTEGER PRIMARY KEY AUTOINCREMENT,

user_id INTEGER,

smoking INTEGER,

alcohol INTEGER,

sleep REAL,

exercise INTEGER,

date TEXT

)
''')

conn.commit()

conn.close()

print("Database Ready")