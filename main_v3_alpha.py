import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

import qdarktheme

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np

from IPython import display

from time import sleep
import time

# from Servo import Servo

from Servo2 import Servo2
from dc import dcMotor
from picamera2 import *

from datetime import datetime

from Imu_i2c import IMU

# servo = Servo()
servo = Servo2()
s1 = 14
s2 = 15
s3 = 18
s4 = 23
s5 = 24
servo.attach(s1, 110)
servo.attach(s2, 110)
servo.attach(s3, 110)
servo.attach(s4, 110)
servo.attach(s5, 140)

dream1 = dcMotor(11, 5)
dream2 = dcMotor(13, 6)
dream3 = dcMotor(19, 26)

ee1 = dcMotor(21, 20)
ee2 = dcMotor(16, 12)
ee3 = dcMotor(8, 7)


form_class = uic.loadUiType("debug.ui")[0]

pos = np.array([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], dtype=float)
r = np.array([14, 11.5, 11.7, 19])  # tail ee Tr Dream
w = np.array([0.97, 0.8, 0.3, 0.68])
theta = np.array([0, 0, 0, 0, 0, 3.14/2, 0], dtype=float)  # 0 ~ pi
theta_sum = np.array([0, 0, 0, 0, 0], dtype=float)  # 0 ~ pi

num_motion = 20


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DreamTree ControlGUI')
        self.setupUi(self)

        self.imu = IMU()

        self.fixed_angle = True  # True : first angle / False : last angle

        self.horizontalSlider_1.valueChanged.connect(
            self.showHorizontalSlider_1_Value)
        self.horizontalSlider_2.valueChanged.connect(
            self.showHorizontalSlider_2_Value)
        self.horizontalSlider_3.valueChanged.connect(
            self.showHorizontalSlider_3_Value)
        self.horizontalSlider_4.valueChanged.connect(
            self.showHorizontalSlider_4_Value)
        self.horizontalSlider_5.valueChanged.connect(
            self.showHorizontalSlider_5_Value)

        for i in range(num_motion):
            self.listWidget.addItem(f"motion {i+1}")

        self.motion.clicked.connect(self.setMotion)

        self.single_capture.clicked.connect(self.single_capture_camera)
        # self.continuos_capture.toggled.connect(self.continuos_capture_camera)

        self.mesure.clicked.connect(self.get_imu_value)

        self.pushButton_4.clicked.connect(self.file_open)

        self.video_start.clicked.connect(self.video_rec_start)
        self.video_stop.clicked.connect(self.video_rec_stop)

        self.dream_dc.clicked.connect(self.dreamState)
        self.dream_dc_state = 0

        self.ee_dc.clicked.connect(self.eeState)
        self.ee_dc_state = 0

        # self.fasten.toggled.connect()
        # self.sample.toggled.connect()

        self.canvas = FigureCanvas(Figure(figsize=(4, 3)))
        self.main.addWidget(self.canvas)

        self.ax = self.canvas.figure.subplots()
        self.ax.set_xlim([-100, 100])
        self.ax.set_ylim([-100, 100])
        self.ax.set_aspect('equal', adjustable='box')

        self.canvas2 = FigureCanvas(Figure(figsize=(4, 3)))
        self.graph.addWidget(self.canvas2)

        self.ax2 = self.canvas2.figure.subplots()
        self.ax2.set_facecolor('#E6E6E6')
        self.ax2.set_axisbelow(True)
        self.ax2.grid(color='white', linestyle='solid')

        for spine in self.ax2.spines.values():
            spine.set_visible(False)
        self.ax2.xaxis.tick_bottom()
        self.ax2.yaxis.tick_left()

        self.ax2.tick_params(colors='gray', direction='out')

        # for tick in self.ax2.get_xticklabels():
        #     tick.set_color('gray')
        # for tick in self.ax2.get_yticklabels():
        #     tick.set_color('gray')

        #self.ax2.set_xlim([-6, 6])
        self.ax2.set_ylim([0, 80])

        self.set_theta(0, 0)
        self.set_theta(1, 0)
        self.set_theta(2, 0)
        self.set_theta(3, 0)
        self.set_theta(4, 0)

        self.img_file_view = QPixmap()
        self.img_file_view_label = QLabel()
        self.img_file_view_label.setPixmap(self.img_file_view)

        self.camera.addWidget(self.img_file_view_label)

        self.img_live_view = QPixmap()
        self.img_live_view_label = QLabel()
        self.img_live_view_label.setPixmap(self.img_live_view)

        self.picam2 = Picamera2()

        self.preview_config = self.picam2.preview_configuration
        self.capture_config = self.picam2.still_configuration
        self.picam2.configure(self.preview_config)

        self.video_config = self.picam2.video_configuration
        self.picam2.configure(self.video_config)
        self.encoder = encoders.H264Encoder(10000000)

        self.picam2.start()

        self.draw()
    def dreamState(self) :
        if self.dream_dc_state == 0:
            self.dream_dc_state = 1
            self.dreamMotor(1)
        elif self.dream_dc_state == 1:
            self.dream_dc_state = -1
            self.dreamMotor(-1)
        elif self.dream_dc_state == -1:
            self.dream_dc_state = 0
            self.dreamMotor(0)

    def eeState(self) :        
        if self.ee_dc_state == 0:
            self.ee_dc_state = 1
            self.eeMotor(1)
        elif self.ee_dc_state == 1:
            self.ee_dc_state = -1
            self.eeMotor(-1)
        elif self.ee_dc_state == -1:
            self.ee_dc_state = 0
            self.eeMotor(0)

    def dreamMotor(self,direction):
        """_summary_
            1 -> right
            0 -> stop
            -1 -> left

        Args:
            direction (int): -1,0,1 
        """
        if direction == 1:
            dream1.forward(1)
            dream2.forward(1)
            dream3.forward(1)
            
        elif direction == 0:
            dream1.stop()
            dream2.stop()
            dream3.stop()
        
        elif direction == -1:
            dream1.backward(1)
            dream2.backward(1)
            dream3.backward(1)
        
    def eeMotor(self,direction):
        """_summary_
            1 -> right
            0 -> stop
            -1 -> left

        Args:
            direction (int): -1,0,1 
        """
        if direction == 1:
            ee1.forward(1)
            ee2.forward(1)
            ee3.forward(1)
            
        elif direction == 0:
            ee1.stop()
            ee2.stop()
            ee3.stop()
        
        elif direction == -1:
            ee1.backward(1)
            ee2.backward(1)
            ee3.backward(1)
        
    def get_imu_value(self):
        imu_data = self.imu.getValue()
        print(imu_data)
        imu_data = np.array(imu_data)*980665
        print(imu_data)
        acc_total = (imu_data[3]**2+imu_data[4]**2+imu_data[5]**2)**(1/2)
        self.AccTable.setItem(0, 0, QTableWidgetItem(str(round(imu_data[3]))))
        self.AccTable.setItem(0, 1, QTableWidgetItem(str(round(imu_data[4]))))
        self.AccTable.setItem(0, 2, QTableWidgetItem(str(round(imu_data[5]))))
        self.AccTable.setItem(0, 3, QTableWidgetItem(str(round(acc_total))))

    def video_rec_start(self):
        self.picam2.stop()

        self.video_start.setStyleSheet("background-color: red")
        self.video_stop.setStyleSheet("background-color: red")
        now = str(time.strftime("%Y%m%d%H%M%S"))
        self.output = outputs.FfmpegOutput(f'{now}.mp4')
        self.picam2.start_recording(self.encoder, self.output)

    def video_rec_stop(self):
        self.video_start.setStyleSheet("background-color: none")
        self.video_stop.setStyleSheet("background-color: none")
        self.picam2.stop_recording()

    def file_open(self):
        filename = QFileDialog.getOpenFileName(self, 'Choose image')
        print(filename[0])
        self.img_file_view.load(filename[0])
        self.img_file_view_label.setPixmap(self.img_file_view)
        self.img_file_view_label.setScaledContents(True)
        self.img.addWidget(self.img_file_view_label)

    def single_capture_camera(self):
        now = str(time.strftime("%Y%m%d%H%M%S"))
        self.picam2.switch_mode_and_capture_file(
            self.capture_config, f"./img/{now}.jpg")
        self.img_live_view.load(f"./img/{now}.jpg")
        self.img_live_view_label.setPixmap(self.img_live_view)
        self.img_live_view_label.setScaledContents(True)
        self.camera.addWidget(self.img_live_view_label)

    def continuos_capture_camera(self, state):
        print(state)
        self.continuos_capture.setStyleSheet(
            "background-color: %s" % ({True: "yellow", False: "green"}[state]))
        self.single_capture.setDisabled(state)
        self.single_capture.setEnabled(not state)
        while state:
            self.single_capture_camera()
            sleep(2)

    def draw_node(self, x1, y1, x2, y2):
        self.ax.plot([-x1, -x2], [y1, y2])
        self.ax.scatter([-x1, -x2], [y1, y2])

    def draw(self):
        # self.ax = self.canvas.figure.subplots()
        self.ax.cla()
        self.ax.set_xlim([-100, 100])
        self.ax.set_ylim([-100, 100])
        self.ax.set_aspect('equal', adjustable='box')

        # print(self.fixed_angle)
        print("draw!")
        if self.fixed_angle:

            pos[1] = pos[0] + r[0] * \
                np.array([np.cos(theta[5]), np.sin(theta[5])], dtype=float)
            pos[2] = pos[1] + r[1] * \
                np.array([np.cos(theta[5] + theta[1]),
                         np.sin(theta[5] + theta[1])], dtype=float)
            pos[3] = pos[2] + r[2] * np.array([np.cos(theta[5] + theta[1] + theta[2]), np.sin(
                theta[5] + theta[1] + theta[2])], dtype=float)
            pos[4] = pos[3] + r[3] * np.array([np.cos(theta[5] + theta[1] + theta[2] + theta[3]), np.sin(
                theta[5] + theta[1] + theta[2] + theta[3])], dtype=float)
            theta[6] = np.pi + (theta[5] + theta[1] + theta[2] + theta[3])

        else:

            pos[3] = pos[4] + r[3] * \
                np.array([np.cos(theta[6]), np.sin(theta[6])], dtype=float)
            pos[2] = pos[3] + r[2] * \
                np.array([np.cos(theta[6] - theta[3]),
                         np.sin(theta[6] - theta[3])], dtype=float)
            pos[1] = pos[2] + r[1] * np.array([np.cos(theta[6] - (
                theta[3] + theta[2])), np.sin(theta[6] - (theta[3] + theta[2]))], dtype=float)
            pos[0] = pos[1] + r[0] * np.array([np.cos(theta[6] - (theta[3] + theta[2] + theta[1])), np.sin(
                theta[6] - (theta[3] + theta[2] + theta[1]))], dtype=float)
            theta[5] = (theta[6] - (theta[1] + theta[2] + theta[3])) - np.pi
        
        
        # if self.fixed_angle:
        #     for i in [0, 1, 2, 3]:
        #         theta_sum[i] = np.sum(theta[1:i+1]) + 3.14/2

        #     for i in [1, 2, 3, 4]:
        #         # pos[i] = pos[i-1] + r * np.array( [np.cos( np.sum(theta[:i])), np.sin(np.sum(theta[:i]))], dtype=float )
        #         pos[i] = pos[i-1] + r[i-1] * \
        #             np.array([np.cos(theta_sum[i-1]),
        #                      np.sin(theta_sum[i-1])], dtype=float)
        # else:
        #     for i in [2, 1, 0]:
        #         theta_sum[i] = theta_sum[i+1] - theta[i+1]

        #     for i in [3, 2, 1, 0]:
        #         pos[i] = pos[i+1] - r[i] * \
        #             np.array([np.cos(theta_sum[i]), np.sin(
        #                 theta_sum[i])], dtype=float)


        for i in [0, 1, 2, 3]:
            self.draw_node(pos[i][0], pos[i][1], pos[i+1][0], pos[i+1][1])
        # print('draw')

        self.ax2.cla()
        #self.ax2.set_xlim([-6, 6])
        self.ax2.set_ylim([0, 80])
        torque = [0, 0, 0]
        torque_data = [0, 0, 0, 0, 0, 0]
        torque_data = self.calc_torque()
        if self.fixed_angle:
            torque = torque_data[:3]
        else:
            temp = torque_data[3:]
            torque = [temp[2], temp[1], temp[0]]
        bars = self.ax2.bar(['dream', 'tr', 'ee'],
                            torque, color=['#F2DC5D', '#B3CDD1', '#FCBFB7'], width=0.5)
        for bar in bars:
            height = bar.get_height()
            self.ax2.text(bar.get_x()+bar.get_width()/2.0, height,
                          '%.1f' % height, ha='center', va='bottom', size=12)
        # ['#F2DC5D','#B3CDD1','#FCBFB7']
        self.ax2.set_title('Torque graph', fontsize=15)
        self.ax2.set_ylabel('kg*cm', fontsize=13)
        self.ax2.legend(handles=bars, labels=['dream', 'tr', 'ee'])

        self.canvas.draw()
        self.canvas2.draw()

    def showHorizontalSlider_1_Value(self):
        self.set_theta(0, float(self.horizontalSlider_1.value()))
        self.draw()
        servo.write(s1, float(self.horizontalSlider_1.value())+90+20)

    def showHorizontalSlider_2_Value(self):
        self.set_theta(1, float(self.horizontalSlider_2.value()))
        self.draw()
        servo.write(s2, float(self.horizontalSlider_2.value())+90+20)

    def showHorizontalSlider_3_Value(self):
        self.set_theta(2, float(self.horizontalSlider_3.value()))
        self.draw()
        servo.write(s3, -float(self.horizontalSlider_3.value())+90+20)

    def showHorizontalSlider_4_Value(self):
        self.set_theta(3, float(self.horizontalSlider_4.value()))
        self.draw()
        servo.write(s4, float(self.horizontalSlider_4.value())+90+20)

    def showHorizontalSlider_5_Value(self):
        self.set_theta(4, float(self.horizontalSlider_5.value()))
        self.draw()
        servo.write(s5, float(self.horizontalSlider_5.value())+90+20)

    def set_theta(self, num, deg):
        theta[num] = np.radians(deg)
        if num == 0:
            # servo.write(s1, deg+90+20)
            self.label_1.setText(f"{deg}")
            self.horizontalSlider_1.setValue(int(deg))
        if num == 1:
            # servo.write(s2, deg+90+20)
            self.label_2.setText(f"{deg}")
            self.horizontalSlider_2.setValue(int(deg))
        if num == 2:
            # servo.write(s3, -deg+90+20)
            self.label_3.setText(f"{deg}")
            self.horizontalSlider_3.setValue(int(deg))
        if num == 3:
            # servo.write(s4, deg+90+20)
            self.label_4.setText(f"{deg}")
            self.horizontalSlider_4.setValue(int(deg))
        if num == 4:
            # servo.write(s5, deg+90+20)
            self.label_5.setText(f"{deg}")
            self.horizontalSlider_5.setValue(int(deg))

    def motion1_set(self) :
        self.fixState(True)
        self.set_theta(0, 0)
        self.set_theta(1, 0)
        self.set_theta(2, 0)
        self.set_theta(3, 0)
        self.set_theta(4, 0)

    def motion2_set(self):
        self.fixState(True)
        self.set_theta(2-1,-30)
        self.set_theta(3-1,-30)
        self.set_theta(2-1,-60)
        self.set_theta(3-1,-60)
        self.set_theta(4-1,-15)
        self.set_theta(2-1,-70)
        self.dreamMotor(1)
        self.set_theta(4-1,-70)

    def motion3_set(self):
        self.dreamMotor(0)
        self.fixState(False)
        # self.set_theta(1, -65)
        # self.set_theta(2,-90)
        # self.set_theta(3,-25)
        # self.set_theta(1,-85)
        # self.set_theta(3,90)
        # self.set_theta(2,34)
        # self.set_theta(1,46)
    
    def motion4_set(self):
        self.set_theta(3, 0)
        self.draw()

    def motion5_set(self):
        self.set_theta(2, 90)
        self.draw()

    def motion6_set(self):
        self.set_theta(1, 45)
        self.draw()

    def motion7_set(self):
        self.set_theta(3, 45)
        self.draw()

    def motion8_set(self):
        self.set_theta(3, 90)
        self.draw()

    def motion9_set(self):
        self.set_theta(1, 0)
        self.draw()

    def motion10_set(self):
        self.set_theta(2, -90)
        self.draw()

    def motion11_set(self):
        self.set_theta(3, -45)
        self.draw()

    def motion12_set(self):
        self.set_theta(1, -45)
        self.draw()

    def setMotion(self):
        index = self.listWidget.currentRow()+1
        if index == 1:
            self.motion1_set()
        elif index == 2:
            self.motion2_set()
        elif index == 3:
            self.motion3_set()
        elif index == 4:
            self.motion4_set()
        elif index == 5:
            self.motion5_set()
        elif index == 6:
            self.motion6_set()
        elif index == 7:
            self.motion7_set()
        elif index == 8:
            self.motion8_set()
        elif index == 9:
            self.motion9_set()
        elif index == 10:
            self.motion10_set()
        elif index == 11:
            self.motion11_set()
        elif index == 12:
            self.motion12_set()
        else:
            print("Undefined")

    # def slot_toggle(self, state):
    #     self.fix.setStyleSheet("background-color: %s" %
    #                            ({True: "green", False: "red"}[state]))
    #     self.fix.setText({True: "first fixed", False: "last  ankle"}[state])
    #     self.fixed_angle = state
    #     self.draw()
    def fixState(self,state) :
        self.fixed_angle = state
        self.draw()
    
    def p2p_distant(self, x1, x2, y1, y2):
        return abs(x2-x1)

    def calc_torque(self):
        mid_pos = [0, 0, 0, 0]
        for idx in [0, 1, 2, 3]:
            mid_pos[idx] = (pos[idx] + pos[idx+1]) / 2

        tq1_temp = 0
        tq2_temp = 0
        tq3_temp = 0
        tq4_temp = 0
        tq5_temp = 0
        tq6_temp = 0

        tq5_temp = w[3] * self.p2p_distant(*mid_pos[3], *pos[3])
        tq6_temp = w[0] * self.p2p_distant(*mid_pos[0], *pos[1])

        tq3_temp = w[3] * self.p2p_distant(*mid_pos[3], *pos[2]) + \
            w[2] * self.p2p_distant(*mid_pos[2], *pos[2])
        tq4_temp = w[0] * self.p2p_distant(*mid_pos[0], *pos[2]) + \
            w[1] * self.p2p_distant(*mid_pos[1], *pos[2])

        tq1_temp = w[3] * self.p2p_distant(*mid_pos[3], *pos[1]) + w[2] * self.p2p_distant(
            *mid_pos[2], *pos[1]) + w[1] * self.p2p_distant(*mid_pos[1], *pos[1])
        tq2_temp = w[0] * self.p2p_distant(*mid_pos[0], *pos[3]) + w[1] * self.p2p_distant(
            *mid_pos[1], *pos[3]) + w[2] * self.p2p_distant(*mid_pos[2], *pos[3])

        return [tq1_temp, tq3_temp, tq5_temp, tq2_temp, tq4_temp, tq6_temp]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarktheme.load_stylesheet("light"))

    myWindow = WindowClass()

    myWindow.show()
    app.exec_()
