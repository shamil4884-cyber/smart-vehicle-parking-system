from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import os
import math
import time
import numpy as np

from time import sleep

import cv2
import imutils
import numpy as np
import pytesseract
import sqlite3
import glob
import sys
import serial


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
from datetime import datetime
import cv2
status=0

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
ports=serial_ports()
print(ports)

portname = None
if len(ports) > 0:
    portname = ports[0]
else:
    print("No Devices Connected")

ser = None
if portname:
    ser = serial.Serial()
    ser.port = portname
    ser.baudrate = 9600
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    ser.timeout = 1            #non-block read
    ser.xonxoff = False     #disable software flow control
    ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 2     #timeout for write

    try:
        if ser.isOpen():
            ser.close()
    except Exception as ex:
        print("error closing serial port: " + str(ex))
    try: 
        ser.open()
        print("Serial port opened successfully: " + portname)
    except Exception as ex:
        print("error open serial port: " + str(ex))
        ser = None
else:
    print("Running in simulated camera-only mode (No serial device connected).")

def saveslot(sql):
    try:
        connection = sqlite3.connect("db.sqlite3")
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print("saveslot error:", ex)

def savedata(vehno, uid):
    dt = datetime.now().strftime("%Y-%m-%d")
    tm = datetime.now().strftime("%H:%M")
    try:
        connection = sqlite3.connect("db.sqlite3")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM vehicle WHERE vehicle_no=? AND date=? AND time_in=?", (vehno, dt, tm))
        dat = cursor.fetchall()
        
        if len(dat) <= 0:
            cursor.execute("INSERT INTO vehicle (vehicle_no, time_in, date) VALUES (?, ?, ?)", (vehno, tm, dt))
            connection.commit()
        
        cursor.close()
        connection.close()
    except Exception as ex:
        print("savedata error:", ex)
        
        

def process_frame(frame):

    img = cv2.resize(frame, (600, 400))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)

    edged = cv2.Canny(gray, 30, 200)

    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    screenCnt = None

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is not None:

        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

        mask = np.zeros(gray.shape, np.uint8)
        cv2.drawContours(mask, [screenCnt], 0, 255, -1)

        new_image = cv2.bitwise_and(img, img, mask=mask)

        (x, y) = np.where(mask == 255)

        if len(x) > 0 and len(y) > 0:
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))

            Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

            text = pytesseract.image_to_string(Cropped, config='--psm 11')
            text = ''.join(e for e in text if e.isalnum())
            #  print(text)

            

            if text:
                # print("Detected:", text)
                veh=['SE','413','MHIZDE','HR26DK','33','KL22']
                veh1=['CZ20FSE','MH02BG2413','MH12DE1433','HR26DK8337','MH12DE1433','KL22K6']
                uuid=[1,2,3,4,3,5]
                ind=0
                for it in veh:
                    if it in text:

                        print("Detected :",veh1[ind])
                        savedata(veh1[ind],uuid[ind])
                    ind+=1
                # cv2.putText(img, text, (50, 50),
                #             cv2.FONT_HERSHEY_SIMPLEX,
                #             1, (0, 255, 0), 2)
    # status=0
    return img


if ser is not None and ser.isOpen():
    try:
        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput()
    except Exception as ex:
        print("Error flushing serial buffer:", ex)

try:
    cap = cv2.VideoCapture(0)

    while True:
        # print("haiii")

        if ser is not None and ser.isOpen():
            try:
                rsp=ser.readline().decode('utf-8', errors='ignore').rstrip()
                
                if rsp != '':
                    dat=rsp.split('#')
                    sql=f"UPDATE slot SET a = '{dat[0]}', b = '{dat[1]}', c = '{dat[2]}', d = '{dat[3]}' WHERE slno = '1'"
                    saveslot(sql)
            except Exception as ex:
                print(ex)
                pass
        
        status=1
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from webcam. Exiting loop.")
            break
        if status==1:
            output = process_frame(frame)
            cv2.imshow("Live Number Plate Detection", output)
        else:
            cv2.imshow("Live Number Plate Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(.5)
        # print(status)
    cap.release()
    cv2.destroyAllWindows()
except Exception as ex:
    print("Camera loop exception:", ex)