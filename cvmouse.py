import cv2, time, mouse, mediapipe, math, keyboard

cap = cv2.VideoCapture(0)
mp_hands = mediapipe.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.3)
mp_draw = mediapipe.solutions.drawing_utils
show_frame = False

#DO NOT CHANGE
mode = "AIR"

#Lists to track previous movement:
movement = []
last_move = []
sensitivity = 7
mouse_last_frame = False

#Track clicking
can_l = True
l_count = 0
l_threshold = 1
click_thresh = 30

r_count = 0
can_r = True

#Zooming
horizontal_previous_distance = 0
vertical_previous_distance = 0
left_pinched = False
scroll_counter = 0

#Constants:
smoothing = 5

#Random
last_frame = time.time()*1000
#set to 1000 to turn off
frameskip_thresh = 1000

while True:
    found_time = False
    try:
        deltatime = (time.time()*1000)-last_frame
        found_time = True
    except:
        pass
    last_frame = time.time()*1000
    if deltatime < frameskip_thresh:
        sucess, image = cap.read()
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(img)

    #If there ARE hands:
    if deltatime < frameskip_thresh and results.multi_hand_landmarks:

        #For each HAND
        for hand in results.multi_hand_landmarks:
            if results.multi_handedness[results.multi_hand_landmarks.index(hand)].classification[0].label.lower() == "left":
            
                #found diagram @ https://www.researchgate.net/publication/355402809/figure/fig1/AS:1080622231617545@1634651825721/Mediapipe-hand-landmarks.png
                fingertip = [hand.landmark[8].x * image.shape[1] * sensitivity, hand.landmark[8].y * image.shape[0] * sensitivity]
                pinkytip = [hand.landmark[20].x * image.shape[1] * sensitivity, hand.landmark[20].y * image.shape[0] * sensitivity]
                tracking_location = [hand.landmark[17].x * image.shape[1] * sensitivity, hand.landmark[17].y * image.shape[0] * sensitivity]
                thumb = [hand.landmark[4].x * image.shape[1] * sensitivity, hand.landmark[4].y * image.shape[0] * sensitivity]
                distance = math.sqrt((fingertip[0]/sensitivity-thumb[0]/sensitivity)**2 + (fingertip[1]/sensitivity-thumb[1]/sensitivity)**2)
                distance2 = math.sqrt((pinkytip[0]/sensitivity-thumb[0]/sensitivity)**2 + (pinkytip[1]/sensitivity-thumb[1]/sensitivity)**2)

                if distance <= click_thresh:
                    l_count += 1

                    if l_count >= l_threshold and can_l:
                        can_l = False
                        mouse.press("left")

                if distance > click_thresh:
                    if not can_l:
                        mouse.release("left")
                        
                    l_count = 0
                    can_l = True

                if distance2 <= click_thresh:
                    r_count += 1

                    if r_count >= l_threshold and can_r:
                        can_r = False
                        mouse.press("right")

                if distance2 > click_thresh:
                    if not can_r:
                        mouse.release("right")

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
                    print("ERROR")
                    last_move = tracking_location
                    pass

                #IDLE doesn't support un-indenting, so I just added an if statement so I didn't have to move everything =)
                if len(movement) == smoothing:
                    sum_x = 0
                    sum_y = 0
                    
                    for x,y in movement:
                        sum_x += x
                        sum_y += y

                    dis = math.sqrt((sum_x / smoothing)**2 + (sum_y / smoothing)**2)
                    clkn = can_l and can_r
                    boolean = clkn or dis > 50

                    if boolean:
                        avg_x = sum_x / smoothing
                        avg_y = sum_y / smoothing
                    else:
                        avg_x = 0
                        avg_y = 0

                    mouse.move(avg_x, avg_y, absolute=False) 
                    movement.pop(0)

                try: movement.append(move)
                except: print("MOVE DOESN'T EXIST")
                
            else:
                try:
                    left_fingertip = [hand.landmark[8].x * image.shape[1] * sensitivity, hand.landmark[8].y * image.shape[0] * sensitivity]
                    left_tracking_location = [hand.landmark[17].x * image.shape[1] * sensitivity, hand.landmark[17].y * image.shape[0] * sensitivity]
                    left_thumb = [hand.landmark[4].x * image.shape[1] * sensitivity, hand.landmark[4].y * image.shape[0] * sensitivity]
                    left_distance = math.sqrt((left_fingertip[0]/sensitivity-left_thumb[0]/sensitivity)*(left_fingertip[0]/sensitivity-left_thumb[0]/sensitivity) + (left_fingertip[1]/sensitivity-left_thumb[1]/sensitivity)*(left_fingertip[1]/sensitivity-left_thumb[1]/sensitivity))

                    if left_distance <= click_thresh:
                        scroll_counter += 1
                        left_pinched = True
                        if scroll_counter > 1:
                            horizontal_distance = (fingertip[0] - left_fingertip[0])
                            vertical_distance = (fingertip[1] - left_fingertip[1])
                            if horizontal_previous_distance == 0 or vertical_previous_distance == 0:
                                horizontal_previous_distance = horizontal_distance
                                vertical_previous_distance = vertical_distance

                            elif scroll_counter > 1:
                                hdist = horizontal_distance - horizontal_previous_distance
                                vdist = vertical_distance - vertical_previous_distance
                                
                                if hdist < -50 and 50 > vdist > -50:
                                    keyboard.press("ctrl")
                                    mouse.wheel(1)
                                    keyboard.release("ctrl")


                                elif hdist > 50 and 50 > vdist > -50:
                                    keyboard.press("ctrl")
                                    mouse.wheel(-1)
                                    keyboard.release("ctrl")

                                if vdist < -50:
                                    print("scrolling up")
                                    mouse.wheel(3)

                                elif vdist > 50:
                                    mouse.wheel(-3)
                                    print("scrolling down")

                            horizontal_previous_distance = horizontal_distance
                            vertical_previous_distance = vertical_distance
                    else:
                        scroll_counter = 0
                        left_pinched = False
                except:
                    pass
       
    if show_frame:
        found_finger = None
        try: found_finger = fingertip
        except: found_finger = None

        if found_finger:
            if can_l:
                c = (0,0,255)
            else:
                c = (0,255,0)
            x, y = fingertip
            print("hi!")
            cv2.circle(img=image, center=(int(x/sensitivity), int(y/sensitivity)), radius=10, color=c, thickness=-1)


        cv2.imshow("OUT", image)
    cv2.waitKey(1)

