import torch 
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math


import os
import time 

''' Simple, decode only Transformer using both the POP909 and UG datasets.
Goal is to predict, given a sequence of chords, the next chord. '''

''' This transformer will be mainly imeplemented from scratch, without using 
torch.nn.Transformer. This is for two reasons:
1. torch.nn.Transformer is very rigid; I would like to have some things that
aren't exactly like the paper, so not the best fit.
2. It's a good learning opportunity for me to get more involved with the
archiecture.
3. I will be using torch.nn.TransformerDecoder and pass in the 'blocks' that 
I've coded up - but pretty much everything else is raw 

Whole dataset NNs will be implemented using Transformers/LSTMS. My time period
specific NNs and my genre specific NNs will be trianed using simple MLP (b/c
lack of training data lol)

See README for my references. 
'''

class Attention(nn.Module):
    pass


class MLP(nn.Module):
    pass


class Decoder(nn.Module):
    pass


class WholeDatasetTransformer(nn.Module):

    def __init__(self):
        super().__init__()
    
    def forward(self, ):
        pass

    def get_loss(self, yhat, y):
        pass

    def generate(self, idx: torch.tensor, tokens=None):
        ''' generation function for NN'''
        
        if tokens is None:
            # as many tokens as needed 
            tokens = None