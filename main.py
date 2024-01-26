from modes import *
import sqlite3

prRed("x to simulate inside sensor, y to simulate outside sensor")

mode_one()
print_data()

data = get_data()

# SQLite part
con = sqlite3.connect("Database.db")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS database(
            name TEXT NOT NULL,
            day INTEGER, 
            StartTime INTEGER, 
            EndTime INTEGER, 
            MaxPeople INTEGER, 
            TimesIn TEXT,
            TimesOut TEXT,
            EarlyExit BOOLEAN)''')

#datatest = [("test1", 26, 12, 13, 3,'14:10:10', '14:22:23', True)]


cur.executemany("INSERT INTO database VALUES(?,?,?,?,?,?,?,?)", data)
con.commit()

res = cur.execute("SELECT rowid, name, StartTime FROM database")
print(res.fetchall())

con.close()
