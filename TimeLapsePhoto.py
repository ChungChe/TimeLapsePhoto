#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import time
from time import strftime
import sys
import os

# fswebcam -p YUYV -d /dev/video0 -r 640x480 file.jpg
# jpegoptim file.jpg --strip-all

class timeLapseWidget(QWidget):
    def __init__(self, parent=None):
        super(timeLapseWidget, self).__init__(parent)
        self.duration = 25 # take a photo for every 25 seconds
        self.createWidgets()
        self.setWindowTitle(u"縮時攝影")
        self.timer = QTimer()
    def take_a_photo(self):
        file_name = "/home/pi/photos/{}.jpg".format(strftime("%Y_%m_%d_%H_%M_%S")) 
        #self.status_label.setText(u"{}".format(file_name))
        os.system("fswebcam -p YUYV -d /dev/video0 -r 640x480 {}".format(file_name))
        os.system("jpegoptim {} --strip-all".format(file_name))
        
        pix = QPixmap(file_name)
        scaled_pix = pix.scaled(self.status_label.size(), Qt.KeepAspectRatio)
        self.status_label.setPixmap(scaled_pix)
    def start(self):
        self.status_label.setText(u"開始截圖")
        self.timer.timeout.connect(self.take_a_photo)
        self.timer.start(int(self.spin_box.value() * 1000))
    def end(self):
        QCoreApplication.instance().quit()
    def createWidgets(self):
        hbox_bottom = QHBoxLayout()
        start_button = QPushButton(u"開始")
        start_button.setFixedHeight(60)
        start_button.clicked.connect(self.start)

        end_button = QPushButton(u"結束")
        end_button.setFixedHeight(60)
        end_button.clicked.connect(self.end)

        hbox_bottom.addWidget(start_button)
        hbox_bottom.addWidget(end_button)

        duration_label = QLabel(self)
        duration_label.setText(u"抓圖間隔:")
        
        self.spin_box = QSpinBox(self)
        self.spin_box.setFixedSize(120, 60)
        self.spin_box.setRange(1, 80000)
        self.spin_box.setValue(self.duration)

        self.status_label = QLabel(self)
        self.status_label.setFixedSize(320, 240)
        hbox_body = QHBoxLayout()
        hbox_body.addWidget(duration_label)
        hbox_body.addWidget(self.spin_box)

        vbox = QVBoxLayout()
        vbox.addWidget(self.status_label)
        vbox.addLayout(hbox_body)
        vbox.addLayout(hbox_bottom)
        self.setLayout(vbox)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = timeLapseWidget()
    widget.show()
    sys.exit(app.exec_())
