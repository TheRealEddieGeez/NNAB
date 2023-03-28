#Import Dependencies
import win32api
import win32con
import mss
import numpy as np
import cv2
import time
import pyautogui
import keyboard
import torch


pyautogui.FAILSAFE = True #

##model = torch.hub.load ('ultralytics/yolov5', 'yolov5s', pretrained=True) #Loads Base Model of yolov5
model = torch.hub.load ('ultralytics/yolov5', 'custom', path='E:\NNProject\NNAB\NNProject') #Loads custom model, replaces above.  ## CHANGE PATH TO CSGO.PT LOCATION ##

monitor_width = 1920  # Monitor Width
monitor_height = 1080  # Monitor Height
capture_width = 1920  # Rendered Window Width
capture_height = 1080  # Rendered Window Height

capture_top = int((monitor_height - capture_height) / 2) #To Center Window 
capture_left = int((monitor_width - capture_width) / 2)

with mss.mss() as sct:
    monitor = {'top': capture_top, 'left': capture_left, 'width': capture_width, 'height': capture_height}
 
while True: #Creates a loop

     
     t = time.time()
     img = np.array(sct.grab(monitor))  #Grabs Image on Screen
     results = model(img)   #Model Refrence
     rl = results.xyxy[0].tolist()
     print(rl) 


     if len(rl) > 0:
          if rl[0][4] > 0.35:  # Confidence level over percentage
               if rl[0][5] == 0 or rl[0][5] == 1:  # [X][X] == Actual Number
                    x = int(rl[0][2])  # Gets X Coords
                    y = int(rl[0][3])  # Gets Y Coords

                    width = int(rl[0][2] - rl[0][0])  # Width = X Coord Max - X Coord Min
                    print('width', width)  # Prints Width

                    height = int(rl[0][3] - rl[0][1])  # Height = Y Coord Max - Ycord Min
                    print('height', height)  # Prints Height

                    # Calculate the absolute coordinates of the center point of the box
                    x_center_abs = int(rl[0][0] + width / 2)  # Absolute X coordinate of the center point
                    y_center_abs = int(rl[0][1] + height / 2)  # Absolute Y coordinate of the center point

                    # Calculate the relative coordinates of the center point of the box
                    x_center_rel = x_center_abs / 1920  # Relative X coordinate of the center point
                    y_center_rel = y_center_abs / 1080  # Relative Y coordinate of the center point

                    # Convert the relative coordinates to absolute coordinates of the center point
                    x_center_abs_final = int(x_center_rel * 65535)  # Absolute X coordinate of the center point
                    y_center_abs_final = int(y_center_rel * 65535)  # Absolute Y coordinate of the center point

                    print('Moving mouse to:', x_center_abs_final, y_center_abs_final)

                    # Move the mouse to the absolute coordinates of the center point
                    win32api.mouse_event(
                         win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE,
                         x_center_abs_final,
                         y_center_abs_final
                    )
                  






     cv2.imshow('s', np.squeeze(results.render()))  #Display Images

     ##print('fps: {}'.format(1 / (time.time() - t))) #Get Frames and Prints to Terminal

     cv2.waitKey(1) #Wait Timer

     if keyboard.is_pressed('pause'):   #If this key is pressed process closes
        break
         
cv2.destroyAllWindows   #Closes Window
