
def process(image):
    # Gray scale of the image, better contrast
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cv2.imwrite("output/1Gray.jpg", gray)
    kernel_size = 11
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    low_threshold = 50
    high_threshold = 150
    # Find edges of the images
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
    cv2.imwrite("output/2Canny.jpg", edges)
    cop = image.copy()
    # Treat the image as a picture of a sheet
    e, t = photo(cop)
    h2 = cv2.HoughLines(e, 1, np.pi/150, 200)
    # Maybe the picture is a clean image of a partiture
    h = cv2.HoughLines(edges, 1, np.pi/ 150, 200)
    if h2 is None: # if it is not a photo
        a, b = detect_lines(h, gray, 80)
        r = edges
    else: # if it is
        a, b = detect_lines(h2, t, 80)
        r = e
    return a, b, r


