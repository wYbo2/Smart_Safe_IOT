import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


import spidev #import SPI library
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import I2C_LCD_driver #import the library

# Your email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'detectorfire36@gmail.com'  # Replace with your email address
EMAIL_PASSWORD = 'herpmenhpmtdbrog'       # Replace with your email password

# Set up GPIO, DHT11 instance, and SPI
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
instance = dht11.DHT11(pin=21)  # read data using pin 21
spi=spidev.SpiDev() #create SPI object
spi.open(0,0) #open SPI port 0, device (CS) 0
GPIO.setup(18, GPIO.OUT)  # set GPIO 18 as output
GPIO.setup(24,GPIO.OUT) #set GPIO 24 as output
GPIO.setup(23,GPIO.OUT) #set GPIO 23 as output
GPIO.setup(17,GPIO.IN) # set GPIO 17 as input
PIR_state=0 #use this, so that only a change in state is reported

buzzer_pwm = GPIO.PWM(18, 100)  # set 100Hz PWM output at GPIO 18
LCD = I2C_LCD_driver.lcd() #instantiate an lcd object, call it LCD

LCD.backlight(0)

# Your email sending functions
def send_email(subject, message):
    sender_email = EMAIL_ADDRESS
    sender_password = EMAIL_PASSWORD
    recipient_email = "stk15915@gmail.com"  # Replace with recipient's email address

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", str(e))


def send_followup_email(subject, message):
    sender_email = EMAIL_ADDRESS
    sender_password = EMAIL_PASSWORD
    recipient_email = "stk15915@gmail.com"  # Replace with recipient's email address

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Follow-up email sent successfully")
    except Exception as e:
        print("Error sending follow-up email:", str(e))



def readadc(adcnum):
    #read SPI data from the MCP3008, 8 channels in total
    if adcnum>7 or adcnum<0:
        return -1
    spi.max_speed_hz = 1350000
    r=spi.xfer2([1,8+adcnum<<4,0])
        #construct list of 3 items, before sending to ADC:
        #1(start), (single-ended+channel#) shifted left 4 bits, 0(stop)
        #see MCP3008 datasheet for details
    data=((r[1]&3)<<8)+r[2]
        #ADD first byte with 3 or 0b00000011 - masking operation
        #shift result left by 8 bits
        #OR result with second byte, to get 10-bit ADC result
    return data

try:
    email_sent = False
    followup_email_sent = False
    last_email_time = None
    
    while True:  # keep reading, unless the keyboard is pressed
        result = instance.read()
        LDR_value=readadc(0) #read ADC channel 0 i.e. LDR
        print("LDR = ", LDR_value) #print result
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)

            if result.temperature > 26 or LDR_value > 950 :
                if not email_sent:
                    email_subject = "Fire Detected!"
                    email_message = "Fire has been detected in your location. Please reply to confirm receipt."
                    send_email(email_subject, email_message)
                    email_sent = True
                    last_email_time = time.time()
                
                else:
                    print ("email sent alr")

                LCD.lcd_clear() #clear the display
                buzzer_pwm.start(50)  # Start the buzzer with 50% duty cycle
                GPIO.output(24,1) #output logic high/'1'
                GPIO.output(23,1) #output logic low/'0'
                LCD.backlight(1) #turn backlight on
                LCD.lcd_display_string("Fire Detected", 1,2) #write on line 1
                LCD.lcd_display_string("Temp %-3.1f C" % result.temperature, 2, 2) #write on line 2
                if GPIO.input(17): #read a HIGH i.e. motion is detected
                    if PIR_state==0:
                        print('detected HIGH i.e. motion detected')
                        PIR_state=1
                else: #read a LOW i.e. no motion is detected
                    if PIR_state==1:
                        print('detected LOW i.e. no motion detected')
                        PIR_state=0

                
            else:
                email_sent = False
                LCD.backlight(0)
                LCD.lcd_clear() #clear the display
                buzzer_pwm.stop()  # Stop the buzzer
                GPIO.output(24,0) #output logic high/'1'
                GPIO.output(23,0) #output logic low/'0'
                #LCD.backlight(1) #turn backlight on
                #LCD.lcd_display_string("No Fire Detected", 1) #write on line 1
                #LCD.lcd_display_string("Temperature"+result.temperature, 2, 2) #write on line 2

        time.sleep(0.5)  # short delay between reads

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()

