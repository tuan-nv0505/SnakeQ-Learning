import numpy as np
from utils.config import WIDTH, HEIGHT, CELL_SIZE


class Food:

    def __init__(self):
        # self.__x_food = 540
        # self.__y_food = 450
        self.__x_food = np.random.choice(np.arange(0, WIDTH, CELL_SIZE))
        self.__y_food = np.random.choice(np.arange(0, HEIGHT, CELL_SIZE))
        self.__position = np.array([self.__x_food, self.__y_food])

    def reset_position(self, snake):
        for i in range(0, 1000):
            self.__x_food = np.random.choice(np.arange(0, WIDTH, CELL_SIZE))
            self.__y_food = np.random.choice(np.arange(0, HEIGHT, CELL_SIZE))
            self.__position = np.array([self.__x_food, self.__y_food])
            if self.__valid_food(snake):
                break
        else:
            print("WARNING: Could not find valid food position after 1000 attempts.")

    def __valid_food(self, snake):
        return not any((self.__position == element).all() for element in snake.body)

    def get_pos(self):
        return np.copy(self.__position)

