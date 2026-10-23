"""Decides how fast the car may go: stop for obstacles in its lane, slow down near zebra crossings."""

import math

#SETTINGS:
CITY_SPEED = 30 #(kmph) WHO's limit for streets shared with people, same as ChowkCheck
CROSSING_SPEED = 20 #(kmph)
CROSSINGS = [(-61.46, 45.07), (45, -26)] #(m) zebra crossings B and A
CROSSING_RADIUS = 30 #(m) slow down this close to a crossing
STOP_DISTANCE = 12 #(m) stopping from 30 kmph takes about 9 m
LANE_HALF_WIDTH = 1.5 #(m) the lidar only counts things this close to the car's path
MIN_RANGE = 1.0 #(m) ignore readings closer than this: the car's own body or the road when the nose dips
SEEN_STEPS = 20 #(ticks) stop only after an obstacle has been seen for 0.2 s
CLEAR_STEPS = 100 #(ticks) drive on only after the lane has been clear for 1 s


#distance_ahead - how far ahead the nearest thing in the car's own lane is, or math.inf:
def distance_ahead(ranges, fov):
    nearest = math.inf
    count = len(ranges)
    for i in range(count):
        distance = ranges[i]
        if math.isinf(distance) or distance < MIN_RANGE:
            continue
        angle = -fov / 2 + i * fov / (count - 1)
        side = distance * math.sin(angle)
        ahead = distance * math.cos(angle)
        if abs(side) <= LANE_HALF_WIDTH and ahead < nearest:
            nearest = ahead
    return nearest


#near_any - True if the car is within radius of any of the points:
def near_any(x, y, points, radius):
    for point in points:
        if math.dist((x, y), point) < radius:
            return True
    return False


#choose_speed - the state and the speed for it:
def choose_speed(blocked, near_crossing):
    if blocked:
        return "STOP", 0
    elif near_crossing:
        return "SLOW", CROSSING_SPEED
    else:
        return "DRIVE", CITY_SPEED


#ObstacleWatch - turns the lidar distance into blocked / not blocked, without flickering:
class ObstacleWatch:
    def __init__(self):
        self.seen_steps = 0
        self.clear_steps = 0
        self.blocked = False

    def update(self, distance):
        if distance < STOP_DISTANCE:
            self.seen_steps += 1
            self.clear_steps = 0
        else:
            self.clear_steps += 1
            self.seen_steps = 0
        if self.seen_steps >= SEEN_STEPS:
            self.blocked = True
        elif self.clear_steps >= CLEAR_STEPS:
            self.blocked = False
        return self.blocked
