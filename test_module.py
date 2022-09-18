
from Servo import Servo

servo1 = Servo();
servo2 = Servo();
servo3 = Servo();
servo4 = Servo();
servo5 = Servo();

servo1.attach(14);
servo2.attach(15);
servo3.attach(18);
servo4.attach(23);
servo5.attach(24);
servo1.start()
servo2.start()
servo3.start()
servo4.start()
servo5.start()

#servo1.write(30)
servo2.write(90)
servo3.write(90)
servo4.write(90)
servo5.write(90)

servo1.end()
servo2.end()
servo3.end()
servo4.end()
servo5.end()