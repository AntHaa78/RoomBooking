import random
import string
import time
import keyboard # Used to simulate sensors (without raspberry pi)
import threading
import sqlite3
from flask import Flask, render_template, request 
import calendar


#Room reservation
#to improve: better time system reservation. Remove x/y rom inputs



# creation of quick method prRed to print in red in terminal, prGreen green 
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
    
# basic password generator function, only lower case letters, can adjust lentgh.
def password_generator(): 
    length = 5
    letters = string.ascii_lowercase
    result_pw = ''.join(random.choice(letters) for i in range(length))
    return result_pw    
    

def printit(): #used for testing ending on max time case (with minutes for faster test)
  global t
  t=None
  current_time = time.strftime("%M:%S", time.localtime())
  print(f"\nCurrent minute:second : {current_time}")
  t = threading.Timer(10, printit)
  t.start()


def reservation(): # Function to reserve room. Need to implement calendar/more dates choice later. Currently only current month
    
    global data_user
    back = True
    personCount = 0
    time_out = 0   
    early_exit=False
    print_status = True # Boolean variable to be able to print only once when in While loops  
    max_time_out_of_room = 10 # adjust time (in seconds for test, for real use probably minutes) a person can be outside the room while its reserved

    print("\nWelcome to the room reservation system for January")
    name=input("\nEnter your name: ")
    day=(time.localtime())[2]  
    day_formatted = time.strftime("%Y-%m-%d")  
    hour=(time.localtime()).tm_hour
    
    # Testings end case with minutes
    #minute_base = (time.localtime()).tm_min # used for testing end time
    #minute = minute_base
    #print(f"TESTING: Room bookings ends at {hour}:{minute_base+2}")
    #time_out_str=f'{hour}:{minute_base+2}:00'

    day_user=int(input(f"\nEnter the day of the reservation ({day}-31): ")) #only for current day for now (easy testing)
    if day_user==day:
        start_time = int(input(f"\nEnter the start time of the reservation ({hour}-19): "))
    else:
        start_time = int(input(f"\nEnter the start time of the reservation (8-19): "))
    start_time_str=str(start_time)+':00'
    end_time = int(input(f"\nEnter the end time of the reservation ({start_time+1}-20): "))
    end_time_str = str(end_time)+':00'
    time_out_str=f'{end_time}:00' # if timer reaches end, this is end time out of room
    password = password_generator()
    if (hour>=start_time and hour<end_time and day_user==day):
        print(f"\nYour name is {name}, your password will be '{password}', your reservation starts at {start_time} and ends at {end_time}. Work hard!")
    else:
        pass
    print("\n")


    while hour<end_time:
        hour=(time.localtime()).tm_hour
    #while minute < minute_base+2: #used for testing end time
        #minute = (time.localtime()).tm_min # used for testing end time
        time.sleep(0.05) # to avoid permanent loop, was causing issues with the keyboard.is_pressed method

        if (hour>=start_time and day_user==day): # check time compared to reservation
                
                    
                print(f"\nWaiting for 'someone' to show up...")
                
                print_status=False  
      
                while keyboard.is_pressed('y')==False:
                    pass

                time_in_str = time.strftime("%H:%M", time.localtime())             
                answer_name = input("\nWelcome visitor. Enter your name: ")
                answer_password = input("Enter your password: ")
                print("ID check...")
                time.sleep(1)
                    
                while (answer_name!=name or answer_password!=password): # as long as name/pwd incorrect, loop
                    print("Name and/or password inccorect. Try again") 
                    answer_name = input("\nWelcome visitor. Enter your name: ")
                    answer_password = input("Enter your password: ")
                    print("ID check...")
                    

                if (answer_name==name and answer_password==password):
                    print(f"\nWelcome {name} to your booking! It is booked until {end_time} o'clock")
                    max_time_out_of_room = int(input("How long before the reservation cancels if the room is empty? (max 15 secs, default=10): "))
               
                    print_status = True

                    print(f"\n{name} is in the room... ")
                        
                    print_status=False
                    
                    personCount = personCount + 1
                    max_people_in=1

                    print("Sisällä on ",personCount," henkilöä.")
                    while hour<end_time:
                        hour = (time.localtime()).tm_hour
                    #while minute < minute_base+2: #used for testing end time
                        #minute = (time.localtime()).tm_min # used for testing end time                        
                        time.sleep(0.05)
                        if keyboard.is_pressed('y'):
                            personCount+=1
                            if personCount>max_people_in:
                                max_people_in+=1
                            print(f"One more person entered! There are now {personCount} people inside!")
                            time.sleep(0.1)
                            
                        if keyboard.is_pressed('x') and personCount>0:
                            personCount-=1
                            if personCount>1:
                                print(f"A person exited! There are now {personCount} people inside!")
                                time.sleep(0.1)
                                
                            if personCount==1:
                                print(f"Only one persone left!")
                                time.sleep(0.1)
                                
                        if keyboard.is_pressed('x') and personCount==0:
                            prRed(f"\nNo one left in the room! If you're not back within {max_time_out_of_room} seconds, your reservation will be cancelled.")                                                                                 
                            time_out=time.time()
                            time_out_str = time.strftime("%H:%M", time.localtime())                    
                            back = False
                            while (time.time() - time_out) < max_time_out_of_room:
                                if keyboard.is_pressed('y'):
                                    print(f"Welcome back {name}!")
                                    personCount+=1
                                    back = True
                                    break
                            if back == False:
                                break
                                time.sleep(0.02)                        
        if hour == end_time:
        #if minute == minute_base: #test    
            prRed("\nTimer reached. Please exit the room")
            break
                    
        if back == False:
            prRed(f"\nYou took too long to come back {name}! Your reservation is now cancelled.")
            early_exit=True     
            break


        elif print_status: # if hour is not yet reached start time
            print(f"\nNo reservation at {hour} on {day}/12. Next reservation at {start_time} on {day_user}/12")                  
            print_status=False   
            exit    

    #t.cancel() cancel timer on testings
            
    data_user=[(name, day_formatted, start_time_str, end_time_str, max_people_in, time_in_str, time_out_str, early_exit)]        

def print_data():
    print(data_user)

def get_data():
    data = data_user
    return data

def update_db():
    con = sqlite3.connect("Database.db")
    con.execute('''CREATE TABLE IF NOT EXISTS database(
            name TEXT NOT NULL,
            day DATE, 
            StartTime INTEGER, 
            EndTime INTEGER, 
            MaxPeople INTEGER, 
            TimesIn TEXT,
            TimesOut TEXT,
            EarlyExit BOOLEAN)''')
    con.executemany("""INSERT INTO database 
                    VALUES(?,?,?,?,?,?,?,?)""", data_user)
    con.commit()
    con.close()

# random booking generator
def random_booking():
    day = random.choice([date for date in calendar.Calendar().itermonthdates(2024, 1) if date.month == 1])
    starttime = random.randint(8,19)
    starttime_str = str(starttime)+':00'
    endtime = random.randint(1+starttime,20)
    endtime_str = str(endtime)+':00'
    maxpeople = random.randint(1,10)
    hour_in = starttime
    minute_in = random.randint(0,59)
    if minute_in<10:
        timein = f'{hour_in}:0{minute_in}'
    else:
        timein = f'{hour_in}:{minute_in}'
    time_out_minutes = random.randint(hour_in*60+minute_in, endtime*60)
    hour_out, minute_out = divmod(time_out_minutes, 60)
    if minute_out<10:
        timeout = f'{hour_out}:0{minute_out}'
    else:
        timeout = f'{hour_out}:{minute_out}'   
    if timeout==endtime_str:
        earlyexit=False
    else:
       earlyexit=True
    data = (str(day), starttime_str, endtime_str, maxpeople, timein, timeout, earlyexit)
    return data

# create random SQL rownumber-table of datas
def random_bookings(rownumber):
    datas=[]  
    for i in range(1,rownumber+1):
        name = ('test'+str(i),)
        data = random_booking()
        datas.append((name+data))
    con = sqlite3.connect('DatabaseRandom.db') 
    con.execute('DROP TABLE bookings')
    con.execute('''CREATE TABLE bookings(
            name TEXT NOT NULL,
            day DATE, 
            StartTime TEXT, 
            EndTime TEXT, 
            MaxPeople INTEGER, 
            TimesIn TEXT,
            TimesOut TEXT,
            EarlyExit BOOLEAN)''')   
    con.executemany('INSERT INTO bookings (name, day, StartTime, EndTime, MaxPeople, TimesIn, TimesOut, EarlyExit) VALUES (?,?,?,?,?,?,?,?)', datas)
    con.commit()
    con.close()

app = Flask(__name__) 

@app.route('/') 
@app.route('/home') 
def index(): 
	return render_template('index.html') 

@app.route('/bookings') 
def bookings(): 
	connect = sqlite3.connect('Database.db') 
	cursor = connect.cursor() 
	cursor.execute('SELECT * FROM database') 

	data = cursor.fetchall() 
	return render_template("bookings.html", data=data) 

@app.route('/addbooking', methods=['GET', 'POST'])
def addbooking(): 
	if request.method == 'POST': 
		name = request.form['name'] 
		day = request.form['day'] 
		starttime = request.form['starttime'] 
		endtime = request.form['endtime'] 
		maxpeople = request.form['maxpeople']
		timein = request.form['timein']
		timeout = request.form['timeout']
		earrlyexit = request.form['earlyexit'] 

		with sqlite3.connect("Database.db") as users: 
			cursor = users.cursor() 
			cursor.execute("INSERT INTO database VALUES(?,?,?,?,?,?,?,?)", (name, day, starttime, endtime, maxpeople, timein, timeout, earrlyexit))
			users.commit() 
		return render_template("index.html") 
	else: 
		return render_template('addbooking.html') 

if __name__ == '__main__': 
    prRed("x to simulate inside sensor, y to simulate outside sensor")
    reservation()
    update_db()

    #random_bookings(20)

    #app.run(debug=False) 
