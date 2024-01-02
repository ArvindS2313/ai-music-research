"""
train.py trains both the time period neural network (MLP) and the whole dataset
neural network (Transformer) seperately. The user, in their preferences, enters
which time periods and which genres they wish to hear music from. From that, only
the required number of time period and genre NNs will be trained. 

Things to do in the near future:
TODO: Implement a learning rate schedueler, as proposed by Vaswani et al., 2017
TODO: Implement gradient clipping 
"""

import torch 
import argparse
import pickle
import time

from model.time_prd import TimePeriod
from model.whole_dataset_tr import WholeDatasetTransformer
from torch.utils.data.dataloader import DataLoader, RandomSampler
from data.whole_dataset import WholeDataset

device = 'cpu'
eval_interval = 400
eval_iters = 40
disp_interval = 2


class Train:

    def __init__(self, hparams: dict, epoch_tr: bool, rand=True):
        '''
        Initalizes the data if it was not passed in already, sets up optimizers and 
        constants, and declares the model.
        '''

        self.rand = rand
        self.hparams = hparams
        # document important params
        self.block_size = self.hparams['block_size']
        self.batch_size = self.hparams['batch_size']

        # set up training data and dataloaders 
        self.train_data = WholeDataset(train=True, rand=self.rand, block_size=self.block_size)
        self.val_data = WholeDataset(train=False, rand=self.rand, block_size=self.block_size)
        self.train_dl = DataLoader(
            dataset=self.train_data,
            batch_size= self.batch_size, 
            shuffle= True,
            sampler= RandomSampler(self.train_data)  # TODO: add custom sampler
        )
        self.val_dl = DataLoader(
            dataset=self.val_data,
            batch_size= self.batch_size, 
            shuffle= True,
            sampler= RandomSampler(self.val_data)# TODO: add custom sampler
        )

        self.train_iter = iter(self.train_dl)
        self.val_iter = iter(self.val_dl)
        self._load_pkl()

        # set up model and optimizers 
        self.model = WholeDatasetTransformer(
            n_embd = hparams['n_embd'], n_layers = hparams['n_layers'],
            vocab_size = self.vocab_size, n_head = hparams['n_head'],
            h_dim = hparams['h_dim'], block_size = hparams['block_size'],
            dropout = hparams['dropout'], ffn_bias = hparams['ffn_bias'],
            layernorm_eps = hparams['layernorm_eps']
        )
        self.optimizer = torch.optim.AdamW(
            self.model.parameters(), 
            lr=hparams['learning_rate'],
            betas = hparams['betas'] )
        
        # initalize time/velocity variables 
        self.num_iters = 0
        self.start = None
        self.end = None
        
        
    def train(self):
        pass

    def evaluate(self):
        pass
        


    def _load_pkl(self):
        with open("train/info.pkl") as f:
            self.vocab_size = pickle.load(f)
        return 













# # MLP Data 
# mlp_dataset = 'ug'
# mlp_max_iters = 5000
# tp_vocab_sizes: dict
# genre_vocab_sizes: dict
# mlp_block_size = 4
# mlp_n_embd = 10
# mlp_n_hidden = 50
# mlp_norm = 'batch'

# # Transformer Data
# tr_dataset = ('ug', 'pop909')
# tr_max_iters = 10000
# tr_vocab_size: int
# n_layers = 12
# n_embd = 120    # head_size = 10
# n_head = 10
# tr_block_size = 8
# bias = True
# layernorm_eps = 1e-6
# dropout = 0.1   # make 0.0 or 0.1

# # Optimizer
# opt = 'AdamW'
# learning_rate = 1e-3
# weight_decay = 0.0
# beta1 = 0.9
# beta2 = 0.9

