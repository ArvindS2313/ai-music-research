import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class AbsPositonalEncoding(nn.Module):
    ''' Definition of an absolute positional encoding. I'll also be using 
    relative positional encodings (i.e. nn.Embedding) but putting these in 
    as well.'''

    def __init__(self, block_size: int, n_embd: int, dropout=0.0):
        super().__init__()

        self.block_size = block_size
        self.n_embd = n_embd
        self.dropout = nn.Dropout(dropout) if dropout is not None else None
        self.pe = torch.zeros(self.block_size, self.n_embd)

        # case when dealing with even dimension
        even = torch.arange(0, n_embd, 2)
        denom_even = torch.pow(10000, even/self.n_embd)
        odd = torch.arange(1, n_embd, 2)
        denom_odd = torch.pow(10000, (odd-1)/self.n_embd)
 






    def forward(self, x):
        assert x.dim == 3, "Must be of shape (B, T, C)"

        x = x + self.pe
        if self.dropout is not None:
            x = self.dropout(x)
        return x