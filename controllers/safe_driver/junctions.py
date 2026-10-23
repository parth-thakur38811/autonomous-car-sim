"""Steers through the two junctions, where the road lines stop, using the GPS and compass."""

import math

#SETTINGS: (junction centre, point to aim for on the far side), in metres
JUNCTIONS = [((-45, 45), (-60, 47.7)),
             ((45, -45), (47.7, -30))]
JUNCTION_RADIUS = 16 #(m) steer by GPS this close to a junction's centre
AIM_REACHED = 3 #(m) stop aiming this close to the aim point; any closer, the direction to it swings round


#heading - which way the car points, in radians: 0 = east, pi/2 = north, pi or -pi = west, -pi/2 = south
def heading(compass):
    x, y, _ = compass.getValues()
    return math.atan2(x, y)


#junction_exit - the point to aim for if the car is in a junction zone, otherwise None:
def junction_exit(x, y):
    for centre, aim in JUNCTIONS:
        if math.dist((x, y), centre) < JUNCTION_RADIUS and math.dist((x, y), aim) > AIM_REACHED:
            return aim
    return None


#steer_to_point - the steering angle that turns the car towards the target:
def steer_to_point(x, y, car_heading, target):
    target_angle = math.atan2(target[1] - y, target[0] - x)
    difference = target_angle - car_heading
    difference = (difference + math.pi) % (2 * math.pi) - math.pi
    return -difference
