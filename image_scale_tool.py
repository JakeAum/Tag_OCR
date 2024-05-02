# this is a tool that allows me to measure a distance in an image relative to a known scale bar

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def main():
    # use file dialog to get the image
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename()


    # get the scale bar length
    scale_bar_length_Cm = float(input('Enter the scale bar length in [Cm]: '))

    # read the image
    image = cv2.imread(image_path)

    # shrink the image by 0.5
    #image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

    # get the coordinates of two points clicked by the user
    points = []
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            if len(points) == 2:
                cv2.line(image, points[0], points[1], (0, 255, 0), 5)
                cv2.imshow('image', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            elif len(points) == 4:
                cv2.line(image, points[2], points[3], (0, 0, 255), 5)
                cv2.imshow('image', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                # calculate the distance in pixels between the two points
                scale_bar_length_px = np.sqrt((points[1][0] - points[0][0])**2 + (points[1][1] - points[0][1])**2)
                measured_distance_px = np.sqrt((points[3][0] - points[2][0])**2 + (points[3][1] - points[2][1])**2)

                # calculate the distance in real world units
                ratio = scale_bar_length_Cm / scale_bar_length_px
                measured_distance = measured_distance_px * ratio


                print(f"The distance between the two points is {measured_distance} [Cm]")
                # draw the distance of the scale bar over the line in green
                cv2.putText(image, f"Scale Bar: {scale_bar_length_Cm} cm", (points[0][0], points[0][1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255, 255), 2)

                # draw the distance of the measurement over the red bar in green
                cv2.putText(image, f"Measurement: {round(measured_distance,3)} cm", (points[2][0], points[2][1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                cv2.imshow('image', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                # save the image
                output_path = image_path.strip(".png")+ "_annotated.jpg"

                cv2.imwrite(output_path, image)
                print(f"Image saved as {output_path}")
                exit()

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mouse_callback)

    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




if __name__ == '__main__':
    main()