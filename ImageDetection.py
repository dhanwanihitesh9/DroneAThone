import cv2
import numpy as np

i = 1
while i < 31:

    # Load the image
    image = cv2.imread('/Users/hiteshdhanwani/PycharmProjects/Tello_Course/Resources/Images/image'+str(i)+'.jpg')

    # Define grid parameters
    grid_size = (50, 50)  # Adjust the size of the grid squares as needed
    grid_color = (0, 255, 0)  # Green color in BGR format
    marker_radius = 5
    marker_color = (0, 0, 255)  # Red color in BGR format

    # Calculate grid coordinates and draw markers
    for y in range(0, image.shape[0], grid_size[1]):
        for x in range(0, image.shape[1], grid_size[0]):
            cv2.circle(image, (x, y), marker_radius, marker_color, -1)  # -1 for filled circle
            cv2.putText(image, "x:"+str(x)+",y:"+str(y), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.2,
                        (0, 255, 0), 1, cv2.LINE_AA, False)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,  # Inverse ratio of accumulator resolution
        minDist=110,  # Minimum distance between detected centers
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
            cv2.circle(image, center, radius, (0, 255, 0), 2)
            cv2.circle(image, center, 2, (0, 255, 0), 2)
            print(circle)

    # Display the image with detected circles
    cv2.imshow('Detected Circles '+str(i), image)
    cv2.waitKey(0)
    i = i+1
    print(i)

