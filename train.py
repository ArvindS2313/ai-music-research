"""
train.py trains both the time period neural network (MLP) and the whole dataset
neural network (Transformer) seperately. The user, in their preferences, enters
which time periods and which genres they wish to hear music from. From that, only
the required number of time period and genre NNs will be trained. 

Things to do in the near future:
TODO: Implement a learning rate schedueler, as proposed by Vaswani et al., 2017
TODO: Implement gradient clipping 
"""

import numpy as np 
import torch 
import torch.nn.functional as F
import sklearn

from model.time_prd import TimePeriod
from model.whole_dataset_tr import WholeDatasetTransformer

# ----------------------- HYPERPARAMETERS ---------------------------
eval_interval = 400
eval_iters = 40
display_interval = 2
comb_vocab_size: int 
device = 'cpu'     # TODO: get cuda support working 

# MLP Data 
mlp_dataset = 'ug'
mlp_max_iters = 5000
tp_vocab_sizes: dict
genre_vocab_sizes: dict
mlp_block_size = 4
mlp_n_embd = 10
mlp_n_hidden = 50
mlp_norm = 'batch'

# Transformer Data
tr_dataset = ('ug', 'pop909')
tr_max_iters = 10000
tr_vocab_size: int
n_layers = 12
n_embd = 120    # head_size = 10
n_head = 10
tr_block_size = 8
bias = True
layernorm_eps = 1e-6
dropout = 0.1   # make 0.0 or 0.1

# Optimizer
opt = 'AdamW'
learning_rate = 1e-3
weight_decay = 0.0
beta1 = 0.9
beta2 = 0.9

# ---------------------- LOAD DATA ----------------------------------
