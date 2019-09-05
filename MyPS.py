#!/usr/bin/python
#coding:utf-8 
"""
@author: SPRATUMN
@software: PyCharm
@file: MyPS.py
@time: 2018/9/16 22:02
"""
import CVshopmainwindow
import cv2 as cv
import numpy as np
import sys
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


# 主窗口类，继承窗口Ui_MainWindow主界面
class MyPS(QMainWindow, CVshopmainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 窗口属性修改
        self.setWindowTitle('PS')
        self.label.setAlignment(Qt.AlignCenter)
        self.actionSnip.setDisabled(True)
        self.actionRecord.setDisabled(True)
        # 实例属性初始化
        self.cap = cv.VideoCapture(0)
        self.fName = ''
        self.mat = np.zeros([1, 1, 3], np.uint8)
        # 信号槽连接
        self.actionFile.triggered.connect(self.load_file)
        self.actionCamera.triggered.connect(self.open_camera)
        self.actionRotate.triggered.connect(self.rotate_image)
        self.actionFlip.triggered.connect(self.flip_image)
        self.actionSnip.triggered.connect(self.snip_image)
        self.actionRecord.triggered.connect(self.record_camera)

    # 加载文件,根据后缀判断文件类型
    def load_file(self):
        if self.cap.isOpened():
            self.cap.release()
            self.actionSnip.setDisabled(True)
        self.fName = QFileDialog.getOpenFileName(self, 'Open File', './',
                                                 'Image Files (*.png *.jpg *.bmp);;Video Files (*.mp4 *.mkv)')
        if self.fName[0].endswith('png') or self.fName[0].endswith('jpg') or self.fName[0].endswith('bmp'):
            self.mat = cv.imread(self.fName[0])
            self.display_image(self.mat)
        elif self.fName[0].endswith('mp4') or self.fName[0].endswith('mkv'):
            QMessageBox.warning(self, 'Warning', 'video file', QMessageBox.Ok)
            self.cap.open(self.fName[0])
            while self.cap.isOpened():
                self.actionSnip.setEnabled(True)
                self.actionRecord.setEnabled(True)
                ret, cam_img = self.cap.read()
                if ret:
                    self.display_image(cam_img)
                    cv.waitKey(33)

    # 打开摄像头
    def open_camera(self):
        self.cap = cv.VideoCapture(0)
        if self.cap.isOpened():
            self.cap.release()
        if self.cap.open(0):
            while self.cap.isOpened():
                self.actionSnip.setEnabled(True)
                self.actionRecord.setEnabled(True)
                ret, cam_img = self.cap.read()
                if ret:
                    self.display_image(cam_img)
                    cv.waitKey(33)
        else:
            QMessageBox.warning(self, 'Error', 'Open camera fail', QMessageBox.Ok)

    # 录制摄像头视频
    def record_camera(self):
        pass

    # 获取视频当前帧的图片
    def snip_image(self):
        if self.cap.isOpened():
            ret, self.mat = self.cap.read()
            if ret:
                self.actionSnip.setDisabled(True)
                self.actionRecord.setDisabled(True)
                self.display_image(self.mat)
                self.cap.release()

    # 使用label显示图片
    def display_image(self, imge):
        height, width, channels = imge.shape
        if height > 400 or width > 800:
            rate = height / 400 if height / 400 > width / 800 else width / 800
            width = int(width / rate)
            height = int(height / rate)
            img = cv.resize(imge, (width, height))
        else:
            img = imge
        self.statusbar.showMessage('img size:({},{})'.format(width, height))
        self.statusbar.show()
        line_bytes = channels * width
        qt_image = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        label_image: QImage = QImage(qt_image.data, width, height, line_bytes, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(label_image))

    def mousePressEvent(self, event):
        print('clicked at (', event.x(), ',', event.y(), ')')

    def closeEvent(self, *args, **kwargs):
        self.cap.release()

    def rotate_image(self):
        self.mat = cv.transpose(self.mat)
        self.mat = cv.flip(self.mat, 1)
        self.display_image(self.mat)

    def flip_image(self):
        self.mat = cv.flip(self.mat, 1)
        self.display_image(self.mat)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyPS()
    w.show()
    sys.exit(app.exec_())
