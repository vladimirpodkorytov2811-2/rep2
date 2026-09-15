import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led=26
GPIO.setup(led, GPIO.OUT)
light_detector=6
GPIO.setup(light_detector,GPIO.IN)

state=0

while True:
    state= (GPIO.input(light_detector)==1)
    GPIO.output(led,state)
    time.sleep(0.2)
