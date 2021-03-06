# Neural.Swarms
Python swarm simulation with neural net based agents. Mainly focused on the NaviGame in my fork of [Python.Swarms](https://github.com/thetabor/Python.Swarms/), but the way I extend the game to allow a neural net is applicable to all of the games. You will need that repo, so clone it down before continuing. I am exploring both supervised and reinforcement learning for the agent. For a nice visual display, see:

```
/NaviGame/Reinforcement Model Training.ipynb
/NaviGame/Supervised Model Training.ipynb
```

If you just want to train models or want to display somehow other than with a jupyter notebook, use these files:

```
/NaviGame/reinforcement_training.py
/NaviGame/supervised_training.py
```

# tl;dr

- To train a model, run one of the two .py files above
- They will step you through setting up the basic variables
- That code is locked to a 40 by 30 game board, 3-layer MLPs, and training on a empty field
- I recommend training a model through the terminal, launching a Jupyter Notebook, and playing with it there
- Then, use the Jupyter Notebook to run the more advanced training methods

# Known issues

- Figure placement can create recursion crashes
- Not enough comments anywhere
- Requires jupyter for visualization
  - Add direct GIF export
  - Consider potential pygame interfaces

# Initial Goals

The goals are behavioral in nature, rather than statistic.
- **Navigation** : demonstrate reinforcement learning for simple navigation
- **Cooperation** : multiple agents move a target
- **Model Extension** : find a way to build a model which can be trained to arbitrary performance levels, then still train further on new environments.

# Agents, Environments, and Reinforcement Learning

- **Agents**, in the context of machine learning, are a class of algorithms which make choices once deployed. Agents may be anything from humble vacuum cleaners to stock-picking algorithms. We generally say the agent exists in an environment, be it virtual or physical.
- **Supervised Learning** is the standard method of many statistical models and neural networks. It requires an (X, y) style training set, with inputs and desired outputs. The training set becomes a limitation, as the agent will only perform as well as the data it learns from. For the simple task of reaching a goal position in a deterministic environment, it performs very well after a short training period. We obtain data for this training from a deterministic strategy, so the neural network is limited to that performance level on the game. Simply adding a small barrier is enough to completely halt the network's strategy.
- **Reinforcement Learning** allows us to train our algorithms with rewards. Rather than learning from an (X, y) training set, it learns from experience. Each experience comes with certain rewards, and each time a reward is received, the algorithm can learn.
- **Deep-Q Networks** are a way to deploy reinforcement learning to neural networks. The network predicts Q-values for each action the network is allowed. A Q-value is a **quality** of a state, or the expected sum of rewards as we play the game from that state. We (almost) always select the max Q-value we predict.
- **RL Data:** Initially, the agent has absolutely no knowledge of the environment, so Q-values are effectively random. At each step, it updates the Q-value using the actual reward, plus the Q-value of the next step it plans on taking. So, our model trains on (X, y) data, but each y is actually self-generated and often very inaccurate. But since a part of it is ground truth, the model eventually learns something close enough to real Q-values to function.

# Deterministic and Supervised Examples
Here we see how quickly the supervised learner can perform well on the simple task. In contrast, the reinforcement learner struggles to perform well, but it is does show potential. Here are some examples of simulation performance:

| Deterministic Strategy | Almost trained supervised model | Trained supervised |
| --- | --- | --- |
| ![Deterministic](https://github.com/thetabor/Neural.Swarms/blob/master/Notes/gifs/deterministic_strategy_test.gif) | ![Almost trained](https://github.com/thetabor/Neural.Swarms/blob/master/Notes/gifs/supervised/slight_undertrained_supervised.gif) | ![Fully trained](https://github.com/thetabor/Neural.Swarms/blob/master/Notes/gifs/supervised/trained_supervised.gif) |

The supervised network learns from the deterministic strategy on the left, and eventually learns to mimic it perfectly.

This also means that the supervised learner is limited by the strategy it learns from. So, enter *reinforcement learning*!

# Reinforcement Examples

Reinforcement learning allows the agent to explore strategies on its own, and by receiving rewards from its environment, learns which are better.

When the DQN agent is initialized, it's output values are effectively random numbers, and training is very susceptible to local minima. So, we train using an explore/exploit ratio that decreases throughout the training session. Typically, it starts at 0.9, and ends at 0.1. Additionally, I can make some of the choices come from our deterministic strategy, to focus training on the "correct" routes. Third, we know that our deterministic strategy works, so why not use it? And, finally, a tolerance function can make the game easier or harder, to let's start with an easier game, then make it harder once the agent is doing well.

With all this in mind, I built a new model. This model takes inputs as usual, the whole game screen. As outputs, it has the five usual outputs; up, down, left, right and stay, plus a new addition: use the deterministic strategy. So, for the simple games, all our DQN agent has to do is learn to always use the deterministic strategy. Once it learns this, then we can start exploring more complex problems. Meet Larry, the simple bundle of neurons:

| Break In | More Training | Trained with harder game | Non-optimal paths | Doesn't like obstacles |
| --- | --- | --- | --- | --- |
| ![Larry1](https://github.com/thetabor/Neural.Swarms/blob/master/Notes/gifs/larry/01_break_in.gif) | ![Larry2](https://github.com/thetabor/Neural.Swarms/blob/master/Notes/gifs/larry/02_more_training.gif) | ![img3](https://github.com/thetabor/Neural.Swarms/blob/master/Notes/gifs/larry/03_harder_game.gif) | ![img4](https://github.com/thetabor/Neural.Swarms/blob/master/Notes/gifs/larry/04_non_optimal.gif) | ![img5](https://github.com/thetabor/Neural.Swarms/blob/master/Notes/gifs/larry/05_run_away.gif) |

To conclude, reinforcement learning clearly works, and leaves flexibility to function of new challenges. I've built new training systems for training with a variety of obstacles. I'm currently in the processes of documenting the code here and in my Sphero DQN project, and will continue testing models once that's finished.

# References

- [Python.Swarms](https://github.com/elmar-hinz/Python.Swarms/)
- [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602)
- Excellent materials in Georgia Tech's [Reinforcement Learning](https://www.udacity.com/course/reinforcement-learning--ud600) course on Udacity.
- [Keras Plays Catch](https://edersantana.github.io/articles/keras_rl/)
- [Pong from Pixels](http://karpathy.github.io/2016/05/31/rl/)
- [Deep Reinforcement Learning](https://www.nervanasys.com/demystifying-deep-reinforcement-learning/)
