import RPi.GPIO as GPIO
import I2C_LCD_driver
from time import sleep
import time
import requests
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(24,GPIO.OUT) #GPIO24 as Red LED
GPIO.setup(25,GPIO.OUT) #GPIO25 as Trig
GPIO.setup(27,GPIO.IN) #GPIO27 as Echo

# telegram bot setup
Token ='6384012630:AAFV2fktz9DGpoam4bvVnOrBElM3l6aftNU'
chat_id='1403383287'
message = 'Someone walked past the sensor'
doorbell = 'Someone pressed the doorbell'

# Token = "6738451332:AAGo1Z2erYUyAxc_rieq-Fvc2nQae1zXROI"
# chat_id = "952883191"
# message = "Movement detected"

# setting up keypad
MATRIX=[ [1,2,3],
         [4,5,6],
         [7,8,9],
         ['*',0,'#']] #layout of keys on keypad
ROW=[6,20,19,13] #row pins
COL=[12,5,16] #column pins

#set column pins as outputs, and write default value of 1 to each
for i in range(3):
    GPIO.setup(COL[i],GPIO.OUT)
    GPIO.output(COL[i],1)

#set row pins as inputs, with pull up
for j in range(4):
    GPIO.setup(ROW[j],GPIO.IN,pull_up_down=GPIO.PUD_UP)

#lcd setup
LCD = I2C_LCD_driver.lcd()
LCD.backlight(1)

#defining password
password = "111111"
entered = ""

# alert function
def alert(x):
    for i in range(0,x):
        GPIO.output(24,1)
        sleep(0.1)
        GPIO.output(24,0)
        sleep(0.1)

#define a function called distance below:
def distance():
    #produce a 10us pulse at Trig
    GPIO.output(25,1) 
    time.sleep(0.00001)
    GPIO.output(25,0)

    #measure pulse width (i.e. time of flight) at Echo
    StartTime=time.time()
    StopTime=time.time()
    while GPIO.input(27)==0:
        StartTime=time.time() #capture start of high pulse       
    while GPIO.input(27)==1:
        StopTime=time.time() #capture end of high pulse
    ElapsedTime=StopTime-StartTime

    #compute distance in cm, from time of flight
    Distance=(ElapsedTime*34300)/2
       #distance=time*speed of ultrasound,
       #/2 because to & fro
    return Distance

# main code
def keypad_scan():
    # scanning keypad
    global entered
    for i in range(3): #loop through all columns
        LCD.lcd_display_string("Enter password:",1)
        GPIO.output(COL[i],0) #pull one column pin low
        for j in range(4): #check which row pin becomes low
            if GPIO.input(ROW[j])==0: #if a key is pressed
                pressed = MATRIX[j][i]
                entered = entered + str(pressed)
                LCD.lcd_display_string(str(entered),2)
                print (MATRIX[j][i]) #print the key pressed
                while GPIO.input(ROW[j])==0: #debounce
                    sleep(0.1)
        GPIO.output(COL[i],1) #write back default value of 1

        if len(entered) == 6:
            if entered == password:
                LCD.lcd_display_string("Success",2)
                print("entry success")
                sleep(0.4)
                LCD.lcd_clear()
            else:
                print("entry denied")
                LCD.lcd_display_string("Denied",2)
                alert(2)
                LCD.lcd_clear()

            #reset entered keys for next attempt
            entered = ""
    
        if (entered) == "*":
            LCD.lcd_display_string("Doorbell",2)
            print("Doorbell pressed")
            url = f"https://api.telegram.org./bot{Token}/sendMessage?chat_id={chat_id}&text={doorbell}"
            print(requests.get(url).json())
            sleep(0.4)
            LCD.lcd_clear()
            entered = ""

        
    
def ultrasound_scan():
    print("Measured distance = {0:0.1f} cm".format(distance()))
    sleep(0.3)
    
    if distance() < 50 :
        url = f"https://api.telegram.org./bot{Token}/sendMessage?chat_id={chat_id}&text={message}"
        print(requests.get(url).json())


while (True):
    # create threads
    thread1 = threading.Thread(target=keypad_scan)
    thread2 = threading.Thread(target=ultrasound_scan)

    # start threads
    thread1.start()
    thread2.start()

    # wait until both threads finish
    thread1.join()
    thread2.join()
