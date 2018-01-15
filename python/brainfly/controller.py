import numpy as np


class PlayerController:

    def __init__(self, alpha=0.05):
        self.alpha = alpha
        self.desired_position = 0.5

    def move(self, prediction):
        prediction = prediction - 0.5
        self.desired_position = self.desired_position + self.alpha * prediction
        self.desired_position = np.clip(self.desired_position, 0, 1)
