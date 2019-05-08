import argparse
import cv2
from GetLines import process
from GetStaffs import staffs
from GetNotes import detect_notes
import numpy as np

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--input',
        default='input/good/dark2.jpg'
    )
    return parser.parse_args()


def circles(image):
    img = cv2.medianBlur(image,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
    param1=50,param2=30,minRadius=50,maxRadius=200)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    cv2.imwrite("output/circless.jpg", cimg)

def main():
    args = parse()
    image = cv2.imread(args.input)
    print(args.input)
    all_lines, lines_image_color, adjusted = process(image)
    stfs = staffs(all_lines, lines_image_color)
    notes = detect_notes(adjusted, stfs)

main()
