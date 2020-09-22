#!/usr/bin/env python
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
#VideoCapture의 argument는 카메라 번호 또는 비디오 파일 이름으로 한다.
while(True):
    #Capture frame-by-frame
    ret, frame = cap.read()
    #Displat the resulting frame
    cv2.imshow('frame',frame)
    k = cv2.waitKey(30)
    if k > 0:
        break
#위의 코드는 image frames를 반복적으로 읽고, 어느 키가 눌리면 종료
