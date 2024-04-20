import cv2
import numpy as np

images_list = ['test_img\\USDA_1.png', 'test_img\\USDA_3.png']   

HSV_list = []
radius = 10  # Set the initial radius of the paint tool

def on_mouse_drag(event, x, y, flags, param):
    global radius
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            radius = min(radius + 1, 30)  # Increase radius by 1, capped at 12
        else:
            radius = max(radius - 1, 5)  # Decrease radius by 1, capped at 1

    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_LBUTTONUP or event == cv2.EVENT_MOUSEMOVE:
        if flags == cv2.EVENT_FLAG_LBUTTON:
            cv2.circle(image, (x, y), radius, (0, 0, 255), -1)
            hsv_value = hsv_image[y, x]
            HSV_list.append(hsv_value)
            
for image in images_list:
    # Load the image
    image = cv2.imread(image)

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create a window and set the mouse callback function
    cv2.namedWindow("HSV Color Picker")
    cv2.setMouseCallback("HSV Color Picker", on_mouse_drag)

    while True:
        cv2.imshow("HSV Color Picker", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()

# Calculate the min and max HSV values
HSV_list = np.array(HSV_list)
min_HSV = np.min(HSV_list, axis=0)
max_HSV = np.max(HSV_list, axis=0)

print("#####################")
print(f"Min HSV: {min_HSV}")
print(f"Max HSV: {max_HSV}")
print("#####################")