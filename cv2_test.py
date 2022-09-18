import cv2
from picamera2 import *


picam2 = Picamera2()
#picam2.start_preview()

preview_config = picam2.preview_configuration
capture_config = picam2.still_configuration
picam2.configure(preview_config())

picam2.start()