import pigpio
from time import sleep

pi = pigpio.pi()
#while True :
pi.set_servo_pulsewidth(14,0)
sleep(1)
pi.set_servo_pulsewidth(14,560)
sleep(0.2)
pi.set_servo_pulsewidth(14,560+90*7)
sleep(1)
#pi.set_servo_pulsewidth(14,2450)
    
