from gpiozero import Motor
from time import sleep

class dcMotor() :
    def __init__(self,fw,bd) :
        self.motor = Motor(forward=fw,backward=bd)
        self.motor.stop()

    
    def forward(self,speed) :
        self.motor.forward(speed=speed)       
    
    def backward(self,speed) :
        self.motor.backward(speed=speed)

    def stop(self) :
        self.motor.stop()
        
    