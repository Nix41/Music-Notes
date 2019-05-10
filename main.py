import argparse
import cv2
from GetLines import process
from GetStaffs import staffs
from GetNotes import detect_notes
from DefineNotes import extract_notes, draw_notes_pitch
import numpy as np
from play import play_notes


def musical_notes(path, min_note, max_note):
    image = cv2.imread(path)
    all_lines, lines_image_color, adjusted = process(image)
    cv2.imwrite('output/Adjust.png', adjusted)
    ad2 = adjusted.copy()
    stfs = staffs(all_lines, lines_image_color)
    notes = detect_notes(adjusted, stfs, min_note, max_note)
    defined = extract_notes(notes, stfs, adjusted)
    draw_notes_pitch(ad2, defined)
    return defined

