import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
leds=[16,20,21,25,26,17,27,22]
GPIO.setup(leds,GPIO.OUT)
GPIO.output(leds,0) #погасили все
dynamic_range=3.3 #переменная динамик рэнджь
def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
        print("Устанавлниваем 0.0 В")
        return 0
    return int(voltage / dynamic_range * 255)

def number_to_dac(number):
    GPIO.output(leds, [int(element) for element in bin(number)[2:].zfill(8)])
    print([int(element) for element in bin(number)[2:].zfill(8)])

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)


        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")
finally:
    GPIO.output(leds, 0)
    GPIO.cleanup()