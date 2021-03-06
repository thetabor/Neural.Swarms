# utilities
import pandas as pd
import numpy as np
import pylab as pl
import pickle
import os, sys
from collections import Counter
sys.path.append(os.path.abspath("../../../Python.Swarms/"))

# import the game parts
# game imports
from random import random, sample, randint
from game import BoardGame
from board import Board
from figure import Figure, FigureStrategy
from logger import log
from navi_game import *
from game_display_helper import make_gif

# imports for neural net
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import sgd, RMSprop, Adagrad, Adam
import theano

# Navigator game main class
class SupervisedNaviGame(NaviGame):
    def __init__(self,
            height,
            width,
            model = None,
            tolerance = 1.4,
            goal_idle = 2):
        NaviGame.__init__(self, height, width,
                            goal = (int(height/2), int(width/2)),#None,
                            moving_target = False,
                            tolerance = tolerance,
                            goal_idle = goal_idle)
        self.model = model

    def setup(self):
        NaviGame.setup(self)
        self.training_strategy = NaviStrategy(self.goal, self.tolerance)
        self.strategy = SupervisedStrategy(self.goal, self.model)
        self.Navigator.bindStrategy(self.strategy)

    # in: 4, out: 5
    # by default, uses one ReLU based hidden layer
    def game_model(self, optimizer = sgd(lr = 0.001),
        layers = [{"size":20,"activation":"relu"}]):
        # one action for each direction and one for hold
        num_actions = 5
        # prepare the navigator model
        model = Sequential()
        # initial inputs
        l = list(layers)
        l0 = l[0]
        del l[0]
        model.add(Dense(l0['size'],
        input_dim = 4,
        activation = l0['activation']))
        # the hidden layers
        for layer in l:
            model.add(Dense(layer['size'], activation=layer['activation']))
        # the output layer
        model.add(Dense(num_actions, activation='sigmoid'))
        model.compile(optimizer = optimizer,
        loss = "mean_squared_error")
        return model

    # generate data for training the navigator
    # uses the deterministic strategy NaviStrategy
    def train_data(self, n = 100):
        inputs, targets = [], []
        self.Navigator.bindStrategy(self.training_strategy)
        for i in range(n):
            ipt, _ = self.Navigator.strategy.get_input()
            inputs.append(ipt)
            choice = self.Navigator.strategy.plan_movement()
            t = [0, 0, 0, 0, 0]
            t[choice] = 1
            targets.append(t)
            self.step()
        # return the data
        self.Navigator.bindStrategy(self.strategy)
        return inputs, targets

    def train_model(self, steps = 1000, epochs = 20, batch_size = 32,
                        verbose = 0, inputs = None, targets = None):
        if (inputs == None) and (targets == None):
            s = 0
            inputs, targets = [], []
            # grab sequences of games, ten steps at a time
            while s < steps:
                # self.shift_figure()
                inputsk, targetsk = self.train_data(10)
                inputs.extend(inputsk)
                targets.extend(targetsk)
                s += len(inputsk)
        print("Data generated")
        _resp = input("would you like to review?")
        if _resp == "y":
            print("[Inputs], [Targets]")
            for i in range(10):
                print(inputs[i], targets[i])
        print("Now fitting network")
        log = self.model.fit(inputs, targets,
                            verbose = verbose,
                            epochs = epochs,
                            batch_size = batch_size,
                            shuffle=True)
        return log, inputs, targets

# Supervised learning strategy
class SupervisedStrategy(NaviStrategy):
    def __init__(self, goal, model):
        self.model = model
        NaviStrategy.__init__(self, goal)

    def plan_movement(self, det_choice = False):
        if (self.model != None) and (det_choice == False): # use the model
            ipt, _ = self.get_input()
            predictions = self.model.predict(np.array(ipt).reshape(1, 4))
            choice = np.argmax(predictions)
        else: # use the deterministic strategy
            choice = NaviStrategy.plan_movement(self)
        return choice

if __name__=='__main__':
    # learning variables
    epochs = 20
    batch_size = 32
    learning_rate = 0.05

    # optimizer
    optimizer = sgd(lr=learning_rate)
    optimizer_str = "SGD(lr = "+str(learning_rate)+")"

    # layers
    layers = [{"size":20,"activation":"tanh"}]
    # {"size":5,"activation":"tanh"}]

    # number of steps to train on
    steps = 20000

    # prepare the game for collecting data
    training_game = SupervisedNaviGame(13, 19)

    # make the model
    training_game.model = training_game.game_model(optimizer, layers)

    # setup the game
    training_game.setup()

    print("Generating data & training")
    # pdb.set_trace()
    # collect all data to make pickled runs!
    # stop regenerating the damn data!
    # test_data = training_game.train_data()
    # for i in range(100):
    #     print(test_data[0][i], test_data[1][i])
    log, inputs, targets = training_game.train_model(
                steps = steps,
                epochs = epochs,
                batch_size = batch_size,
                verbose = 1)
    # # pull data points of for validation
    # print("Network and final validation data ready for testing.")
    # # prepare the game for final validation
    print("Creating animation")
    make_gif(training_game, 100)
    training_game.model.save('game_model.h5')
    # note: the example model performs almost identically to the
    # deterministic strategy. It is trained with the following parameters
    # epochs: 20
    # batch size: 32
    # learning rate: 0.05
    # optimizer: sgd
    # hiddens: 1 x (20 tanh)
    # loss: 0.0269 
