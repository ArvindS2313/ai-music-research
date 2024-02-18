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
    

    def generate(self, context, num_tokens):
        assert context.dim() == 2, "Must be shape (B, T)"
        assert self.eval, "Must be in evaluation mode"
    
         # only last block_size elements are allowed
        context = context[:, -self.block_size:]

        # duplicate if less than block_size context provided
        context = context.repeat(0, math.ceil(self.block_size/context.shape[1]))    

        for _ in range(num_tokens):
            logits = self(context)
            probs = F.softmax(logits, dim=-1)
            pred = torch.multinomial(probs, num_samples=1)
            context = torch.cat((context[:, 1:], pred), dim=1)

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
