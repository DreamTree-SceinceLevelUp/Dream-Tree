import pigpio
from time import sleep

class Servo() :
    def __init__(self) :
        self.pi = pigpio.pi()
        
    def attach(self, pin,theta) :
        self.pi.set_servo_pulsewidth(pin,0)
        self.pi.set_servo_pulsewidth(pin,theta*7+560)
        print('active attach')
        
    def write(self,pin,theta) :
        if theta>270 :
            theta = 270
            print('valueError: Theta must be less than 270')
        if theta <0 :
            theta = 0
            print('ValueError: Theta must be more than 0')
        self.pi.set_servo_pulsewidth(pin,theta*7+560)
        print('active write')
        
        
#servo = Servo()
#servo.attach(14,0)
#servo.write(14,180)