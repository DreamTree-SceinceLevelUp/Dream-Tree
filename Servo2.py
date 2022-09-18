import pigpio
from time import sleep


class Servo2():
    def __init__(self):
        self.pi = pigpio.pi()

    def attach(self, pin, theta):
        self.pi.set_servo_pulsewidth(pin, theta*7+560)
        print('active attach')
        
    def temp(self,pin) :
        print(type(self.pi.get_servo_pulsewidth(pin)))

    def write(self, pin, theta):
        theta = int(theta)
        if theta > 270:
            theta = 270
            print('valueError: Theta must be less than 270')
        if theta < 0:
            theta = 0
            print('ValueError: Theta must be more than 0')

        current_theta = self.pi.get_servo_pulsewidth(pin)
        theta = theta*7+560

        if current_theta <= theta:
            for i in range(current_theta, theta+1, 1):
                self.pi.set_servo_pulsewidth(pin, i)
                sleep(0.00085)
        else:
            for i in range(current_theta, theta, -1):
                self.pi.set_servo_pulsewidth(pin, i)
                sleep(0.00085)

        print('active write')


#servo = Servo2()
#servo.attach(15,110)
#servo.write(15,50)
