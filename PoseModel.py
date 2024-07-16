import cv2
import mediapipe as mp
import time
import math


class poseDetector():
    def __init__(self) -> None:
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.Pose = self.mpPose.Pose()
        self.config=[]
    def construct(self,img,draw=0):
        self.img=img
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.Pose.process(imgRGB)
        if draw:
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpPose.HAND_CONNECTIONS)
        lmList = []
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy,cz = int(lm.x * w), int(lm.y * h), int(lm.z*1000)
                lmList.append([id, cx, cy,cz])
            cx,cy=(lmList[12][1]+lmList[11][1])//2,(lmList[12][2]+lmList[11][2])//2
            lmList.append([33,cx,cy])
            cx,cy=(lmList[33][1]+lmList[0][1])//2,(lmList[33][2]+lmList[0][2])//2
            lmList.append([34,cx,cy])
        self.lmList = lmList
        if(self.config==[]):
             self.config=lmList
        return self.lmList
        
    def findAngle(self, p1, p2, p3, draw=True):
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:3]
        x2, y2 = self.lmList[p2][1:3]
        x3, y3 = self.lmList[p3][1:3]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        # print(angle)

        # Draw
        if draw:
            cv2.line(self.img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(self.img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(self.img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(self.img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(self.img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(self.img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(self.img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(self.img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(self.img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle
    def shoulder(self,hemi=1):
        if self.lmList!= None:
            if hemi==1:
                return(self.findAngle(14,12,33))
            else:        
                    return(self.findAngle(13,11,33))
    def elbow(self,hemi=1):
        if self.lmList!= None:
            if hemi==1:
                return(self.findAngle(12,14,16))
            else:        
                    return(self.findAngle(11,13,15))
    def wrist(self,hemi=1):
        if self.lmList!= None:
            if hemi==1:
                    return(self.findAngle(14,16,20))
            else:        
                    return(self.findAngle(13,15,19))

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        L=detector.construct(img)
        detector.elbow()
        detector.shoulder()
        # print(L[0],L[20])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

        cv2.imshow("Image", img)
        k=cv2.waitKey(1)
        if k==ord('q'):
            print(L[0],L[20])
            break 


if __name__ == "__main__":
    main()