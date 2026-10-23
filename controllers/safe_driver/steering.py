"""Turns the line error into a steering angle."""


#clamp function - keeping the speed and turn within range:
def clamp(value, low, high):
    if value < low:
        return low
    elif value > high:
        return high
    else:
        return value


#PD controller - steers by how far off the line is (P) and how fast that is changing (D):
class PDController:
    def __init__(self, kp, kd):
        self.kp = kp
        self.kd = kd
        self.previous_error = None

    def update(self, error, dt):
        if self.previous_error is None:
            change = 0.0
        else:
            change = (error - self.previous_error) / dt
        self.previous_error = error
        return self.kp * error + self.kd * change

    def reset(self):
        self.previous_error = None
