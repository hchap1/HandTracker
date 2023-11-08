# HandTracker - DOWNLOAD Computer Vision Mouse.zip | Main code = cvmouse3.pyw |
*python file is more performant and more frequently updated -> use .exe only if:
  Python is not installed.
  Modules are not installed.

You can basically treat the .pyw as an app.

Uses OPENCV-2 and mediapipe to track your hand position relative to camera, and convert into mouse positions.

----------------
**INSTALL MODULES**
pip3.10 install -r <FILEPATH TO REQUIREMENTS.TXT>

LIST OF MODULES:
  mouse (pip3.10 install mouse)
  keyboard (pip3.10 install keyboard)
  cv2 (pip3.10 install opencv-python)
  mediapipe (pip3.10 install mediapipe)
  pyautogui (pip3.10 install pyautogui)
  pydirectinput (pip3.10 install pydirectinput)

  INCLUDED WITH PYTHON:
  time
  numpy
  math
  
FINGER POSES:
  RIGHT HAND> Forefinger touching thumb = left click
              Pinky touching thumb = right click
              Movement of mouse cursor is based off right hand movement.
  
  LEFT HAND> Forefinger touching thumb = activate scroll
             Move hand up/down while activated ^ = scroll
 
NOTES:
  You can change some of the values, especially click_thresh to suit your hands / needs / camera FOV. 
  click_thresh is how close your fingers have to be to count as touching.
  show_frame shows what your camera is seeing.

  If you are experiencing performance problems:
    If the performance problem is jumpy hand movement, increase the smoothing variable.
    If the performance problem is frame-rate related:
      Decrease the reset for frame skip found halfway through code.
      Decrease resolution scaling variable.

  This will work with some games. For example, in Minecraft, it works if the raw input option is off in settings.
