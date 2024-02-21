import torch 
import torch.nn as nn
import torch.nn.functional as F
import math
import os
from os.path import dirname, abspath
import sys
d = dirname(dirname(abspath(__file__)))
sys.path.append(d)


''' Simple, multi-layer feed-forward network to generate music according to
the user's prefered time period. The reason for a simple archiecture is 
lack of data.'''

class TimePeriod(nn.Module):
    ''' 2 layered MLP with ReLU nonlinearity with optional norm, no dropout '''

    def __init__(self, n_embd:int, vocab_size:int, block_size:int, norm:str, 
                 n_hidden:int=50):
    
        super().__init__()

        self.n_embd = n_embd
        self.vocab_size = vocab_size
        self.block_size = block_size

        self.layers = nn.Sequential(
            nn.Embedding(self.vocab_size, self.n_embd),
            nn.Flatten(),
            nn.Linear(self.block_size*self.n_embd, n_hidden),
            nn.ReLU(n_hidden),
            nn.BatchNorm1d(n_hidden) if norm == "batch" else nn.LayerNorm(n_hidden),
            nn.Linear(n_hidden, self.vocab_size),
        )

    def forward(self, x):
        assert x.dim() == 2, "Must be shape (B, T)"
        assert x.shape[1] == self.block_size, "must have block_size elements"

        out = self.layers(x)
        return out


    def get_loss(self, yhat, y):
        assert yhat.dim() == 2, "Must be shape (B, T)"
        assert y.dim() == 1, "Must be a 1d tensor"

        loss = F.cross_entropy(yhat, y)
        return loss
    

    def generate(self, idx, num_tokens):
        for i in range(num_tokens):
            # if the context is larger than the block_size, crop it
            if idx.shape[1] > self.block_size:
                inp = idx[:, -self.block_size:]
            else:
                inp = idx

            logits = self(inp)
            probs = F.softmax(logits, dim=-1)
            next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat([idx, next], dim=-1)

        return idx

    def get_params(self):
        """ 
        Return's the number of parameters the Transformer has. Used to see 
        if I should reduce the model size.  
        Modified from https://github.com/karpathy/nanoGPT/blob/master/model.py
        """
        total_params = sum(p.numel() for p in self.parameters())
        # remove embedding parameters i.e. token embedding table
        params_no_emb = total_params - self.layers[0].weight.numel()
        return {'total parameters': total_params, 'total except embedding':params_no_emb}
