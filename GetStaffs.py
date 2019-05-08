
import cv2
import numpy as np

class Staff:
    def __init__(self, min_range, max_range):
        self.min_range = min_range
        self.max_range = max_range
        self.lines_location, self.lines_distance = self.get_lines_locations()

    def get_lines_locations(self):
        lines = []
        lines_distance = int((self.max_range - self.min_range) / 4)
        for i in range(5):
            lines.append(self.min_range + i * lines_distance)
        return lines, lines_distance


LINES_DISTANCE_THRESHOLD = 50

def detect_staffs(all_lines):
    print("Detecting staffs.")
    staffs = []
    lines = []
    all_lines = sorted(all_lines)
    for current_line in all_lines:
        # If current line is far away from last detected line
        if lines and abs(lines[-1] - current_line) > LINES_DISTANCE_THRESHOLD:
            if len(lines) >= 5:
                # Consider it the start of the next staff.
                # If <5 - not enough lines detected. Probably an anomaly - reject.
                staffs.append((lines[0], lines[-1]))
            lines.clear()
        lines.append(current_line)
    # Process the last line
    if len(lines) >= 5:
        if abs(lines[-2] - lines[-1]) <= LINES_DISTANCE_THRESHOLD:
            staffs.append((lines[0], lines[-1]))
    return staffs

def draw_staffs(image, staffs):
    # Draw the staffs
    width = image.shape[0]
    for staff in staffs:
        cv2.line(image, (0, staff[0]), (width, staff[0]), (0, 255, 255), 2)
        cv2.line(image, (0, staff[1]), (width, staff[1]), (0, 255, 255), 2)
    cv2.imwrite("output/6staffs.png", image)

def staffs(lines, color_lines):
    s = detect_staffs(lines)
    draw_staffs(color_lines, s)
    return [Staff(staff[0], staff[1]) for staff in s]

