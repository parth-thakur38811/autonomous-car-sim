"""Turns camera pictures into numbers the car can steer by."""

import numpy as np


def camera_to_array(camera):
    raw = camera.getImage()
    width = camera.getWidth()
    height = camera.getHeight()
    pixels = np.frombuffer(raw, dtype=np.uint8)
    image = pixels.reshape((height, width, 4))
    return image[:, :, :3]