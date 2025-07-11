import numpy as np
from utils.config import WIDTH, HEIGHT, CELL_SIZE


class Food:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        # self.__x_food = 540
        # self.__y_food = 450
        self.__x_food = np.random.choice(np.arange(0, WIDTH, CELL_SIZE))
        self.__y_food = np.random.choice(np.arange(0, HEIGHT, CELL_SIZE))
        self.position = np.array([self.__x_food, self.__y_food])

    def reset_position(self, snake):
        while True:
            self.__x_food = np.random.choice(np.arange(0, WIDTH, CELL_SIZE))
            self.__y_food = np.random.choice(np.arange(0, HEIGHT, CELL_SIZE))
            if self.__valid_food(snake):
                break
        self.position = np.array([self.__x_food, self.__y_food])

    def __valid_food(self, snake):
        return np.any(np.all(self.position == element) for element in snake.body)

