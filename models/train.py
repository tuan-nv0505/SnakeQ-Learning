import pickle

import numpy as np
import json
import os
import shutil

import pygame

from q_learning import QLearning
from things.Food import Food
from things.Snake import Snake
from utils.config import get_action, manhattan, CELL_SIZE

learning_rate = 0.2
discount_factor = 0.9
episodes = 1000000
epsilon = 1
epsilon_min = 0.01
epsilon_decay = 0.9995
list_score = []
list_step = []
list_reward = []


def is_avoiding_imminent_danger(snake, index_action):
    next_positions = snake.get_next_pos()
    straight_pos = next_positions[snake.direction.value]
    action_pos = next_positions[(snake.direction.value + get_action(index_action)) % 4]
    is_danger = snake.is_collision_body(straight_pos) or snake.is_collision_wall(straight_pos)
    is_safe = not (snake.is_collision_body(action_pos) or snake.is_collision_wall(action_pos))
    return is_danger and is_safe


def is_moving_same_direction(old_direction, new_direction):
    return old_direction == new_direction


def is_forcing_dead_end(snake):
    return sum(snake.is_collision_wall(p) or snake.is_collision_body(p)
               for p in snake.get_next_pos()) == 3


def is_stuck(snake):
    return sum(snake.is_collision_wall(p) or snake.is_collision_body(p)
               for p in snake.get_next_pos()) == 4

def loop(snake, food, model, epsilon):
    alive = True
    score = 0
    step = 0
    running = True
    while alive and running:
        step += 1
        current_state = snake.get_state(food)
        old_head = snake.get_head()
        old_direction = snake.direction

        index_action = model.choice_action(epsilon, current_state)
        snake.update_direction(get_action(index_action))
        ate = snake.move(food)
        new_head = snake.get_head()

        # Reward
        reward = 0
        if not snake.is_alive():
            reward -= 300
            list_score.append(score)
            list_step.append(step)
            alive = False
        elif ate:
            reward += 200
            score += 1
        else:
            dist_old = manhattan(old_head, food.get_pos())
            dist_new = manhattan(new_head, food.get_pos())
            if dist_new < dist_old:
                reward += 2
            elif dist_new > dist_old:
                reward -= 2

            if is_avoiding_imminent_danger(snake, index_action):
                reward += 10
            if is_stuck(snake):
                reward -= 300
            if is_forcing_dead_end(snake):
                reward -= 20
            if is_moving_same_direction(old_direction, snake.direction):
                reward += 2
            else:
                reward -= 2
            reward -= 2

        # Update q_table
        next_state = snake.get_state(food)
        model.update_q_table(index_action, current_state, next_state, reward)
        list_reward.append(reward)


def main():
    q_table_train = "brain/q_table_train.pkl"
    os.makedirs("brain", exist_ok=True)
    model = QLearning(3, learning_rate, discount_factor)

    # Load file
    if os.path.exists(q_table_train):
        with open(q_table_train, "rb") as f:
            model.q_table = pickle.load(f)
        print("load file thanh cong.")
    else:
        print("load file that bai.")

    global epsilon
    for episode in range(episodes):
        # Train
        snake = Snake()
        food = Food()
        loop(snake, food, model, epsilon)
        epsilon = max(epsilon_min, epsilon * epsilon_decay)

        # Print log
        if episode % 100 == 0:
            with open(q_table_train, "wb") as f:
                pickle.dump(model.q_table, f)

            print(
                "Episode [{}][{}] | Epsilon: {:.4f} | Max score: {} Average score: {:.4f} | "
                "Max step: {} Average step: {:.4f} | Max reward: {} Average reward: {:.4f}".
                format(
                    episode, episodes, epsilon, max(list_score), np.mean(np.array(list_score)),
                    max(list_step), np.mean(np.array(list_step)), max(list_reward), np.mean(np.array(list_reward))
                )
            )
            print("EXPLORE THE MAP: {:.2f}%".format(len(model.q_table)*100/256))
            list_score.clear()
            list_step.clear()
            list_reward.clear()


if __name__ == "__main__":
    main()