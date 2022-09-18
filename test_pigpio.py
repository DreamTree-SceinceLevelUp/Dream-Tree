import pigpio
from time import sleep

pi = pigpio.pi()
#while True :
pi.set_servo_pulsewidth(23,0)
sleep(1)
pi.set_servo_pulsewidth(23,560)
sleep(1)
pi.set_servo_pulsewidth(23,560+90*7)
sleep(1)
pi.set_servo_pulsewidth(23,2450)
    
    