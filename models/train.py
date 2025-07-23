import pickle
import numpy as np
import os
from q_learning import QLearning
from things.Food import Food
from things.Snake import Snake
from utils.config import get_action, manhattan, CELL_SIZE, WIDTH, HEIGHT
from collections import deque

learning_rate = 1
min_learning_rate = 0.05
discount_factor = 0.9
episodes = 300000
epsilon = 0.01
epsilon_min = 0.01
epsilon_decay = 0.9995
list_score = []
list_step = []
list_reward = []


def is_avoiding_imminent_danger(snake, index_action):
    next_positions = snake.get_next_pos(snake.get_head())
    straight_pos = next_positions[snake.direction.value]
    action_pos = next_positions[(snake.direction.value + get_action(index_action)) % 4]
    is_danger = snake.is_collision_body(straight_pos) or snake.is_collision_wall(straight_pos)
    is_safe = not (snake.is_collision_body(action_pos) or snake.is_collision_wall(action_pos))
    return is_danger and is_safe


def is_moving_same_direction(old_direction, new_direction):
    return old_direction == new_direction


def is_forcing_dead_end(snake):
    return sum(snake.is_collision_wall(p) or snake.is_collision_body(p)
               for p in snake.get_next_pos(snake.get_head())) == 3


# BFS
def free_space(snake):
    spaces = 0
    q = deque()
    visited = np.zeros((HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE))

    head = snake.get_head()
    start_y = head[1] // CELL_SIZE
    start_x = head[0] // CELL_SIZE
    q.append(head)
    visited[start_y, start_x] = 1

    while len(q) > 0:
        pos_current = q.popleft()
        for next_pos in snake.get_next_pos(pos_current):
            y = next_pos[1] // CELL_SIZE
            x = next_pos[0] // CELL_SIZE

            if (0 <= y < HEIGHT // CELL_SIZE and 0 <= x < WIDTH // CELL_SIZE and
                    visited[y, x] != 1 and
                    not any((next_pos == element).all() for element in snake.body)):
                visited[y, x] = 1
                spaces += 1
                q.append(next_pos)

        if spaces > len(snake.body):
            return True
    # print("da bi bao vay")
    return False


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
            # print("chet")
            reward -= (100 + 2.5 / epsilon)
            list_score.append(score)
            list_step.append(step)
            alive = False
        elif ate:
            reward += 100
            score += 1
        else:
            dist_old = manhattan(old_head, food.get_pos())
            dist_new = manhattan(new_head, food.get_pos())
            if dist_new < dist_old:
                reward += 2
            elif dist_new > dist_old:
                reward -= 2

            if epsilon <= 0.3:
                if is_avoiding_imminent_danger(snake, index_action):
                    reward += 3

                if is_forcing_dead_end(snake):
                    reward -= (20 + 1 / epsilon)
                elif not free_space(snake):
                    reward -= (100 + 2.5 / epsilon)

                if epsilon <= 0.2:
                    if is_moving_same_direction(old_direction, snake.direction):
                        reward += 1.5
                    else:
                        reward -= 1.5
                reward -= 0.5

        reward += 20 + score

        # Update q_table
        # print("reward: {}".format(reward))
        next_state = snake.get_state(food)
        model.update_q_table(index_action, current_state, next_state, reward)
        list_reward.append(reward)


def main():
    q_table_train = "checkpoint/q_table_train.pkl"
    os.makedirs("checkpoint", exist_ok=True)
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
        model.learning_rate = min_learning_rate + (learning_rate - min_learning_rate) * epsilon

        # Print log
        if episode % 100 == 0:
            with open(q_table_train, "wb") as f:
                pickle.dump(model.q_table, f)

            print(
                "Episode [{}][{}] | Epsilon: {:.3f} Learning rate: {:.3f} | Max score: {} Average score: {:.3f} | "
                "Max step: {} Average step: {:.3f} | Max reward: {} Average reward: {:.3f}".
                format(
                    episode, episodes, epsilon, model.learning_rate, max(list_score), np.mean(np.array(list_score)),
                    max(list_step), np.mean(np.array(list_step)), max(list_reward), np.mean(np.array(list_reward))
                )
            )
            exp_state = len(model.q_table)
            print("EXPLORE THE MAP: {}/{} | {:.2f}%".format(exp_state, 1024, exp_state*100/1024))
            list_score.clear()
            list_step.clear()
            list_reward.clear()


if __name__ == "__main__":
    main()