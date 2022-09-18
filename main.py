import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np

from IPython import display

from time import sleep

from Servo import Servo

servo1 = Servo()
servo2 = Servo()
servo3 = Servo()
servo4 = Servo()

servo1.attach(14)
servo2.attach(15)
servo3.attach(18)
servo4.attach(23)
#servo5.attach(18,50)

servo1.start()
servo2.start()
servo3.start()
servo4.start()

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("debug.ui")[0]

pos = np.array([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], dtype=float)
r = 1
theta = np.array([0, 0, 0, 0], dtype=float)  # 0 ~ pi
theta_sum = np.array([0, 0, 0, 0], dtype=float)  # 0 ~ pi

num_motion = 20

# 화면을 띄우는데 사용되는 Class 선언


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

        for i in range(num_motion):
            self.listWidget.addItem(f"motion {i+1}")

        self.motion.clicked.connect(self.setMotion)

        self.fix.toggled.connect(self.slot_toggle)

        self.canvas = FigureCanvas(Figure(figsize=(4, 3)))
        self.gridLayout.addWidget(self.canvas)

        self.ax = self.canvas.figure.subplots()
        self.ax.set_xlim([-6, 6])
        self.ax.set_ylim([-6, 6])
        self.ax.set_aspect('equal', adjustable='box')

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
                pos[i] = pos[i-1] + r * \
                    np.array([np.cos(theta_sum[i-1]),
                             np.sin(theta_sum[i-1])], dtype=float)
        else:
            for i in [2, 1, 0]:
                theta_sum[i] = theta_sum[i+1] - theta[i+1]

            for i in [3, 2, 1, 0]:
                pos[i] = pos[i+1] - r * \
                    np.array([np.cos(theta_sum[i]), np.sin(
                        theta_sum[i])], dtype=float)

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

    def set_theta(self, num, deg):
        theta[num] = np.radians(deg)
        if num == 0:
            servo1.write(deg+90)
            self.label_1.setText(f"{deg}")
            self.horizontalSlider_1.setValue(deg)
        if num == 1:
            servo2.write(deg+90)
            self.label_2.setText(f"{deg}")
            self.horizontalSlider_2.setValue(deg)
        if num == 2:
            servo3.write(deg+90)
            self.label_3.setText(f"{deg}")
            self.horizontalSlider_3.setValue(deg)
        if num == 3:
            servo4.write(deg+90)
            self.label_4.setText(f"{deg}")
            self.horizontalSlider_4.setValue(deg)

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


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
    servo1.end()
