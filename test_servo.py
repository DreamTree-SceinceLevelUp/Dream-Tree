from gpiozero import Servo, Device, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

print("tesrt")

#Device.pin_factory = PiGPIOFactory(host='127.0.0.1')
#Device.pin_factory = PiGPIOFactory(host='10.138.26.159')
Device.pin_factory = PiGPIOFactory(host='10.138.27.185')

print("tesrt2")
servo_x = Servo(23, min_pulse_width=500/1000000, max_pulse_width=2500/1000000)
servo_y = Servo(24, min_pulse_width=500/1000000, max_pulse_width=2500/1000000)

while True :
    print('dee')
    servo_x.value = 1
    servo_y.value = 1
    sleep(2)
    
    servo_x.value = -1
    servo_y.value = -1
    sleep(2)