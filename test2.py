import Adafruit_DHT
import time
from time import sleep
import RPi.GPIO as GPIO #import RPi.GPIO module
import csv

GPIO.setmode(GPIO.BCM) #choose BCM mode
GPIO.setwarnings(False)
GPIO.setup(22,GPIO.IN)
GPIO.setup(26,GPIO.OUT) #set GPIO 26 as output
sensor = Adafruit_DHT.AM2302
pin = 21 #GPIO 4 or pin 7
n = 0
PWM=GPIO.PWM(26,50) #set 50Hz PWM output at GPIO26


if GPIO.input(22):
        
    PWM.start(3) #3% duty cycle
    print('duty cycle:', 3) #3 o'clock position
    sleep(4) #allow time for movement
    PWM.start(12) #13% duty cycle
    print('duty cycle:', 12) #9 o'clock position
    sleep(4) #allow time for movement
    n_time = time.strftime("%H")+':'+time.strftime("%M")+':'+time.strftime("%S")
    n_date = time.strftime("%d")+'-'+time.strftime("%m")+'-'+time.strftime("%Y")
    data_row = ["fish has been fed at " + n_time + " on " + n_date] #prepare a row of data

    # Open csv file and append the row of data
    with open('feederdata.txt','a') as csvfile:
        data_file = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        data_file.writerow(data_row)

else:
    print('Failed to get reading. Try again!')
    time.sleep(2)



    
