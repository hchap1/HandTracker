# HandTracker

Uses OPENCV-2 and mediapipe to track your hand position relative to camera, and convert into mouse positions.

----------------
**INSTALL MODULES**
pip3.10 install -r <FILEPATH TO REQUIREMENTS.TXT>
  
FINGER POSES:
  RIGHT HAND> Forefinger touching thumb = left click
              Pinky touching thumb = right click
  
  LEFT HAND> Forefinger touching thumb = activate scroll/zoom
             Move hand up/down while activated ^ = scroll
             Move hand left/right while activated ^ = zoom
 
NOTES:
  You can change some of the values, especially click_thresh to suit your hands / needs / camera FOV. 
  click_thresh is how close your fingers have to be to count as touching.
  show_frame shows what your camera is seeing.
 
