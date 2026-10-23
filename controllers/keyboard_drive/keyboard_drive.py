#This is my code for an autonomous car simulator.
#Imports:
from vehicle import Driver
from controller import Keyboard

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
speed = 0
steering = 0
print_time = 1.0
print(f"keyboard_drive started, time step: {time_step}ms")

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
