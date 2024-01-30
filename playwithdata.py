import sqlite3

#1) From Database, how many bookings reached the end time?
""" con = sqlite3.connect('Database.db')
res = con.execute("SELECT name From bookings WHERE EarlyExit=False")
A = res.fetchall()
print(f"There were {len(A)} bookings that reached the end")
con.close() """

#2) From DatabaseRandom, how many bookings happened on the 18th of january?

con = sqlite3.connect('DatabaseRandom.db')
res = con.execute("SELECT rowid FROM bookings WHERE day = '2024-01-18'")
print(res.fetchall())
A = res.fetchall()
print(f"There were {len(A)} bookings on the 18th of January")
con.close()
