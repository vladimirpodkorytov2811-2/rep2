import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
leds=[16,12,25,17,27,23,22,24]
GPIO.setup(leds,GPIO.OUT)
GPIO.output(leds,0) #погасили все
button_up=9 #настроим вход то есть кнопки
GPIO.setup(button_up,GPIO.IN)
button_down=10
GPIO.setup(button_down,GPIO.IN)
#настройка кнопок завершена
num=0
def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

sleep_time=0.2
while True:
    if GPIO.input(button_up):
        num=num+1
        if num==256:
            num=0
        print(num,dec2bin(num))
        time.sleep(sleep_time)
    if GPIO.input(button_down):
        num=num-1
        if num==-1:
            num=255
        print(num,dec2bin(num))
        time.sleep(sleep_time)
    
    
    GPIO.output(leds, dec2bin(num))
