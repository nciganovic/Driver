# Driver
Computer vision script for simulating  gaming racing wheel

## Description
* When the program is started three windows will open. 
* All three windows are webcams. 
* One is at a normal position, one is rotated by 40 degrees and the last one is rotated by -40 degrees. 
* All three at the same time are trying to **detect a person's head** each frame of the recording. 
* If the first normal one detects head then the program knows that person is holding the head at a natural position. 
* If a camera with a **40-degree angle** detects head then the program knows that person tilted head on the right side and presses the **⬅ key on the keyboard**. 
* If a camera with a **-40 degree angle** detects head then the program knows that person tilted head on the left side and presses the **➡ key on the keyboard**.

## Demo
![](driver-demo.gif)

## How this works
* With [haar cascade for head detection](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml) I am able to detect persons head on camera.
* With three cameras on different angles I am able to detect if head is rotated on left or right or if it is normal.
* Depending on which camera detects head (only one out of three cameras can detect face) I am authomaticly pressing ⬅ or ➡ key on keyboard
* With that, you can play some racing games

## Requierments
#### Languague
* Python 3.8

#### Libraries
```
numpy==1.19.2
opencv-python==4.4.0.42
pynput==1.7.1
```
#### Other
Webcam, if you dont have webcam you can download [DroidCam](https://www.dev47apps.com/) and use your phone's camera as webcam like I did.

## Using on windows desktop games
* If you want to try this out on desktop games like GTA V you need to uncomment all **wk.PressKey() and wk.ReleaseKey()** methods comment all **keyboard.press() and keyboard.release()**
* If you choose **wk.PressKey()** you will press **A** or **D** key instead of ⬅➡

## How to run
* Install all requirements listed above.
* Run **driver.py** script

## Useful resources
* Haar Cascade tutorial on [pythonprogramming.net](https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/)
