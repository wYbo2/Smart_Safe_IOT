from PIL import Image
from io import BytesIO
import requests
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(5)
camera.capture('/home/pi/Desktop/IoTe/Training_Kit/testproject/image2.jpg')
camera.stop_preview

TOKEN = "6738451332:AAGo1Z2erYUyAxc_rieq-Fvc2nQae1zXROI"
chat_id = "952883191"
# Sending text message is easy:
message = "Sending a Telegram message from Python code..."
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
print (requests.get(url).json()) # this sends the message
#Sending a picture is slightly more involved:
img = Image.open(r"/home/pi/Desktop/IoTe/Training_Kit/testproject/image2.jpg")
# Convert the image to a binarystream
image_stream = BytesIO()
img.save(image_stream, format='PNG')
image_stream.seek (0)

# Send the image as a binary stream
url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
files = {'photo': ('image.png', image_stream)}
data = {'chat_id': chat_id}
print (requests.post(url, files=files, data=data).json())



