#SAFE DRIVER
#Drives the loop by itself: the camera keeps the lane, the GPS and compass steer through the junctions,
#and the lidar and the crossing zones decide the speed. The up/down arrows set the top speed you allow.
#Imports:
import math
from vehicle import Driver
from controller import Keyboard
import cv2
import junctions
import safety
import steering
import vision

#SETTINGS:
MAX_SPEED = 30 #(kmph)
SPEED_STEP = 0.1 #(kmph per tick and 1 tick = 10ms)
MAX_STEERING = 0.5 #(rad)
KP = 1.0 #(rad of steering per unit of line error)
KD = 0.0 #(rad of steering per unit of error change per second; 0 = P control only)

#SETUP
driver = Driver()
time_step = int(driver.getBasicTimeStep())
dt = time_step / 1000 #(seconds per tick)
keyboard = driver.getKeyboard()
keyboard.enable(time_step)
gps = driver.getDevice("gps")
gps.enable(time_step)
compass = driver.getDevice("compass")
compass.enable(time_step)
camera = driver.getDevice("camera")
camera.enable(time_step)
lidar = driver.getDevice("Sick LMS 291")
lidar.enable(time_step)
pd = steering.PDController(KP, KD)
watch = safety.ObstacleWatch()
speed_limit = 0 #(kmph) the top speed you allow with the arrow keys; 0 = wait at the start
steering_angle = 0.0
error = 0.0
print_time = 1.0
last_x = vision.TARGET_LINE_X
print(f"safe_driver started, time step: {time_step}ms, KP={KP}, KD={KD}. Hold the up arrow to set a top speed.")

while driver.step() != -1:
    #SENSE: speed keys, GPS, compass, camera and lidar
    key = keyboard.getKey()
    while key != -1:
        if key == Keyboard.UP:
            speed_limit += SPEED_STEP
        elif key == Keyboard.DOWN:
            speed_limit -= SPEED_STEP
        key = keyboard.getKey()
    x, y, _ = gps.getValues()
    car_heading = junctions.heading(compass)
    image = vision.camera_to_array(camera)
    mask = vision.yellow_mask(image)
    line_x = vision.line_position(mask, last_x)
    crossing = vision.is_crossing(mask)
    distance = safety.distance_ahead(lidar.getRangeImage(), lidar.getFov())

    #THINK, steering: GPS in a junction zone; otherwise the line, or hold the last steering when it can't be trusted
    aim = junctions.junction_exit(x, y)
    if aim is not None:
        steering_angle = junctions.steer_to_point(x, y, car_heading, aim)
        pd.reset()
    elif crossing or line_x is None:
        pd.reset()
    else:
        error = line_x - vision.TARGET_LINE_X
        steering_angle = pd.update(error, dt)

    #remember where the line was, for next tick's search window
    if crossing:
        pass
    elif line_x is None:
        last_x = vision.TARGET_LINE_X
    else:
        last_x = line_x

    #THINK, speed: stop for an obstacle in the lane, slow down near crossings, never above your top speed
    blocked = watch.update(distance)
    near_crossing = safety.near_any(x, y, safety.CROSSINGS, safety.CROSSING_RADIUS)
    state, target_speed = safety.choose_speed(blocked, near_crossing)
    speed_limit = steering.clamp(speed_limit, 0, MAX_SPEED)
    speed = min(target_speed, speed_limit)

    #ACT: send speed and steering to the car
    steering_angle = steering.clamp(steering_angle, -MAX_STEERING, MAX_STEERING)
    driver.setCruisingSpeed(speed)
    driver.setSteeringAngle(steering_angle)

    #once a second: print what the car sees and does, and save the pictures
    if driver.getTime() >= print_time:
        if line_x is None:
            line_text = "none"
        else:
            line_text = f"{line_x:.2f}"
        if aim is None:
            steer_by = "line"
        else:
            steer_by = "GPS"
        print(f"t={driver.getTime():.0f} x={x:.1f} y={y:.1f} heading={math.degrees(car_heading):.0f} "
              f"speed={driver.getCurrentSpeed():.1f}/{speed:.0f} state={state} ahead={distance:.1f} "
              f"steer_by={steer_by} line_x={line_text} crossing={crossing} steering={steering_angle:+.2f}")
        camera.saveImage(f"../../runs/frames/frame_{int(driver.getTime())}.png", 100)
        cv2.imwrite(f"../../runs/frames/mask_{int(driver.getTime())}.png", mask)
        print_time += 1.0
