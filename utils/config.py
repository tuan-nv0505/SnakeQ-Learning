from enum import Enum

import numpy as np

CELL_SIZE = 30
WIDTH = CELL_SIZE *  30
HEIGHT = CELL_SIZE * 30

def get_action(index):
    if index not in [0, 1, 2]:
        raise IndexError("index khong hop le.")
    return index - 1

def get_index(action):
    if action not in [-1, 0, 1]:
        raise ValueError("action khong hop le.")
    return action + 1

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __len__(self):
        return 4

    def get_straight_pos(self, position):
        next_position = position
        if self is Direction.UP:
            next_position[1] -= CELL_SIZE
        if self is Direction.RIGHT:
            next_position[0] += CELL_SIZE
        if self is Direction.DOWN:
            next_position[1] += CELL_SIZE
        if self is Direction.LEFT:
            next_position[0] -= CELL_SIZE
        return next_position
