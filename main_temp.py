import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np

from IPython import display

from time import sleep

# from Servo import Servo

# servo = Servo()
# s1 = 14
# s2 = 15
# s3 = 18
# s4 = 23
# s5 = 24
# servo.attach(s1,110)
# servo.attach(s2,110)
# servo.attach(s3,110)
# servo.attach(s4,110)
# servo.attach(s5,110)

form_class = uic.loadUiType("debug.ui")[0]

pos = np.array([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], dtype=float)

r = np.array([14, 11.5, 11.7, 24.1])
w = np.array([0.97,0.8,0.3,0.68])
theta = np.array([0, 0, 0, 0,0], dtype=float)  # 0 ~ pi
theta_sum = np.array([0, 0, 0, 0,0], dtype=float)  # 0 ~ pi

num_motion = 20


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

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

        self.fix.toggled.connect(self.slot_toggle)

        self.canvas = FigureCanvas(Figure(figsize=(4, 3)))
        self.main.addWidget(self.canvas)

        self.ax = self.canvas.figure.subplots()
        self.ax.set_xlim([-6, 6])
        self.ax.set_ylim([-6, 6])
        self.ax.set_aspect('equal', adjustable='box')

        self.set_theta(0,0)
        self.set_theta(1,0)
        self.set_theta(2,0)
        self.set_theta(3,0)
        self.set_theta(4,0)
        
        self.draw()

    def draw_node(self, x1, y1, x2, y2):
        self.ax.plot([x1, x2], [y1, y2])
        self.ax.scatter([x1, x2], [y1, y2])

    def draw(self):
        # self.ax = self.canvas.figure.subplots()
        self.ax.cla()
        self.ax.set_xlim([-6, 6])
        self.ax.set_ylim([-6, 6])
        self.ax.set_aspect('equal', adjustable='box')

        # print(self.fixed_angle)
        print("draw!")
        if self.fixed_angle:
            for i in [0, 1, 2, 3]:
                theta_sum[i] = np.sum(theta[:i+1])

            for i in [1, 2, 3, 4]:
                # pos[i] = pos[i-1] + r * np.array( [np.cos( np.sum(theta[:i])), np.sin(np.sum(theta[:i]))], dtype=float )
                pos[i] = pos[i-1] + r[i-1] * \
                    np.array([np.cos(theta_sum[i-1]),np.sin(theta_sum[i-1])], dtype=float)
        else:
            for i in [2, 1, 0]:
                theta_sum[i] = theta_sum[i+1] - theta[i+1]

            for i in [3, 2, 1, 0]:
                pos[i] = pos[i+1] - r[i] * \
                    np.array([np.cos(theta_sum[i]), np.sin(theta_sum[i])], dtype=float)

        for i in [0, 1, 2, 3]:
            self.draw_node(pos[i][0], pos[i][1], pos[i+1][0], pos[i+1][1])
        # print('draw')

        self.canvas.draw()

    def showHorizontalSlider_1_Value(self):
        self.set_theta(0,float(self.horizontalSlider_1.value()))
        self.draw()

    def showHorizontalSlider_2_Value(self):
        self.set_theta(1,float(self.horizontalSlider_2.value()))
        self.draw()

    def showHorizontalSlider_3_Value(self):
        self.set_theta(2,float(self.horizontalSlider_3.value()))
        self.draw()

    def showHorizontalSlider_4_Value(self):
        self.set_theta(3,float(self.horizontalSlider_4.value()))
        self.draw()
        
    def showHorizontalSlider_5_Value(self):
        self.set_theta(4,float(self.horizontalSlider_5.value()))
        self.draw()

    def set_theta(self, num, deg):
        theta[num] = np.radians(deg)
        if num == 0:
            # servo.write(s1,deg+90+20)
            self.label_1.setText(f"{deg}")
            self.horizontalSlider_1.setValue(deg)
        if num == 1:
            # servo.write(s2,deg+90+20)
            self.label_2.setText(f"{deg}")
            self.horizontalSlider_2.setValue(deg)
        if num == 2:
            # servo.write(s3,-deg+90+20)
            self.label_3.setText(f"{deg}")
            self.horizontalSlider_3.setValue(deg)
        if num == 3:
            # servo.write(s4,deg+90+20)
            self.label_4.setText(f"{deg}")
            self.horizontalSlider_4.setValue(deg)
        if num == 4:
            # servo.write(s5,deg+90+20)
            self.label_5.setText(f"{deg}")
            self.horizontalSlider_5.setValue(deg)

    def motion1_set(self):
        self.set_theta(0, 90)
        self.set_theta(1, -45)
        self.set_theta(2, -90)
        self.set_theta(3, -45)

    def motion2_set(self):
        self.set_theta(1, -90)
        self.draw()

    def motion3_set(self):
        self.set_theta(3, 0)
        self.draw()

    def motion4_set(self):
        self.set_theta(2, 90)
        self.draw()

    def motion5_set(self):
        self.set_theta(1, 45)
        self.draw()

    def motion6_set(self):
        self.set_theta(3, 45)
        self.draw()

    def motion7_set(self):
        self.set_theta(3, 90)
        self.draw()

    def motion8_set(self):
        self.set_theta(1, 0)
        self.draw()

    def motion9_set(self):
        self.set_theta(2, -90)
        self.draw()

    def motion10_set(self):
        self.set_theta(3, -45)
        self.draw()

    def motion11_set(self):
        self.set_theta(1, -45)
        self.draw()

    def motion12_set(self):
        print(self.theta_torque())
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

    def slot_toggle(self, state):
        self.fix.setStyleSheet("background-color: %s" %
                               ({True: "green", False: "red"}[state]))
        self.fix.setText({True: "first fixed", False: "last  ankle"}[state])
        self.fixed_angle = state
        
    def p2p_distant(self, x1, y1, x2, y2):
        return  ((x1-x2)**2 + (y1-y2)**2)**(1/2)

    def theta_torque(self):
        mid_pos = [0,0,0,0,0]
        for idx in [0,1,2,3]:
            mid_pos[idx] = (pos[idx] + pos[idx+1]) / 2
        
        print(mid_pos)

        tq1_temp = 0
        tq2_temp = 0
        tq3_temp = 0
        tq4_temp = 0
        tq5_temp = 0
        tq6_temp = 0
        
        tq5_temp = w[3] * self.p2p_distant(*mid_pos[3], *pos[1])
        tq6_temp = w[0] * self.p2p_distant(*mid_pos[0], *pos[3])
        
        tq3_temp = tq5_temp + w[2] * self.p2p_distant(*mid_pos[2], *pos[1])
        tq4_temp = tq6_temp + w[1] * self.p2p_distant(*mid_pos[1], *pos[3])
        
        tq1_temp = tq3_temp + w[1] * self.p2p_distant(*mid_pos[1], *pos[1])
        tq2_temp = tq4_temp + w[2] * self.p2p_distant(*mid_pos[2], *pos[3])
        
        return [tq1_temp, tq2_temp, tq3_temp, tq4_temp, tq5_temp, tq6_temp]


if __name__ == "__main__":
    app = QApplication(sys.argv)

    myWindow = WindowClass()

    myWindow.show()
    app.exec_()
    # servo1.end()
    # servo2.end()
    # servo3.end()
    # servo4.end()
    # servo5.end()
