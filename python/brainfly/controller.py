import numpy as np


class PlayerController:

    def __init__(self):
        self.pos = 0.5

    def move(self, prediction):
        prediction = prediction - 0.5
        self.pos += prediction * 0.05
        print(self.pos)
        self.pos = np.clip(self.pos, 0, 1)
        return self.pos
