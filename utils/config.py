from enum import Enum

import numpy as np

CELL_SIZE = 30
WIDTH = CELL_SIZE *  30
HEIGHT = CELL_SIZE * 30

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __len__(self):
        return 4

    def go_straight(self, position):
        next_position = np.copy(position)
        if self is Direction.UP:
            next_position[1] -= CELL_SIZE
        if self is Direction.RIGHT:
            next_position[0] += CELL_SIZE
        if self is Direction.DOWN:
            next_position[1] += CELL_SIZE
        if self is Direction.LEFT:
            next_position[0] -= CELL_SIZE
        return next_position
