#/usr/bin/env python
import numpy as np
import cv2

img = cv2.imread('robot.jpg',0)
# cv2의 첫번째 argument는 사진의 이름, 두번째 argument는 색을 지정-> 0보다 크면 RGB컬러, 0이면 흑백
cv2.imshow('image', img)
cv2.waitKey(0)
#cv2.watikey는 단축키 함수, argument는 밀리초의 시간, 만약 argument가 0이면 무기한으로 key stroke를 기다림
cv2.destroyAllWindows()
#모든 창 닫기

