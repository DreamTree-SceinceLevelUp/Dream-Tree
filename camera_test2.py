from picamera2 import *
import time

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

preview_config = picam2.preview_configuration
capture_config = picam2.still_configuration
picam2.configure(preview_config)

picam2.start()

time.sleep(2)
for i in range(10):
    picam2.switch_mode_and_capture_file(capture_config, f"./img/{i}.jpg")
    time.sleep(1)