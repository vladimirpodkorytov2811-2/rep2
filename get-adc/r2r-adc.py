import RPi.GPIO as GPIO
import time
comparator=21
GPIO.setmode(GPIO.BCM)
GPIO.setup(comparator,GPIO.IN)
class R2R_ADC:
    def __init__(self, dynamic_range,compare_time=0.01 , verbose = False):
        self.dynamic_range =dynamic_range
        self.compare_time = compare_time
        self.verbose =verbose

        self.bits_gpio =[26,20,19,16,13,12,25,11]
        self.comp_gpio=21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio,GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)


    def deinit(self):
        GPIO.output(self.bits_gpio,0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        binary =[int(element)for element in (bin(number)[2:].zfill(8))]
        print(binary)
        for i in range(8):
            GPIO.output(self.bits_gpio[i], binary[i])

    # def set_voltage(self, voltage):
    #     self.set_number(int(voltage/self.delta* 255))
    def sequential_counting_adc(self):
        numZ=0
        while(numZ<256):
            self.number_to_dac(numZ)
            time.sleep(0.01)
            numZ=numZ+1
        return(numZ)

if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.0)

        while True:
            print(adc.sequential_counting_adc())
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Was stopped by keyboard\n")
    else:
        print("No exceptions")


    finally:
        adc.deinit()
