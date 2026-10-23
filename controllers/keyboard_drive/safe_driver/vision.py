"""Turns camera pictures into numbers the car can steer by."""

import numpy as np
import cv2

YELLOW_LOW = (20, 100, 100)
YELLOW_HIGH = (35, 255, 255)
BAND_TOP = 80
BAND_BOTTOM = 110
CROSSING_COVERAGE = 0.5
TARGET_LINE_X = 0.30
SEARCH_WINDOW = 0.12
MIN_LINE_PIXELS = 50


def camera_to_array(camera):
    raw = camera.getImage()
    width = camera.getWidth()
    height = camera.getHeight()
    pixels = np.frombuffer(raw, dtype=np.uint8)
    image = pixels.reshape((height, width, 4))
    return image[:, :, :3]

def yellow_mask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, YELLOW_LOW, YELLOW_HIGH)

def is_crossing(mask):
    band = mask[BAND_TOP:BAND_BOTTOM]
    if band.any(axis=0).mean() > CROSSING_COVERAGE:
        return True
    else:
        return False

def line_position(mask, last_x):
    band = mask[BAND_TOP:BAND_BOTTOM]
    rows, columns = np.nonzero(band)
    positions = columns / mask.shape[1]
    if last_x is not None:
        near = np.abs(positions - last_x) <= SEARCH_WINDOW
        positions = positions[near]
    if len(positions) < MIN_LINE_PIXELS:
        return None
    return positions.mean()