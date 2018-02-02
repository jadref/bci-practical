"""
Implementation of the movement-based-decoder
"""
import numpy as np


class PlayerController:
    """Takes a prediction from the classifier as input and updates the position
    The self.desired_position should be used to control the player
    """
    def __init__(self, max_speed=0.05):
        self.max_speed = max_speed
        self.desired_position = 0.5

    def move(self, prediction):
        prediction = prediction - 0.5
        self.desired_position = self.desired_position + self.max_speed * prediction
        self.desired_position = np.clip(self.desired_position, 0, 1)


class ProbablisticConroller:
    """Controller which disregards the prediction and moves to
    the correct side with a certain probability.
    """
    def __init__(self, alpha=0.05):
        self.alpha = alpha
        self.desired_position = 0.5
        self.target_position = 1

    def move(self, prediction):
        prediction = np.random.normal(0.385, 1)
        self.desired_position = self.desired_position + self.alpha * prediction * self.target_position
        self.desired_position = np.clip(self.desired_position, 0, 1)
