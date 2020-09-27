import numpy as np
import cv2 
import time
import platform
import winkeys as wk #Keaboard keys for playing games on Windows
from pynput.keyboard import Key, Controller

eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
head_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

keyboard = Controller()

total_frames = 0

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

go_left = False
go_right = False

while 1:
    ret, frame = cap.read()
    rotate_frame_left = rotate_image(frame, 40)
    rotate_frame_right = rotate_image(frame, -40)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_rotate_left = cv2.cvtColor(rotate_frame_left, cv2.COLOR_BGR2GRAY)
    gray_rotate_right = cv2.cvtColor(rotate_frame_right, cv2.COLOR_BGR2GRAY)
    
    eyes = head_cascade.detectMultiScale(gray, 1.3, 5)
    eyes_rotate_left = head_cascade.detectMultiScale(gray_rotate_left, 1.3, 5)
    eyes_rotate_right = head_cascade.detectMultiScale(gray_rotate_right, 1.3, 5)

    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    
    for (ex,ey,ew,eh) in eyes_rotate_left:
        cv2.rectangle(rotate_frame_left, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    
    for (ex,ey,ew,eh) in eyes_rotate_right:
        cv2.rectangle(rotate_frame_right, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    
    if(len(eyes) >= 2):
        print(f"{total_frames}. CENTER")
        if(go_left is True):
            #keyboard.release(Key.left)
            wk.ReleaseKey(wk.hex_left_arrow)
        if(go_right is True):
            #keyboard.release(Key.right)
            wk.ReleaseKey(wk.hex_right_arrow)
        go_left = False
        go_right = False
    
    elif(len(eyes_rotate_left) >= 2):
        print(f"{total_frames}. LEFT")
        go_right = False
        if(go_left is False):
            #keyboard.press(Key.left)
            #keyboard.release(Key.right)
            wk.PressKey(wk.hex_left_arrow)
            wk.ReleaseKey(wk.hex_right_arrow)
            go_left = True  
    elif(len(eyes_rotate_right) >= 2):
        print(f"{total_frames}. RIGHT")
        go_left = False
        if(go_right is False):
            #keyboard.press(Key.right)
            #keyboard.release(Key.left)
            wk.PressKey(wk.hex_right_arrow)
            wk.ReleaseKey(wk.hex_left_arrow)
            go_right = True
    

    total_frames += 1

    #Display windows
    cv2.imshow('Rotated Frame Left', rotate_frame_left)
    cv2.imshow('Frame', frame)
    cv2.imshow('Rotated Frame Right', rotate_frame_right)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

#for (ex,ey,ew,eh) in eyes:
    #print(f"ex = {ex}")
    #print(f"ey = {ey}")
    #print(f"ew = {ew}")
    #print(f"eh = {eh}")
    #print("\n")

"""
if(len(eyes) >= 2):
    
    #Figure out which eye is left or right
    x_axis_eye1 = eyes[0][0]
    y_axis_eye1 = eyes[0][1]
    x_axis_eye2 = eyes[1][0] 
    y_axis_eye2 = eyes[1][1]  

    left_eye = 0
    right_eye = 0

    if(x_axis_eye1 < x_axis_eye2):
        left_eye = {
            "x" : x_axis_eye1,
            "y" : y_axis_eye1
        }
        right_eye = {
            "x" : x_axis_eye2,
            "y" : y_axis_eye2
        }
    else:
        right_eye = {
            "x" : x_axis_eye1,
            "y" : y_axis_eye1
        }
        left_eye = {
            "x" : x_axis_eye2,
            "y" : y_axis_eye2
        }
    #compare height of eyes

    eye_diff = left_eye["y"] - right_eye["y"]
    threshold = 15
    if(eye_diff > threshold or eye_diff < (threshold * -1)):
        total_frames += 1
        #print(eye_diff)
        #print(left_eye["y"])
        #print(right_eye["y"])
        #print("\n")

        if(eye_diff > 0): 
            #print(f"{total_frames}. RIGHT")
            keyboard.press(Key.right)
            keyboard.release(Key.right)
        else: 
            #print(f"{total_frames}. LEFT")
            keyboard.press(Key.left)
            keyboard.release(Key.left)
"""