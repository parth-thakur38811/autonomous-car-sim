#SAFE DRIVER
#This is my code for an autonomous car simulator.
#Imports:
from vehicle import Driver
from controller import Keyboard
import vision
import cv2

#SETTINGS:
MAX_SPEED = 30 #(kmph)
SPEED_STEP = 0.1 #(kmph per tick and 1 tick = 10ms)
MAX_STEERING = 0.5 #(rad)
STEERING_STEP = 0.01 #(rad per tick and 1 tick = 10ms)

#clamp function - keeping the speed and turn within range:
def clamp(value, low, high):
    if value < low:
        return low
    elif value > high:
        return high
    else:
        return value

#SETUP
driver = Driver()
time_step = int(driver.getBasicTimeStep())
keyboard = driver.getKeyboard()
keyboard.enable(time_step)
gps = driver.getDevice("gps")
gps.enable(time_step)
camera = driver.getDevice("camera")
camera.enable(time_step)
speed = 0
steering = 0
print_time = 1.0
last_x = vision.TARGET_LINE_X
print(f"safe_drive started, time step: {time_step}ms")

while driver.step() != -1:
    steered = False
    key = keyboard.getKey()
    while key != -1:
        if key == Keyboard.UP:
            speed += SPEED_STEP
        elif key == Keyboard.DOWN:
            speed -= SPEED_STEP
        elif key == Keyboard.LEFT:
            steered = True
            steering -= STEERING_STEP
        elif key == Keyboard.RIGHT:
            steered = True
            steering += STEERING_STEP
        key = keyboard.getKey()
    if not steered:
        steering = steering * 0.9
    speed = clamp(speed, 0, MAX_SPEED)
    steering = clamp(steering, -MAX_STEERING, MAX_STEERING)
    driver.setCruisingSpeed(speed)
    driver.setSteeringAngle(steering)
    image = vision.camera_to_array(camera)
    mask = vision.yellow_mask(image)
    line_x = vision.line_position(mask, last_x)
    crossing = vision.is_crossing(mask)
    if driver.getTime() >= print_time:
        coordinates = gps.getValues()
        x = coordinates[0]
        y = coordinates[1]
        z = coordinates[2]
        print(f"t={driver.getTime()}; x={x:.1f}, y={y:.1f}, z={z:.1f}; target vel = {speed}, current vel={driver.getCurrentSpeed()}")
        filename = f"../../runs/frames/frame_{driver.getTime()}.png"
        camera.saveImage(filename, 100)
        try:
            print(f"line_x={line_x:.2f}, crossing={crossing}")
        except(TypeError):
            print("line_x= none")
        cv2.imwrite(f"../../runs/frames/mask_{int(driver.getTime())}.png", mask)
        print_time += 1.0
    if crossing:
        pass
    elif line_x is None:
        last_x = vision.TARGET_LINE_X
    else:
        last_x = line_x