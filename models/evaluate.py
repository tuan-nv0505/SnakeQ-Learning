import json
import os
import pickle

import numpy as np
import pygame
import sys
from q_learning import QLearning
from things.Food import Food
from things.Snake import Snake
from utils.config import CELL_SIZE, get_action, WIDTH, HEIGHT
from train import free_space

epsilon = 0
learning_rate = 0.2
discount_factor = 0.9

def load_file(model):
    q_table_test = "checkpoint/q_table_train.pkl"
    if os.path.exists(q_table_test):
        with open(q_table_test, "rb") as f:
            model.q_table = pickle.load(f)
        print("load file thanh cong.")
    else:
        print("load file that bai.")


class Game:
    __flag = True
    def __init__(self, width, height, background_color, fps, model):
        pygame.init()
        pygame.mixer.init()
        self.sound_eat = pygame.mixer.Sound("assets/eat.wav")
        self.sound_loss = pygame.mixer.Sound("assets/loss.wav")
        try:
            if not os.path.exists("assets/the-return-of-the-8-bit-era-301292.mp3"):
                raise FileNotFoundError("Can not found: {}".format("assets/the-return-of-the-8-bit-era-301292.mp3"))
            pygame.mixer.music.load("assets/the-return-of-the-8-bit-era-301292.mp3")
            pygame.mixer.music.play(loops=-1)
        except FileNotFoundError as error:
            print(error)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.background_color = background_color
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 25)
        self.fps = fps
        self.snake = Snake()
        self.food = Food()
        self.model = model
        self.score = 0

    # Game loop
    def game_update(self):
        while self.is_running():
            self.game_draw()
            if self.snake.move(self.food):
                self.score += 1
                try:
                    if not os.path.exists("assets/eat.wav"):
                        raise FileNotFoundError("Can not found: {}".format("assets/eat.wav"))
                    self.sound_eat.play()
                except FileNotFoundError as error:
                    print(error)
            if not free_space(self.snake):
                print("bi bao vay")

            self.snake.update_direction(get_action(self.model.choice_action(epsilon, self.snake.get_state(self.food))))
        else:
            print("chet")
        pygame.quit()

    # Game draw
    def game_draw(self):
        # Draw snake
        for x in self.snake.body:
            pygame.draw.rect(self.screen, (255, 0, 0), (*x, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(self.screen, (255, 255, 255), (*x, CELL_SIZE, CELL_SIZE), 1)

        # Draw food
        if Game.__flag:
            pygame.draw.rect(
                self.screen, (255, 255, 0),
                (*self.food.get_pos(), CELL_SIZE, CELL_SIZE),
                border_radius=15
            )
            Game.__flag = False
        else:
            pygame.draw.rect(
                self.screen, (255, 255, 0),
                (*(self.food.get_pos() + np.array([5, 5])), CELL_SIZE - 10, CELL_SIZE - 10),
                border_radius=15
            )
            Game.__flag = True

        # Draw score
        try:
            if not os.path.exists("assets/PressStart2P-Regular.ttf"):
                raise FileNotFoundError("Can not found: {}".format("assets/PressStart2P-Regular.ttf"))
        except FileNotFoundError as error:
            print(error)
            self.font = pygame.font.Font(None, 25)
        text = self.font.render("SCORE: {:04d}".format(self.score), True, (0, 255, 0))
        self.screen.blit(text, dest=(15, 15))

        pygame.display.flip()
        self.clock.tick(self.fps)
        self.screen.fill(self.background_color)

    def is_running(self):
        if not self.snake.is_alive():
            try:
                if not os.path.exists("assets/loss.wav"):
                    raise FileNotFoundError("Can not found: {}".format("assets/loss.wav"))
                self.sound_loss.play()
                pygame.time.delay(350)
            except FileNotFoundError as error:
                print(error)
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True


if __name__ == "__main__":
    model = QLearning(3, learning_rate, discount_factor)
    load_file(model)
    while True:
        game = Game(WIDTH, HEIGHT, (0, 0, 0), 30, model)
        game.game_update()