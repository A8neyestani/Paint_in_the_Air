import cv2
import time
import os
import handTrackingModule as htm
import numpy as np

wCam, hCam = 640, 480
eraser=cv2.imread('eraser.png')
eraser=cv2.resize(eraser,(100,100))
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

CTime = 0
PTime = 0
color=(0,0,255)


detector = htm.handDetector()
EraserBox={'x1':500,'y1':0,'x2':600,'y2':100}
redplt={'x1':100,'y1':0,'x2':200,'y2':100}
blueplt={'x1':300,'y1':0,'x2':400,'y2':100}


fingerX=[]
while True:
    _, frame = cap.read()
    if frame is None:
        break
    
    img = detector.findHands(frame)
    frame=cv2.rectangle(frame,(EraserBox['x1'],EraserBox['y1']),
                              (EraserBox['x2'],EraserBox['y2']),
                              (0,0,255),3)
    frame=cv2.rectangle(frame,(redplt['x1'],redplt['y1']),
                              (redplt['x2'],redplt['y2']),
                              (0,0,255),-1)
    frame=cv2.rectangle(frame,(blueplt['x1'],blueplt['y1']),
                              (blueplt['x2'],blueplt['y2']),
                              (255,0,0),-1)

    frame[EraserBox['y1']:EraserBox['y2'],EraserBox['x1']:EraserBox['x2']]=eraser

    lmList = detector.findPosition(img, draw= False)
    j=1
    
    

    if len(lmList)> 10:

        if abs(lmList[8][1]-lmList[5][1])>25:
            fingerX.append([lmList[8][1],lmList[8][2]])

    for i in range(1,len(fingerX)-1):
        
            
        frame= cv2.line(frame,(fingerX[j-1][0],fingerX[j-1][1]),
        (fingerX[j][0],fingerX[j][1])
        ,color,5)

    #cv2.line(img,(0,0),(511,511),(255,0,0),5)

        j+=1


       # print(fingerX)
    try:   
        if EraserBox['x1']<lmList[8][1]<EraserBox['x2'] and EraserBox['y1']<lmList[8][2]<EraserBox['y2'] :
            fingerX=[]
        if redplt['x1']<lmList[8][1]<redplt['x2'] and redplt['y1']<lmList[8][2]<redplt['y2'] :
            color=(0,0,255)
        if blueplt['x1']<lmList[8][1]<blueplt['x2'] and blueplt['y1']<lmList[8][2]<blueplt['y2'] :
            color=(255,0,0)
    except :
        None
    
# cv2.add(frame,eraser)
    cv2.imshow("image", frame)
    #cv2.imshow('de',eraser)

    if cv2.waitKey(1) == ord("q"):
        break
#cv2.imshow('de',eraser)
cv2.destroyAllWindows()
cap.release()
