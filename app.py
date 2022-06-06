import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from time import sleep
import Adafruit_DHT

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   23 : {'name' : 'Living Room', 'state' : GPIO.LOW},
   24 : {'name' : 'Kitchen', 'state' : GPIO.LOW}
   }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

servoPIN = 17
GPIO.setup(servoPIN, GPIO.OUT)

pwm = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
pwm.start(0) # Initialization


 
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4



def SetAngle(angle):
   try:
      duty = angle / 18 + 2
      GPIO.output(servoPIN, True)
      pwm.ChangeDutyCycle(duty)
      sleep(1)
      GPIO.output(servoPIN, False)
      pwm.ChangeDutyCycle(0)

   except KeyboardInterrupt:
      pwm.stop()
      GPIO.cleanup()

def pressButton():
  SetAngle(90)
  sleep(0.5)
  SetAngle(0)


@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

   templateData = {
      'pins' : pins,
      'temperature': temperature,
      'humidity': humidity
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)

   # If the action part of the URL is "on," execute the code indented below:
   if changePin < 25:
         # Get the device name for the pin being changed:
      deviceName = pins[changePin]['name']
      if action == "on":
         # Set the pin high:
         GPIO.output(changePin, GPIO.HIGH)
         # Save the status message to be passed into the template:
         message = "Turned " + deviceName + " on."
      if action == "off":
         GPIO.output(changePin, GPIO.LOW)
         message = "Turned " + deviceName + " off."
   else:
      pressButton()

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins,
      'temperature': temperature,
      'humidity': humidity
      }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
