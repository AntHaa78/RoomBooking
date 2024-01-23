from modes import *
import sqlite3

print("x to simulate inside sensor, y to simulate outside sensor")

mode_one()
print_data()

data = get_data()

# SQLite part
con = sqlite3.connect("Database.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS database(
            name TEXT NOT NULL,
            day INTEGER, 
            StartTime INTEGER, 
            EndTime INTEGER, 
            MaxPeople INTEGER, 
            TimesIn,
            TimesOut,
            EarlyExit BOOLEAN)""")


cur.executemany("INSERT INTO database VALUES(?,?,?,?,?,?,?,?)", data)
con.commit()

res = cur.execute("SELECT rowid, name, StartTime FROM database")
print(res.fetchall())

con.close()