from collections import defaultdict
from functools import partial

import numpy as np

def default_q(number_action):
    return np.zeros(number_action)

class QLearning:

    def __init__(self, number_action, learning_rate, discount_factor):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.number_action = number_action
        self.q_table = defaultdict(partial(default_q, number_action))

    def choice_action(self, epsilon, current_state):
        if np.random.rand() < epsilon:
            return np.random.choice(range(0, self.number_action))
        return np.argmax(self.q_table[current_state])

    def update_q_table(self, index_action, current_state, next_state, reward):
        current_action = self.q_table[current_state][index_action]
        next_action = np.max(self.q_table[next_state])

        self.q_table[current_state][index_action] = current_action + self.learning_rate * (
                reward + self.discount_factor * next_action - current_action
        )

