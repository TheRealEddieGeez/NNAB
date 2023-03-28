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


pyautogui.FAILSAFE = False # Maybe?

##model = torch.hub.load ('ultralytics/yolov5', 'yolov5s', pretrained=True) #Loads Base Model of yolov5
model = torch.hub.load ('ultralytics/yolov5', 'custom', path='E:/NNProject/csgo.pt') #Loads custom model, replaces above.

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
          if rl[0][4] > .35: #Confidence level over Percentage
               if rl[0][5] == 0  or rl[0][5] == 1 : #[X][X] == Actual Number
                    x = int(rl[0][2])   #Gets X Coords
                    y = int(rl[0][3])   #Gets Y Coords

                    width = int(rl[0][2] - rl[0][0]) #Width = X Coord Max - X Coord Min
                    print('width', width)   #Prints Width

                    height = int(rl[0][3] - rl[0][1]) #Height = Y Coord Max - Ycord Min
                    print('height', height)   #Prints Height

                    xpos = int(0.1 * ((x - width/2)) - pyautogui.position()[0]) #Math to find Half the width to find center of X Multiplier Varies
                    ypos = int(0.1 * ((y - height/2)) - pyautogui.position()[1]) #Math to find Half the width to find center of Y Multiplier Varies
                    
                    print('Moving mouse to:', xpos, ypos)

                    ##pyautogui.moveTo(xpos, ypos) #Moves mouse to postion
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(xpos/1920*65535.0), int(ypos/1080*65535.0))

                    print('Mouse moved to:', pyautogui.position())

                    ##pyautogui.click() #Auto clicks on above position

                    ##pyautogui.moveTo(-xpos, -ypos) #Moves mouse back to the same position



     cv2.imshow('s', np.squeeze(results.render()))  #Display Images

     ##print('fps: {}'.format(1 / (time.time() - t))) #Get Frames and Prints to Terminal

     cv2.waitKey(1) #Wait Timer

     if keyboard.is_pressed('pause'):   #If this key is pressed process closes
        break
         
cv2.destroyAllWindows   #Closes Window
