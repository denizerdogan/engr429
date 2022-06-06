import RPi.GPIO as GPIO
from time import sleep
servoPIN = 17
def initMotor():
  servoPIN = 17
  GPIO.setup(servoPIN, GPIO.OUT)

  pwm = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
  pwm.start(2.5) # Initialization

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(servoPIN, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(servoPIN, False)
	pwm.ChangeDutyCycle(0)

def pressButton():
  SetAngle(90)
  sleep(0.5)
  SetAngle(0)

