import cv2
import numpy as np



# Load the image
# image = cv2.imread('/Users/hiteshdhanwani/PycharmProjects/Tello_Course/Resources/Images/circle/Circle'+str(i)+'.jpg')
image = cv2.imread('/Users/hiteshdhanwani/PycharmProjects/Tello_Course/Resources/Images/circle/Circle54.jpg')

imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([30, 150, 50], dtype="uint8")
upper = np.array([255, 255, 180], dtype="uint8")
# lower = np.array([22, 93, 0], dtype="uint8")
# upper = np.array([45, 255, 255], dtype="uint8")
maskImage = cv2.inRange(imageHSV, lower, upper)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(maskImage, (9, 9), 2)

circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1,  # Inverse ratio of accumulator resolution
    minDist=100,  # Minimum distance between detected centers
    param1=100,  # Upper threshold for the internal Canny edge detector
    param2=80,  # Threshold for center detection
    minRadius=10,  # Minimum radius
    maxRadius=1000  # Maximum radius
)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for circle in circles[0, :]:
        center = (circle[0], circle[1])
        radius = circle[2]
        # Draw the circle
        cv2.circle(image, center, radius, (0, 255, 0), 5)
        cv2.circle(image, center, 5, (0, 255, 0), 5)
        print(circle)

# Display the image with detected circles
cv2.imshow('Detected Circles ', image)
cv2.imshow('Masked Image ', maskImage)
cv2.waitKey(0)


