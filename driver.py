import numpy as np
import cv2 
import time
import platform
from pynput.keyboard import Key, Controller

if(platform.system() == "Windows"):
    import winkeys as wk #Keaboard keys for playing games on Windows

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
    frame = cv2.resize(frame, (480, 360), interpolation = cv2.INTER_LINEAR)

    if(frame is None):
        print("frame is None, can't open camera")
        break

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
    
    if(len(eyes) >= 1):
        print(f"{total_frames}. CENTER")
        if(go_left is True):
            keyboard.release(Key.left)
            #wk.ReleaseKey(wk.hex_left_arrow)
        if(go_right is True):
            keyboard.release(Key.right)
            #wk.ReleaseKey(wk.hex_right_arrow)
        go_left = False
        go_right = False
    
    elif(len(eyes_rotate_left) >= 1):
        print(f"{total_frames}. LEFT")
        go_right = False
        if(go_left is False):
            keyboard.press(Key.left)
            keyboard.release(Key.right)
            #wk.PressKey(wk.hex_left_arrow)
            #wk.ReleaseKey(wk.hex_right_arrow)
            go_left = True  
    elif(len(eyes_rotate_right) >= 1):
        print(f"{total_frames}. RIGHT")
        go_left = False
        if(go_right is False):
            keyboard.press(Key.right)
            keyboard.release(Key.left)
            #wk.PressKey(wk.hex_right_arrow)
            #wk.ReleaseKey(wk.hex_left_arrow)
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
