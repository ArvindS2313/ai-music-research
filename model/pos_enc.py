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

        self.dropout = nn.Dropout(dropout) if dropout is not None else None
        
        self.enc = torch.zeros((block_size, 0))   # positional encoding 
        ind = torch.arange(0, n_embd, 2)  
        for i in ind:
            sin = torch.sin(torch.arange(block_size)/torch.pow(10000, torch.tensor([i])/n_embd)).view(block_size, 1)
            cos = torch.sin(torch.arange(block_size)/torch.pow(10000, torch.tensor([i])/n_embd)).view(block_size, 1)
            self.enc = torch.cat((self.enc, sin, cos), 1)


    def forward(self, x):
        assert x.dim() == 3, "Must be of shape (B, T, C)"

        x = x + self.enc
        if self.dropout is not None:
            x = self.dropout(x)
        return x