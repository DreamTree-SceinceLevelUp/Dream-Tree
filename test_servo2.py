import RPi.GPIO as GPIO
import time

servo = 18
hz = 50

def etha(etha) :
    return 0.52 + 0.0075*etha

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo, GPIO.OUT)

pwm = GPIO.PWM(servo,hz)
pwm.start(0.52/20*100)
time.sleep(2)

#pwm.ChangeDutyCycle(1.15/20*100)
#pwm.ChangeDutyCycle(etha(45)/20*100)
#time.sleep(2)
#pwm.ChangeDutyCycle(etha(180))
#time.sleep(2)
#pwm.ChangeDutyCycle(etha(270))
#time.sleep(2)

#pwm.ChangeDutyCycle(1.78/20*100)
#time.sleep(2)

#0.52+ 0.0075*etha
#pwm.ChangeDutyCycle(1.9/20*100)
#time.sleep(4)

pwm.stop()
GPIO.cleanup()