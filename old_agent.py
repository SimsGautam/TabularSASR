import random
import numpy as np

class OldAgent:
    def __init__(self, possible_actions, gamma = 1, epsilon = 1, alpha = 0.9, default_Q = 0.0):
        """
        gamma: discount rate
        epsilon: exploration rate
        alpha: learning rate
        default_Q: default Q value
        possible_actions: list of possible actions
        """
        self.q_table = {}
        self.gamma = gamma
        self.epsilon = epsilon
        self.alpha = alpha
        self.default_Q = default_Q
        self.actions = possible_actions

    def get_size(self):
        return len(self.q_table)

    def set_epilson(self, new_epsilon):
        self.epsilon = new_epsilon

    def get_Q(self, state, action):
        return self.q_table.get((state,action), self.default_Q)

    def update_Q(self, new_estimate, state, action):
        # should update the Q-value in the table based on learning rate
        old_Q = self.q_table.get((state, action), None)
        if old_Q == None:
            self.q_table[(state, action)] = self.alpha*new_estimate
        else:
            self.q_table[(state, action)] = old_Q + self.alpha*(new_estimate - old_Q)

    def choose_action(self, state):
        # epsilon greedy approach: choose randomly with probability epsilon
        if random.random()<self.epsilon:
            action = random.choice(self.actions)
        else:
            q_values = [self.get_Q(state, action) for action in self.actions]
            max_value = max(q_values)
            max_indices = [i for i, j in enumerate(q_values) if j == max_value]
            action = self.actions[random.choice(max_indices)]
        return action

    def learn(self, state, action, reward, new_state):
        new_max_Q = max([self.get_Q(new_state,a) for a in self.actions])
        new_estimate = reward + self.gamma * new_max_Q
        self.update_Q(new_estimate, state, action)
