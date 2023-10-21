import cv2
import numpy as np

def findTarget(img):

    # Load the template image (the object to be found)
    template = cv2.imread('Resources/DronathoneResources/redloopbgless.png')

    # Convert both images to grayscale
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    main_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    # Define a range of template matching parameters to search over
    methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
    results = {}

    # Perform the grid search
    for method in methods:
        result = cv2.matchTemplate(main_gray, template_gray, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            match_val = min_val
        else:
            match_val = max_val

        results[method] = match_val

    # Find the best matching method based on the results
    best_method = min(results, key=results.get)

    # Display the best matching result
    result_image = main_image.copy()
    if best_method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    h, w = template_gray.shape
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(result_image, top_left, bottom_right, (0, 255, 0), 2)

    return img

cap = cv2.VideoCapture(0)
while True:
    _, img = cap.read()
    img2 = findTarget(img)
    cv2.imshow("Output", img2)
    cv2.waitKey(1)