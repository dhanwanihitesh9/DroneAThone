import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def findRedRings(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges using Canny edge detection
    edges = cv2.Canny(blurred, threshold1=30, threshold2=100)

    # Find contours in the edge image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize a variable to count the loops
    loop_count = 0

    # Loop through detected contours
    for contour in contours:
        # Approximate the contour to simplify it
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the contour is closed and has a sufficient number of vertices
        if len(approx) >= 6 and cv2.isContourConvex(approx):
            # Draw the contour on the original image
            cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
            loop_count += 1

    return

while True:
    _, img = cap.read()
    findRedRings(img)
    cv2.imshow("Output", img)
    cv2.waitKey(1)