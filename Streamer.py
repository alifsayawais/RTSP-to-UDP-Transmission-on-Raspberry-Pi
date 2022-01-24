from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import uic
import threading
from threading import Thread
import sys
import os
import signal
import time
global Flag
global counter
Flag=False
counter=0

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('final.ui',self)
        
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        #Labels
        self.label=self.findChild(QLabel,'label')
        self.label_2=self.findChild(QLabel,'label_2')
        self.label_3=self.findChild(QLabel,'label_3')
        self.label_4=self.findChild(QLabel,'label_4')

        #Text Bars
        self.lineEdit=self.findChild(QLineEdit,'lineEdit')
        self.lineEdit_2=self.findChild(QLineEdit,'lineEdit_2')
        self.lineEdit_3=self.findChild(QLineEdit,'lineEdit_3')

        #Buttons
        self.start=self.findChild(QPushButton,'pushButton')
        self.stop=self.findChild(QPushButton,'pushButton_3')
        
        #Button Defining
        self.start.clicked.connect(self.thread)     
        self.stop.clicked.connect(self.thread1)


    def thread(self):
        t1=Thread(target=self.Operation)
        t1.start()

    def thread1(self):
        t2=Thread(target=self.Terminate)
        t2.start()
        
    def ffmpegOperation(self):
        global rtsp
        global Flag
        global counter
        rtsp=self.lineEdit.text()
        udp=self.lineEdit_2.text()
        #rtsp = 'rtmp://123.201.108.125/test1'
        #udp = 'udp://192.168.0.132:8080'
        #udp = 'udp://169.254.187.43:8080'

        x= os.system (f"ffmpeg \
                        -rw_timeout 900000 \
                        -re \
                        -i {rtsp} \
                        -vsync vfr \
                        -map 0:2 \
                        -vcodec h264_v4l2m2m \
                        -pix_fmt yuv420p \
                        -s 1280x720 \
                        -loglevel error \
                        -max_muxing_queue_size 512 \
                        -b:v 4M -minrate 6M -maxrate 10M -bufsize 20M \
                        -num_capture_buffers 1024 \
                        -framerate 25/1 \
                        -acodec aac \
                        -f mpegts {udp}")

        counter=counter+1
        if (Flag==False):
            z=30
            if (counter >= 5):
                #start_time = time.time()
                for i in range(30):
                    #current_time = time.time()
                    time.sleep(1)
                    #elapsed_time = current_time - start_time
                    print (f"Reconnecting in {30-i}s...")
                    if (Flag==True):
                        print ("Stopping")
                        break
            if (x==256):
                try:
                    print("Stream Not Reachable")
                    #start_time = time.time()
                    for i in range(10):
                        #current_time = time.time()
                        time.sleep(1)
                        #elapsed_time = current_time - start_time
                        print (f"Reconnecting in {10-i}s...")
                        if (Flag==True):
                            print ("Stopping")
                            break
                    self.ffmpegOperation()
                except RecursionError:
                    print ("Recursion Error")
                    self.ffmpegOperation()
            if (x==0):
                print("stream disconnected")
                self.ffmpegOperation()
            if (x==15):
                print ("STREAM STOPPED,Press START if you want to connect again")
​
        else:
            print ("STREAMING STOPPED")
            Flag=False
            
    def Operation(self):
        global Flag
        Flag=False
        self.label_4.setStyleSheet('background-color: rgb(47, 148, 255)')
        self.ffmpegOperation()
​
​
    def Terminate(self):
        global Flag
        global counter
        Flag=True
        counter=0
        #print (Flag)
        self.label_4.setStyleSheet('background-color: rgb(255, 0, 0)')
        os.system('pkill -f "ffmpeg -rw_timeout "')
        
​
if __name__=="__main__":
    app=QApplication(sys.argv)
    UIWindow=UI()
    UIWindow.show()
    sys.exit(app.exec_())