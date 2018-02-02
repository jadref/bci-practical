import numpy as np


class PlayerController:

    def __init__(self, max_speed=0.05):
        self.max_speed = max_speed
        self.desired_position = 0.5

    def move(self, prediction):
        prediction = prediction - 0.5
        self.desired_position = self.desired_position + self.max_speed * prediction
        self.desired_position = np.clip(self.desired_position, 0, 1)


class ProbablisticConroller:

    def __init__(self, alpha=0.05):
        self.alpha = alpha
        self.desired_position = 0.5
        self.target_position = 1

    def move(self, prediction):
        prediction = np.random.normal(0.4, 0.4)
        self.desired_position = self.desired_position + self.alpha * prediction * self.target_position
        self.desired_position = np.clip(self.desired_position, 0, 1)