import numpy as np
from Food import Food
from Snake import Snake




if __name__ == "__main__":
    snake = Snake()
    food = Food()
    print(snake.body)
    print(snake.direction)
    snake.move(food)
    print(snake.body)