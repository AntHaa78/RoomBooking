from datetime import datetime
from datetime import timedelta
import random
import string
import time
import keyboard # Used to simulate sensors (without raspberry pi)
import threading


class Cancelled(Exception): pass


#Room reservation
#to improve: better time system reservation. name only with letters?
# check if any motion at all during the amount of hours selected. Can also be modified later

t=None

# creation of quick method prRed to print in red in terminal, prGreen green 
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

def back_to_menu():
    print("\nExiting ... Going back to menu\n")
    time.sleep(1)

def welcome_back(name):
    print(f"\nWelcome back {name}!")
    #print_status = True
    global out_of_room_before_timer
    out_of_room_before_timer = 1
    
def password_generator(): # basic password generator function, only lower case letters, can adjust lentgh. Used for mode one
    length = 5
    letters = string.ascii_lowercase
    result_pw = ''.join(random.choice(letters) for i in range(length))
    return result_pw        

def printit():
  global t
  print("Awaiting motion...")
  t = threading.Timer(5.0, printit)
  t.start()


def mode_one(): # Function one to reserve room. Need to implement calendar/more dates choice later. Currently only current month
    
    global data_user
    personCount = 0
    time_out = 0   
    early_exit=False
    print_status = True # Boolean variable to be able to print only once when in While loops  
    max_time_out_of_room = 10 # adjust time (in seconds for test, for real use probably minutes) a person can be outside the room while its reserved

    print("\nWelcome to the room reservation system for January")
    name=input("\nEnter your name: ")
    hour=(time.localtime()).tm_hour
    day=(time.localtime())[2]
    minute = (time.localtime()).tm_min # used for testing end time
    day_user=int(input(f"\nEnter the day of the reservation ({day}-31): "))
    #only for current day for now (easy testing)
    if day_user==day:
        start_time = int(input(f"\nEnter the start time of the reservation ({hour}-19): "))
    else:
        start_time = int(input(f"\nEnter the start time of the reservation (8-19): "))
    end_time = int(input(f"\nEnter the end time of the reservation ({start_time+1}-20): "))
    password = password_generator()
    if (hour>=start_time and hour<end_time and day_user==day):
        print(f"\nYour name is {name}, your password will be '{password}', your reservation starts at {start_time} and ends at {end_time}. Work hard!")
    else:
        pass
    print("\n")


    while hour<end_time:
        hour=(time.localtime()).tm_hour
    #while minute < 2: used for testing end time
        #minute = (time.localtime()).tm_min # used for testing end time
        time.sleep(0.05) # to avoid permanent loop, was causing issues with the keyboard.is_pressed method
        #try:
        if (hour>=start_time and day_user==day): # check time compared to reservation
                
                    
                print(f"\nWaiting for 'someone' to show up...")
                
                print_status=False  
      
                while keyboard.is_pressed('y')==False:
                    pass
                #all_time_in=[] 
                #all_time_out = []
                #all_time_in.append(time.strftime("%H:%M:%S", time.localtime()))  
                time_in_str = time.strftime("%H:%M:%S", time.localtime())             
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
                            time_out_str = time.strftime("%H:%M:%S", time.localtime())
                            #test=time.strftime("%H:%M:%S", time.localtime(time_out))
                            #all_time_out.append(time.strftime("%H:%M:%S", time.localtime(time_out)))                    
                            back = False
                            while (time.time() - time_out) < max_time_out_of_room:
                                if keyboard.is_pressed('y'):
                                    print(f"Welcome back {name}!")
                                    #all_time_in.append(time.strftime("%H:%M:%S", time.localtime()))
                                    personCount+=1
                                    back = True
                                    break
                            if back == False:

                                break
                                time.sleep(0.02)                        
        if hour == end_time:
            prRed("\nTimer reached. Please exit the room")
            time_out_str = time.strftime("%H:%M:%S", time.localtime())
            break
                    
        if back == False:
            prRed(f"\nYou took too long to come back {name}! Your reservation is now cancelled.")
            early_exit=True
            break


        #if keyboard.is_pressed("e"): #exit mode alarm
           # print("\nMode ROOM booking exited successfully")
            #break

        elif print_status: # if hour is not yet reached start time
            print(f"\nNo reservation at {hour} on {day}/12. Next reservation at {start_time} on {day_user}/12")      
            print_status=False   
            break    
    
    data_user=[(name, day, start_time, end_time, max_people_in, time_in_str, time_out_str, early_exit)]        

def print_data():
    print(data_user)

def get_data():
    data = data_user
    return data
