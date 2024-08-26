from flask import Flask
from flask import render_template

import spidev
my_spi=spidev.SpiDev()
my_spi.open(0,0)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT)

app = Flask(__name__)

def read_ADC():
    my_spi.max_speed_hz = 1350000
    r=my_spi.xfer2([1, 0b10000000, 0])
    result = ((r[1]&3)<<8)+r[2]
    return result

@app.route('/')
def index():
    return render_template("index2.html")

@app.route('/page2')
def page2():
    return "Second Page"

@app.route('/hello/<who>')
def hello(who):
    return render_template("greet.html", name=who)

@app.route('/LED_is_OFF')
def show_LED_is_OFF():
    pot_value=str(read_ADC())
    GPIO.output(24,0)
    return render_template("LED_is_OFF.html", value=pot_value)

@app.route('/LED_is_ON')
def show_LED_is_ON():
    pot_value = str(read_ADC())
    GPIO.output(24,1)
    return render_template("LED_is_ON.html", value=pot_value)



if __name__=="__main__":
    app.run(debug=True, host='127.0.0.2')
