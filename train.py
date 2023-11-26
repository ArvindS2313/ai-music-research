"""
train.py trains both the time period neural network (MLP) and the whole dataset
neural network (Transformer) seperately. The user, in their preferences, enters
which time periods and which genres they wish to hear music from. From that, only
the required number of time period and genre NNs will be trained. 

Things to do in the near future:
TODO: Implement a learning rate schedueler, as proposed by Vaswani et al., 2017
TODO: Implement gradient clipping 
"""

import os
import pickle
import time
import math 
import importlib
import wandb

import numpy as np 
import torch 
import torch.nn.functional as F

