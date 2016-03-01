import numpy as np
import random

EMPTY = 0
WALL = 1
GOAL = 2
AGENT = 3

class MovingGoalsWorld():
    """
    10x10 world specified in world.txt
    key: {'|' = wall, 'a' = agent (at initial location), 'g': allowable goal placement, 'x': empty}
    """

    def __init__(self, world_config = 'world.txt', max_steps = 40):

        self.goal_index = None
        self.agent_index = None
        self.num_steps = None
        self.max_steps = max_steps
        self.world_config = world_config
        self.possible_actions = ['up', 'down', 'right', 'left', 'stay']
        self.state = self.s0()

    def reinitialize(self):
        self.state = self.s0()

    def s0(self):
        self.num_steps = 0
        # parses the world_config file into a bag-of-words state vector
        key = {'x': EMPTY, '|': WALL, 'g': GOAL, 'a': AGENT}
        world_vector = []
        with open(self.world_config, 'r') as world_file:
            for i,line in enumerate(world_file):
                world_vector += [key[i] for i in line.strip().split(' ')]

        # picks a random goal location among the possible goals
        world_vector = np.array(world_vector)
        possible_goal_locs = np.where(world_vector == 2)[0]
        np.random.shuffle(possible_goal_locs)
        # updates goal index
        self.goal_index = possible_goal_locs[0]
        self.agent_index = np.where(world_vector == 3)[0][0]

        for i,value in enumerate(world_vector):
            if value == 2 and i != self.goal_index:
                world_vector[i] = 0

        return world_vector
        
    def step(self, action):
        # returns next state given the action

        self.num_steps += 1

        if action == 'up':
            new_index = self.agent_index - 10
            if self.state[new_index] != WALL and new_index >= 0:
                self.state[self.agent_index] = EMPTY
                self.state[new_index] = AGENT
                self.agent_index = new_index
            return self.is_terminal()

        if action == 'down':
            new_index = self.agent_index + 10
            if self.state[new_index] != WALL and new_index <= 99:
                self.state[self.agent_index] = EMPTY
                self.state[new_index] = AGENT
                self.agent_index = new_index
            return self.is_terminal()

        # don't change state
        if action == 'stay':
            return self.is_terminal()

        # for right and left, update index different, but same checking condition
        if action == 'right':
            new_index = self.agent_index + 1

        if action == 'left':
            new_index = self.agent_index + 1

        if self.state[new_index] != WALL and int(new_index/10) == int(self.agent_index/10):
            self.state[self.agent_index] = EMPTY
            self.state[new_index] = AGENT
            self.agent_index = new_index
        return self.is_terminal()


    def is_terminal(self):
        # state is terminal when agent reaches goal or maxSteps reached
        if self.agent_index == self.goal_index:
            return True
        if self.num_steps >= self.max_steps:
            return True
        return False