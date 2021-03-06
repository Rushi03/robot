import numpy as np
import random
from q_learning import QLearning
from maze import Maze
import sys


class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''
        # Starting location; bottom right corner
        self.location = [0, maze_dim - 1]
        # Starts heading up
        self.heading = 'up'
        # Dimensions of the maze
        self.maze_dim = maze_dim
        # Goal(square) for robot
        self.goal = [self.maze_dim / 2 - 1, self.maze_dim / 2]
        # Import maze environment for rewards
        self.maze = Maze(str(sys.argv[1]))

    def next_move(self, sensors):
        '''
        This function is to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.
        '''
        position = tuple(self.location)
        sensor = tuple(sensors)

        # Implement Q-Learning
        q_learn = QLearning()
        # Build state through sesnsor information
        state = q_learn.build_state(position, sensor)
        # Create state in Q-table if is not already there
        q_learn.create_Q(state)
        # Take action according to state
        action = q_learn.choose_action(state)

        if self.location[0] in self.goal and self.location[1] in self.goal:
            rotation = 'Reset'
            movement = 'Reset'
            if (rotation, movement) == ('Reset', 'Reset'):
                self.location = [0, self.maze_dim - 1]
                self.heading = 'up'
        else:
            # Up
            if action == 'up':
                rotation = 0
                movement = 1
            # Right
            elif action == 'right':
                rotation = 90
                movement = 1
            # Down
            elif action == 'down':
                rotation = 0
                movement = -1
            # Left
            elif action == 'left':
                rotation = -90
                movement = 1
            else:
                rotation = 'Reset'
                movement = 'Reset'

        # Gather reward per action taken by the robot
        reward = self.maze.move(self.goal, self.location, action)
        # Learn from the state, action, and reward
        q_learn.learn(state, action, reward)

        # Returns tuple (rotation, movement)
        return rotation, movement
