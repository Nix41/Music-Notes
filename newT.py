
import cv2

filename = 'input/test/part3.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("output/1Gray.jpg", gray)

cop1 = img.copy()
thres = cv2.adaptiveThreshold(cop1,255 ,cv2.CV_A , cv2.THRESH_BINARY, 15,-2 )
cv2.imwrite("output/2Thres.jpg", thres)


