import cv2
import numpy as np

def findTarget(img):
    # Convert both images to grayscale
    template = cv2.imread('Resources/DronathoneResources/redloopbgless.png')
    main_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Create a SIFT detector
    sift = cv2.SIFT.create()

    # Find the key points and descriptors in both images
    keypoints_main, descriptors_main = sift.detectAndCompute(main_gray, None)
    keypoints_template, descriptors_template = sift.detectAndCompute(template_gray, None)

    # Create a Brute-Force Matcher
    bf = cv2.BFMatcher()

    # Match the descriptors
    matches = bf.knnMatch(descriptors_template, descriptors_main, k=2)

    # Apply a ratio test to keep good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Draw the matches on the main image
    result_image = cv2.drawMatches(template, keypoints_template, img, keypoints_main, good_matches, None,
                                   flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    return img

cap = cv2.VideoCapture(0)
while True:
    _, img = cap.read()
    img2 = findTarget(img)
    cv2.imshow("Output", img2)
    cv2.waitKey(1)