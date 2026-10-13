import RPi.GPIO as g

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        
        self.pins =gpio_pin
        g.setmode (g.BCM)
        g.setup (self.pins, g.OUT)
        self.frequency = pwm_frequency
        self.verbose =verbose
        self.dynamic_range=dynamic_range
        self.pwm=g.PWM(self.pins,self.frequency)
        self.pwm.start(0)
        g.setmode (g.BCM)
        g.setup (self.pins, g.OUT)

    def deinit(self):
        self.pwm.ChangeDutyCycle(0)
        self.pwm.stop()
        g.output(self.pins,0)
        g.cleanup()

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
            self.pwm.ChangeDutyCycle(0)
            return 

        duty_cycle=voltage/self.dynamic_range*100
        self.pwm.ChangeDutyCycle(duty_cycle)

        if self.verbose:
            print(f"Напряжение:{voltage:.3f} В -> скважность {duty_cycle:.2f}%")
if __name__ == "__main__":
    dac = PWM_DAC(12, 500, 3.290, True)
    try:
        

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()