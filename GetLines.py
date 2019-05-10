
import cv2
import numpy as np

def process(image):
    gray = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (11,11), 0)
    edged = cv2.Canny(blur, 0, 50)
    cv2.imwrite("output/1canny.jpg", edged)
    contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    dst = photo(image.copy(),contours)
    cop = gray.copy()
    cop2 = gray.copy()
    e, t, res = straight(dst, image.copy(),contours)
    e1,t2,res2 = straight(image.copy(), image.copy(),contours)
    h2 = cv2.HoughLines(e, 1, np.pi/150, 200)
    # Maybe the picture is a clean image of a partiture
    h = cv2.HoughLines(e1, 1, np.pi/ 150, 200)
    if h2 is None: # if it is not a photo
        a, b = detect_lines(h, gray, 80)
        r = res2
    else: # if it is
        a, b = detect_lines(h2, t, 80)
        r = res
    return a, b, r

def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

THRESHOLD_MIN = 160
THRESHOLD_MAX = 255

def photo(image, contours):
    for cnt in contours:
        # Douglas Pecker algorithm - reduces the number of points in a curve
        epsilon = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * epsilon, True)
        if len(approx) == 4:
            sheet = approx
            break
    approx = np.asarray([x[0] for x in sheet.astype(dtype=np.float32)])
    # top_left has the smallest sum, bottom_right has the biggest
    top_left = min(approx, key=lambda t: t[0] + t[1])
    bottom_right = max(approx, key=lambda t: t[0] + t[1])
    top_right = max(approx, key=lambda t: t[0] - t[1])
    bottom_left = min(approx, key=lambda t: t[0] - t[1])
    max_width = int(max(distance(bottom_right, bottom_left), distance(top_right, top_left)))
    max_height = int(max(distance(top_right, bottom_right), distance(top_left, bottom_left)))
    arr = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")
    rectangle = np.asarray([top_left, top_right, bottom_right, bottom_left])
    m = cv2.getPerspectiveTransform(rectangle, arr)
    dst = cv2.warpPerspective(image, m, (max_width, max_height))
    return dst
LINES_DISTANCE_THRESHOLD = 50
LINES_ENDPOINTS_DIFFERENCE = 10

def detect_lines(hough, image, nlines):
    all_lines = set()
    width, height = image.shape
    # convert to color image so that you can see the lines
    lines_image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for result_arr in hough[:nlines]:
        rho = result_arr[0][0]
        theta = result_arr[0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        shape_sum = width + height
        x1 = int(x0 + shape_sum * (-b))
        y1 = int(y0 + shape_sum * a)
        x2 = int(x0 - shape_sum * (-b))
        y2 = int(y0 - shape_sum * a)
        start = (x1, y1)
        end = (x2, y2)
        diff = y2 - y1
        if abs(diff) < LINES_ENDPOINTS_DIFFERENCE:
            all_lines.add(int((start[1] + end[1]) / 2))
            cv2.line(lines_image_color, start, end, (0, 0, 255), 2)
    cv2.imwrite("output/5lines.png", lines_image_color)
    return all_lines, lines_image_color

def straight(dst1, image,contours):
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    cv2.imwrite("output/2with_contours.png", image)
    dst = cv2.cvtColor(dst1, cv2.COLOR_BGR2GRAY)
    _, result = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("output/3adjusted_photo.png", result)
    rcop = result.copy()
    _, thresholded1 = cv2.threshold(rcop, THRESHOLD_MIN, THRESHOLD_MAX, cv2.THRESH_BINARY)
    element = np.ones((3, 3))
    thresholded2 = cv2.erode(thresholded1, element)
    edges = cv2.Canny(thresholded2, 10, 100, apertureSize=3)
    return edges, thresholded2, result
