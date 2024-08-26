import RPi.GPIO as GPIO
import I2C_LCD_driver
from time import sleep
import time
import requests
import threading
from PIL import Image
from io import BytesIO
from picamera import PiCamera
import math, random

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT) #GPIO18 as Doorbell
GPIO.setup(24,GPIO.OUT) #GPIO24 as Red LED
GPIO.setup(25,GPIO.OUT) #GPIO25 as Trig
GPIO.setup(26,GPIO.OUT) #GPIO26 as Motor
PWM=GPIO.PWM(26,50) #set 50Hz PWM output at GPIO26
GPIO.setup(27,GPIO.IN) #GPIO27 as Echo
# telegram bot setup
Token ='6384012630:AAFV2fktz9DGpoam4bvVnOrBElM3l6aftNU'
chat_id='1403383287'
message = 'No movement detected in a long period of time'
doorbell = 'Doorbell pressed'

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

#defining variable
password = "111111"
entered = ""
otp_password = ""
count = 0

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
            if (entered == password or entered == otp_password):
                LCD.lcd_display_string("Success",2)
                print("entry success")
                PWM.start(3) #13% duty cycle
                print('duty cycle:', 3) #3 o'clock position
                sleep(4) #allow time for movement
                PWM.start(12) #13% duty cycle
                print('duty cycle:', 12) #9 o'clock position
                sleep(4) #allow time for movement
                PWM.start(3) #13% duty cycle
                print('duty cycle:', 3) #9 o'clock position
                sleep(4) #allow time for movement
                PWM.stop() #stop the motor
                
                LCD.lcd_clear()

                
            else:
                print("entry denied")
                LCD.lcd_display_string("Denied",2)
                alert(2)
                LCD.lcd_clear()

            #reset entered keys for next attempt
            entered = ""
    
        if (entered) == "*":
            LCD.lcd_display_string("Doorbell", 2)
            print("Doorbell pressed")
            GPIO.output(18,1) #output logic high/'1'
            sleep(0.5) #delay 1 second
            GPIO.output(18,0) #output logic low/'0'
            # clear lcd, reset entered keys for next attempt
            LCD.lcd_clear()
            entered = ""

            #take photo and save
            camera = PiCamera()
            camera.start_preview()
            sleep(2)
            camera.capture('/home/pi/Desktop/IoTe/Training_Kit/testproject/image2.jpg')
            camera.stop_preview()
            camera.close()

            #send tele message
            img = Image.open(r"/home/pi/Desktop/IoTe/Training_Kit/testproject/image2.jpg")
            image_stream = BytesIO()
            img.save(image_stream, format='PNG')
            image_stream.seek (0)
            url = f"https://api.telegram.org/bot{Token}/sendPhoto"
            files = {'photo': ('image.png', image_stream)}
            data = {'chat_id': chat_id}
            print (requests.post(url, files=files, data=data).json())
    
def ultrasound_scan():
    print("Measured distance = {0:0.1f} cm".format(distance()))
    sleep(0.25)

    if distance() > 50 :
        global count
        count+= 1
        if count>10:
            url = f"https://api.telegram.org./bot{Token}/sendMessage?chat_id={chat_id}&text={message}"
            print(requests.get(url).json())
            count = 0

    else:
        count = 0

def generateOTP():
    digits = "0123456789"
    OTP = ""

    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP
    

last_update_id = 0
activate_ultrasound = True

def message_check():
    global last_update_id, otp_password, activate_ultrasound
    url = f"https://api.telegram.org/bot{Token}/getUpdates?offset={last_update_id + 1}"
    response = requests.get(url).json()

    # check each update for new messages
    for update in response['result']:
        message = update['message']
        chat_id = message['chat']['id']
        text = message['text']

        # if the message is "request code", send a response
        if text.lower() == "request code":
            otp_password = generateOTP()
            response_text = ("Code requested" + otp_password)
            url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={chat_id}&text={response_text}"
            requests.get(url)
        if text.lower() == "stop":
            activate_ultrasound = False
        elif text.lower() == "start":
            activate_ultrasound = True

        # update the last_update_id to the current update's id
        last_update_id = update['update_id']

while True:
    # create threads
    thread1 = threading.Thread(target=keypad_scan)
    thread3 = threading.Thread(target=message_check)

    # start threads
    thread1.start()
    thread3.start()

    if activate_ultrasound:
        thread2 = threading.Thread(target=ultrasound_scan)
        thread2.start()
        thread2.join()

    # wait for threads to finish
    thread1.join()
    thread3.join()
