import cv2, time, mediapipe, math, pydirectinput, pyautogui, keyboard, mouse
import tkinter as tk

#Pydirectinput uses win32api to get a lower level of input for games.

pydirectinput.PAUSE = 0
pydirectinput.FAILSAFE = False
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)
mp_hands = mediapipe.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.3, model_complexity=0)

mp_draw = mediapipe.solutions.drawing_utils
show_frame = True

#SOME GOOD SETTINGS:
#sens = 7, res = 8, smooth = 10, frame = -1

#DO NOT CHANGE
mode = "AIR"
broken_static = True

#Lists to track previous movement:
movement = []
last_move = []
sensitivity = 4

mouse_last_frame = False
found_hand_this_frame = False

#Track clicking
can_l = True
l_count = 0
l_threshold = 1
click_thresh = 25

r_count = 0
can_r = True

#Zooming
lvp = -1
lhp = -1
left_pinched = False
scroll_counter = 0
#Taha didn't make this

#Constants:
smoothing = 5
res_scale = 12

#Random
frame_counter = 0

while not keyboard.is_pressed("f9"):
    found_hand_this_frame = False
    if frame_counter == 0:
        sucess, image = cap.read()
        img = cv2.resize(cv2.cvtColor(image, cv2.COLOR_RGB2BGR), (160*res_scale,120*res_scale), interpolation = cv2.INTER_AREA)
        results = hands.process(img)

    #If there ARE hands:
    if results.multi_hand_landmarks:
        #For each HAND
        for hand in results.multi_hand_landmarks:
            if results.multi_handedness[results.multi_hand_landmarks.index(hand)].classification[0].label.lower() == "left" and not found_hand_this_frame:
                found_hand_this_frame = True
                if frame_counter == 0:
                    #found diagram @ https://www.researchgate.net/publication/355402809/figure/fig1/AS:1080622231617545@1634651825721/Mediapipe-hand-landmarks.png
                    fingertip = [hand.landmark[8].x * image.shape[1] * sensitivity, hand.landmark[8].y * image.shape[0] * sensitivity]
                    pinkytip = [hand.landmark[20].x * image.shape[1] * sensitivity, hand.landmark[20].y * image.shape[0] * sensitivity]
                    middletip = [hand.landmark[12].x * image.shape[1] * sensitivity, hand.landmark[12].y * image.shape[0] * sensitivity]
                    tracking_location = [hand.landmark[17].x * image.shape[1] * sensitivity, hand.landmark[17].y * image.shape[0] * sensitivity]
                    thumb = [hand.landmark[4].x * image.shape[1] * sensitivity, hand.landmark[4].y * image.shape[0] * sensitivity]
                    distance = math.sqrt((fingertip[0]/sensitivity-thumb[0]/sensitivity)**2 + (fingertip[1]/sensitivity-thumb[1]/sensitivity)**2)
                    distance2 = math.sqrt((pinkytip[0]/sensitivity-thumb[0]/sensitivity)**2 + (pinkytip[1]/sensitivity-thumb[1]/sensitivity)**2)
                    distance3 = math.sqrt((middletip[0]/sensitivity-thumb[0]/sensitivity)**2 + (middletip[1]/sensitivity-thumb[1]/sensitivity)**2)
                    
                if distance <= click_thresh:
                    l_count += 1
                    if l_count >= l_threshold and can_l:
                        can_l = False
                        broken_static = False
                        pydirectinput.mouseDown(button="left")
                if distance > click_thresh:
                    if not can_l:
                        pydirectinput.mouseUp(button="left")
                        broken_static = True 
                    l_count = 0
                    can_l = True
                if distance2 <= click_thresh:
                    r_count += 1
                    if r_count >= l_threshold and can_r:
                        can_r = False
                        broken_static = False
                        pydirectinput.mouseDown(button="right")
                if distance2 > click_thresh:
                    if not can_r:
                        pydirectinput.mouseUp(button="right")
                        broken_static = True
                    r_count = 0
                    can_r = True  
                try:
                    #Desk mode or not (air recommended).
                    if mode == "desk":
                        move = [last_move[0] - tracking_location[0], last_move[1] - tracking_location[1]]    
                    else:
                        move = [last_move[0] - tracking_location[0], tracking_location[1] - last_move[1]]
                    last_move = tracking_location    
                except:
                    last_move = tracking_location
                    pass
                #IDLE doesn't support un-indenting, so I just added an if statement so I didn't have to move everything =)
                try: movement.append(move)
                except: pass
                if len(movement) == smoothing:
                    sum_x = 0
                    sum_y = 0   
                    for x,y in movement:
                        sum_x += x
                        sum_y += y
                    dis = math.sqrt((sum_x / smoothing)**2 + (sum_y / smoothing)**2)
                    #DISTANCE MOVED NEEDED TO BREAK MOUSE FOCUS
                    if dis > 10:
                        broken_static = True
                    if broken_static and not distance3 <= click_thresh:
                        avg_x = sum_x / smoothing
                        avg_y = sum_y / smoothing
                    elif broken_static and distance3 <= click_thresh:
                        avg_x = (sum_x / smoothing) / 2
                        avg_y = (sum_y / smoothing) / 2
                    else:
                        avg_x = 0
                        avg_y = 0
                    pydirectinput.move(round((avg_x**1.2).real), round((avg_y**1.2).real), _pause=False) 
                    movement.pop(0)
            else:
                if True:
                    left_fingertip = [hand.landmark[8].x * image.shape[1], hand.landmark[8].y * image.shape[0]]
                    left_tracking_location = [hand.landmark[17].x * image.shape[1], hand.landmark[17].y * image.shape[0]]
                    left_thumb = [hand.landmark[4].x * image.shape[1], hand.landmark[4].y * image.shape[0]]
                    left_distance = math.sqrt((left_fingertip[0]-left_thumb[0])**2 + (left_fingertip[1]-left_thumb[1])**2)

                    v_dist = left_tracking_location[1] - lvp
                    h_dist = left_tracking_location[0] - lhp
                    
                    if left_distance <= click_thresh * 1.5:
                        if v_dist > 10 and -200 < h_dist < 200:
                            #scroll down
                            pyautogui.scroll(200)
                        elif v_dist < -10 and -200 < h_dist < 200:
                            #scroll up
                            pyautogui.scroll(-200)

                        elif h_dist > 10 and -200 < v_dist < 200:
                            pass

                        elif h_dist < -10 and -200 < v_dist < 200:
                            pass
                        
                    else:
                        scroll_counter = 0
                        left_pinched = False

                    lhp, lvp = left_tracking_location

#FRAME COUNTER - LOWER VALUE = MORE FRAME SKIP
    if frame_counter == 0:
        frame_counter = -3
    frame_counter += 1
    
    if show_frame:
        found_finger = None
        try: found_finger = fingertip
        except: found_finger = None

        if found_finger:
            if can_l:
                c = (0,0,255)
            else:
                c = (0,255,0)

            if can_r and can_l:
                c2 = (0,0,255)
            else:
                c2 = (0,255,0)

            if can_r:
                c3 = (0,0,255)
            else:
                c3 = (0,255,0)

            x, y = fingertip
            x2, y2 = thumb
            x3, y3 = pinkytip

        found_finger1 = None
        try: found_finger1 = left_fingertip
        except: found_finger1 = None

        if found_finger1:
            if can_r:
                c4 = (0,0,255)
            else:
                c4 = (0,255,0)
                
            x4, y4 = left_fingertip

        if found_finger:
            cv2.circle(img=image, center=(int(x/sensitivity), int(y/sensitivity)), radius=10, color=c, thickness=-1)
            cv2.circle(img=image, center=(int(x2/sensitivity), int(y2/sensitivity)), radius=10, color=c2, thickness=-1)
            cv2.circle(img=image, center=(int(x3/sensitivity), int(y3/sensitivity)), radius=10, color=c3, thickness=-1)
        if found_finger1:
            cv2.circle(img=image, center=(int(x4), int(y4)), radius=10, color=c4, thickness=-1)

    if show_frame:
        cv2.imshow("COMPUTER POV (BAD CAMERA OK DONT COMMENT)", image)
        
    cv2.waitKey(1)

pydirectinput.mouseUp(button="left")
pydirectinput.mouseUp(button="right")
pydirectinput.keyUp("ctrl")


