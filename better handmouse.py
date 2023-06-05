from cvzone.HandTrackingModule import HandDetector
import cv2, mouse

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
counter = 0
has_clicked = False

rc = 0
lc = 0
cl = True
cr = False
click_sensitivity = 5
smoothing_constant = 3

lp = []
xm=5
ym=5

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands and hands[0]["type"].lower() == "right":
        hand1 = hands[0]
        cp = hand1['center']
        handType1 = hand1["type"]
        fingers = detector.fingersUp(hand1)
        left = fingers[1]
        right = fingers[2]

        #Checks how many frames you've been clicking for.
        if left == 0:
            left = True
            lc += 1
        else:
            left = False
            lc = 0
            cl = True

        if right == 0:
            right = True
            rc += 1
        else:
            right = False
            rc = 0
            cr = True

        #Clicks based on above code.
        if lc >= click_sensitivity:
            cl = False
            mouse.click("left")

        if rc >= click_sensitivity:
            cr = False
            mouse.click("right")

        #Track frames from previous THREE positions
        if len(lp) < smoothing_constant:
            lp.append(cp)

        else:
            lp.append(cp)
            lp.pop(0)
        if len(lp) == smoothing_constant:
            average_pos = [(lp[0][0]+lp[1][0]+lp[2][0])/3, (lp[0][1]+lp[1][1]+lp[2][1])/3]
            change_x = cp[0] - average_pos[0]
            change_y = cp[1] - average_pos[1]
            mouse.move(change_x*xm*-1, change_y*ym, absolute=False)

        cv2.imshow("window", img)
        
    else:
        left = False
        right = False

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
