import pygame
import sys

from Food import Food
from Snake import Snake
from utils.config import CELL_SIZE

pygame.init()
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()
running = True

snake = Snake()
food = Food()

while running and snake.is_alive():
    print(snake.get_state(food))
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False
    for x in snake.body:
        pygame.draw.rect(screen, (255, 0, 0), (*x, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, (255, 255, 255), (*x, CELL_SIZE, CELL_SIZE), 1)
    pygame.draw.rect(screen, (0, 255, 0), (*food.position, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()
    snake.move(food)
    clock.tick(10)

pygame.quit()
sys.exit()