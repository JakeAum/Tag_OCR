# Jacob Auman
# 4/19/2024

# Lets learn OCR :) in python

import numpy as np
import cv2
import easyocr

def showFrame(img):
    cv2.imshow('Image', img)
    cv2.waitKey(500)

# Load the image
img = cv2.imread('test_img\Hello_World.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
showFrame(gray)

# apply the easy ocr to the image
reader = easyocr.Reader(['en'])
result = reader.readtext(gray)
# print(result)

# Draw the bounding boxes
for detection in result:
    top_left = tuple([int(val) for val in detection[0][0]])
    bottom_right = tuple([int(val) for val in detection[0][2]])
    text = detection[1]
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.rectangle(img, top_left, bottom_right, (0,0,255), 1)
    img = cv2.putText(img, text, top_left, font, 1, (255,0,0), 2, cv2.LINE_AA)
    showFrame(img)


# Shut Down
try:
    cv2.destoryAllWindows()
except:
    pass