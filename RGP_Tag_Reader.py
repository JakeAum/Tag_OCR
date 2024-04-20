# Jacob Auman
# 4/19/2024

# A tool to help the RGP Pilot Speed Up the Process of Reading Tags

import numpy as np
import cv2
import easyocr


def showFrame(img):
    cv2.imshow('Image', img)
    cv2.waitKey(500)


# Load the image
img = cv2.imread('test_img\\USDA_1.png')
#img = cv2.imread('test_img\\USDA_3.png')

'''Image Processing'''
showFrame(img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
showFrame(gray)

# convert image to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# mask off the tag -> from HSV Color Picker
lower = np.array([97, 83, 79])
upper = np.array([113, 255, 255])

mask = cv2.inRange(hsv, lower, upper)
showFrame(mask)

# contour detection
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   
largest_contour = max(contours, key=cv2.contourArea)

# draw the contour as white on a black background
mask = np.zeros_like(mask)
cv2.drawContours(mask, [largest_contour], -1, (255), -1)
showFrame(mask)

kernel = np.ones((5,5), np.uint8)
mask = cv2.erode(mask, kernel, iterations=2)
showFrame(mask)

# contour detection
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
largest_contour = max(contours, key=cv2.contourArea)

# draw the contour as white on a black background
mask = np.zeros_like(mask)
cv2.drawContours(mask, [largest_contour], -1, (255), -1)
showFrame(mask)

# minimum area rectangle
rect = cv2.minAreaRect(largest_contour)
box = cv2.boxPoints(rect)
box = np.intp(box)
cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
showFrame(img)

# convex hull
hull = cv2.convexHull(largest_contour)
cv2.drawContours(img, [hull], 0, (255, 0, 0), 2)
showFrame(img)

# simplify countour
epsilon = 0.05*cv2.arcLength(hull, True)
approx = cv2.approxPolyDP(hull, epsilon, True)
cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)
showFrame(img)

#check if the simplified contour is a quadrilateral
if len(approx) == 4:
    print('Quadrilateral')
else:
    raise ValueError('Simplified Contour not Quadrilateral')

# Transform the Image so that the quadrilateral becomes a rectangle
pts1 = np.float32(approx)

# Calculate the dimensions of the quadrilateral
width = np.linalg.norm(approx[0] - approx[1])
height = np.linalg.norm(approx[1] - approx[2])

# Set the points of the desired rectangle based on the dimensions of the quadrilateral
pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
img = cv2.warpPerspective(img, matrix, (int(width), int(height)))

# Resize the image
img = cv2.resize(img, (int(width*2), int(height*2)))
showFrame(img)

'''Easy OCR'''
# apply the easy ocr to the image
reader = easyocr.Reader(['en'])
result = reader.readtext(img)
print(result)

# Draw the bounding boxes
for detection in result:
    top_left = tuple([int(val) for val in detection[0][0]])
    bottom_right = tuple([int(val) for val in detection[0][2]])
    text = detection[1]
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.rectangle(img, top_left, bottom_right, (0,0,255), 1)
    img = cv2.putText(img, text, top_left, font, 1, (255,0,0), 2, cv2.LINE_AA)

# Extract the text from the OCR results and concatenate them together
text = ' '.join([detection[1] for detection in result])

# Print the concatenated text
print(text)

cv2.imshow('Image', img)
cv2.waitKey(0)

# Shut Down
try:
    cv2.waitKey(0)
    cv2.destoryAllWindows()
except:
    pass