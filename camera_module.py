import cv2
import time
import os
import mediapipe as mp
import math
import requests
import switches as sw
devices = sw.devices

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        
    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB) 
    #     print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    #Draw dots and connect them
                    self.mpDraw.draw_landmarks(img,handLms,
                                                self.mpHands.HAND_CONNECTIONS)

        return img
 
    def findPosition(self,img, handNo=0, draw=True):
        """Lists the position/type of landmarks
        we give in the list and in the list ww have stored
        type and position of the landmarks.
        List has all the lm position"""

        lmlist = []

        # check wether any landmark was detected
        if self.results.multi_hand_landmarks:
            #Which hand are we talking about
            myHand = self.results.multi_hand_landmarks[handNo]
            # Get id number and landmark information
            for id, lm in enumerate(myHand.landmark):
                # id will give id of landmark in exact index number
                # height width and channel
                h,w,c = img.shape
                #find the position
                cx,cy = int(lm.x*w), int(lm.y*h) #center
                # print(id,cx,cy)
                lmlist.append([id,cx,cy])

                # Draw circle for 0th landmark
                if draw:
                    cv2.circle(img,(cx,cy), 15 , (255,0,255), cv2.FILLED)

        return lmlist

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

overlayList = [1,2,3,4,5,6]
pTime = 0
detector = handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

number_of_finger = None
found_finger = False
while True:
    if found_finger == False and number_of_finger == None:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        time.sleep(0.8) 
        if len(lmList) != 0:
            fingers = []

            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)
            print(totalFingers)
            if totalFingers>0:
                found_finger = True
                number_of_finger = totalFingers
    else :
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
        #coordinates of the fore finger and thumb and encircling it
        if lmList : 
            x1, y1, = lmList[4][1], lmList[4][2]
            x2, y2, = lmList[8][1], lmList[8][2]
            cv2.circle(img , (x1 ,y1) ,15 , (134, 138, 204) ,cv2.FILLED)
            cv2.circle(img , (x2 ,y2) ,15 , (134, 138, 204) ,cv2.FILLED)
            #line joining above
            cv2.line(img, (x1,y1) , (x2,y2) , (37, 157, 140) ,3)

            z1 = (x1+x2)//2
            z2 = (y1+y2)//2
            length = math.hypot(x2-x1, y2-y1)
            if length <20 :
                
                print("Switch is on the new mode!")
                
                if number_of_finger in [1,2,3]:
                    url="http://192.168.137.226:8080/api/change-servo-device-state/" 
                else:
                    url="http://192.168.137.226:8080/api/change-device-state/" 
                button_number = int(devices[number_of_finger][1])
                state_change_value = 1 if devices[number_of_finger][3]==0 else 0
                
                state_url="http://192.168.137.226:8080/api/check-device-status/" 
                state = dict(requests.get(state_url , params = {"button_number" : button_number}).json())["state"]
                print(f"The state is : {state}")
                response = requests.post(
                    url = url,  
                    headers = {"Authorization" : "Bearer 7JdKKbw03kLCiop"} ,
                    data = {"button_number" : button_number , "state_change_value" : 1 if state == 0 else  0}
                )
                found_finger = False
                number_of_finger = None
            
            print(f"The length is : {length} and totalFinger : {number_of_finger}")
                    
                
            
            cv2.putText(img, str(number_of_finger), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                        10, (255, 0, 0), 25)