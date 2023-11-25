import torch 
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math


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
    ''' a multi-headed attention block'''

    def __init__(self, n_embd, n_head, block_size, exp=False) -> None:
        super().__init__()
        assert n_embd % n_head == 0, "Improper parameters"

        self.exp = exp   # are we in experiment mode? 
        self.n_embd = n_embd
        self.head_size = n_embd/n_head   # head_size * n_head = n_embd
        self.n_head = n_head
        self.block_size = block_size

        self.query = nn.Linear(self.n_embd, self.self.n_embd, bias=False) 
        self.key = nn.Linear(self.n_embd, self.n_embd, bias=False)
        self.val = nn.Linear(self.n_embd, self.n_embd, bias=False)
        self.ln = nn.Linear(self.n_embd, self.n_embd)  # final linear layer        


    def forward(self, x):
        # assert dimensionality of x
        assert x.dim == 3, "Must be shape (B, T, C)"
        batch_size = x.shape[0]

        # query, key, and value vectors
        q = self.query(x)
        k = self.key(x)
        v = self.val(x)

        # adding batch dimensions for multiple heads
        q = q.view(batch_size, self.block_size, self.n_head, 
               int(self.n_embd/self.n_head)).transpose(1, 2)    # B, n_head, T, C
        k = k.view(batch_size, self.block_size, self.n_head,     
               int(self.n_embd/self.n_head)).transpose(1, 2)    # B, n_head, T, C
        v = v.view(batch_size, self.block_size, self.n_head,     
               int(self.n_embd/self.n_head)).transpose(1, 2)    # B, n_head, T, C
        
        # Manual scaled dot product attention - let's implement Shaw. et al. later
        affin = q @ k.transpose(-1, -2) / math.sqrt(self.head_size)   
        set_0 = torch.tril(torch.ones(self.block_size, self.block_size)) \
                            == torch.zeros(self.block_size, self.block_size) # T, T boolean
        affin = affin.masked_fill(set_0, float("-inf"))
        affin = affin.softmax(dim=-1)
        out = affin @ v             # (T, T) x (B, n_head, T, C) -> (B, n_head, T, C)

        out = out.transpose(1, 2).view(batch_size, self.block_size, self.n_embd)
        return self.ln(out)
        

class MLP(nn.Module):
    ''' a feed-foward MLP: linear, ReLU, linear, dropout '''

    def __init__(self, n_embd, h_dim=0, dropout=0.0, bias=True):
        super().__init__()

        # if no h_dim provided, make it 2*n_embd
        if h_dim == 0:
            h_dim = 2*n_embd

        self.ln = nn.Linear(n_embd, h_dim)
        self.act = nn.ReLU(h_dim)
        self.proj = nn.Linear(h_dim, n_embd)
        self.dropout = nn.Dropout1d(dropout)

    def forward(self, x):
        assert x.dim == 3, "Must be shape (B, T, C)"

        x = self.ln(x)
        x = self.act(x)
        x = self.proj(x)
        x = self.dropout(x)
        return x



class DecoderBlock(nn.Module):
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