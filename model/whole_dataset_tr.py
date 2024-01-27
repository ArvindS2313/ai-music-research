import torch 
import torch.nn as nn
import torch.nn.functional as F

import math
import os
from os.path import dirname, abspath
import pickle

import sys
d = dirname(dirname(abspath(__file__)))
sys.path.append(d)
from model.pos_enc import AbsPositonalEncoding


''' Simple, decode only Transformer using both the POP909 and UG datasets.
Goal is to predict, given a sequence of chords, the next chord. '''

''' This transformer archiecture will, for the majority, be implemented from
scratch. This is for three reasons:
1. I wish to implement Relative Positional Encodings (as described by Shaw et al.
and improved by Huang et al.). This isn't implemented in the nn.Transformer.
2. I wish to conduct some experiments to see which hyperparameter and setting
tunings would give better results (i.e. instead of dot product with value vector,
doing the dot product with x?).
3. It is a good learning opportunity for me to be more atuned to the Transformer
model.
4. I will use nn.TransformerDecoder, but the Decoder block is implemented 
manually.

Whole dataset NNs will be implemented using Transformers. My time period and
genre specific NNs and my genre specific NNs will be trianed using simple MLP (b/c
lack of training data lol)

References:
The following people/Github repos have heavily influenced the making of this.
1. Andrej Karpathy's NanoGPT
2. Aditya Gomatam's Music-Transformer
See the README for their Github repo links.

TODO:
- add relative positional embeddings in Attention class
- add checkpoints to model.py and train.py
'''

class Attention(nn.Module):
    ''' a multi-headed attention block'''

    def __init__(self, n_embd, n_head, block_size) -> None:
        super().__init__()
        assert n_embd % n_head == 0, "Improper parameters"

        self.n_embd = n_embd
        self.head_size = n_embd/n_head   # head_size * n_head = n_embd
        self.n_head = n_head
        self.block_size = block_size

        self.query = nn.Linear(self.n_embd, self.n_embd, bias=False) 
        self.key = nn.Linear(self.n_embd, self.n_embd, bias=False)
        self.val = nn.Linear(self.n_embd, self.n_embd, bias=False)
        self.ln = nn.Linear(self.n_embd, self.n_embd)  # final linear layer        


    def forward(self, x):
        # assert dimensionality of x
        assert x.dim() == 3, "Must be shape (B, T, C)"
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
        
        # Manual scaled dot product attention 
        # I'll implement relative encodings (Shaw et. al, Huang et. al) later
        affin = q @ k.transpose(-1, -2) / math.sqrt(self.head_size)   
        set_0 = torch.tril(torch.ones(self.block_size, self.block_size)) \
                            == torch.zeros(self.block_size, self.block_size) # T, T boolean
        affin = affin.masked_fill(set_0, float("-inf"))
        affin = affin.softmax(dim=-1)
        out = affin @ v             # (T, T) x (B, n_head, T, C) -> (B, n_head, T, C)

        out = out.transpose(1, 2).contiguous().view(batch_size, self.block_size, self.n_embd)
        return self.ln(out)
        

class MLP(nn.Module):
    ''' a feed-foward MLP: linear, ReLU, linear, dropout '''

    def __init__(self, n_embd, h_dim, bias:bool, dropout:int):
        super().__init__()

        # if no h_dim provided, make it 2*n_embd
        if h_dim == 0:
            h_dim = 2*n_embd

        self.ln = nn.Linear(n_embd, h_dim, bias)
        self.act = nn.ReLU(h_dim)
        self.proj = nn.Linear(h_dim, n_embd, bias)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        assert x.dim() == 3, "Must be shape (B, T, C)"

        x = self.ln(x)
        x = self.act(x)
        x = self.proj(x)
        x = self.dropout(x)
        return x


class DecoderBlock(nn.Module):
    ''' a Decoder block, consisting of a Multi-headed attention and a FFN.
    Normally, the LayerNorm is applied after the self attention and FFN. However,
    here, the LayerNorm will be applied before the self attention and FFN. 
    '''

    def __init__(self, n_embd, n_head, h_dim, block_size, dropout=0.0, ffn_bias=True, layernorm_eps=1e-6):
        super().__init__()
        self.n_embd = n_embd
        self.n_head = n_head
        self.block_size = block_size

        # Define LayerNorm layers (will go before SA & FFN)
        self.layernorm1 = nn.LayerNorm(self.n_embd, eps=layernorm_eps)
        self.layernorm2 = nn.LayerNorm(self.n_embd, eps=layernorm_eps)

        # Attention and MLP
        self.sa = Attention(self.n_embd, self.n_head, self.block_size)
        self.mlp = MLP(self.n_embd, h_dim, ffn_bias, dropout)

    def forward(self, x):
        assert x.dim() == 3, "Must be shape (B, T, C)"

        ln_x = self.layernorm1(x)
        sa_x = self.sa(ln_x)
        x = x + sa_x   # residual connection for SA

        ln_x = self.layernorm2(x)
        mlp_x = self.mlp(ln_x)
        x = x + mlp_x  # residual connection for MLP

        return x 
    


class WholeDatasetTransformer(nn.Module):
    ''' Implements a decoder only, Transformer using Multi-Headed 
    Attention and an MLP. Uses the torch.nn.TransformerDecoder archiecture'''

    def __init__(self, n_embd: int, n_layers: int, vocab_size: int, 
                 n_head: int, h_dim: int, block_size: int, dropout: int = 0.0, 
                 ffn_bias=True, layernorm_eps=1e-6):
        
        super().__init__()
        self.block_size = block_size
        self.n_embd = n_embd
        self.n_layers = n_layers
        self.vocab_size = vocab_size

        self.abs_pe = AbsPositonalEncoding(self.block_size, self.n_embd, dropout)
        self.token_emb = nn.Embedding(self.vocab_size, self.n_embd)
        self.dropout = nn.Dropout(dropout)
        self.ln = nn.LayerNorm(self.n_embd, eps=layernorm_eps)

        # Transformer Decoder which uses DecoderBlock class
        self.decoder = nn.ModuleList([DecoderBlock(n_embd, n_head, h_dim, block_size, 
                                                   dropout, ffn_bias, layernorm_eps) for _ in range(n_layers)])
        self.lm_head = nn.Linear(self.n_embd, self.vocab_size) 

    
    def get_params(self):
        """ 
        Return's the number of parameters the Transformer has. Used to see 
        if I should reduce the model size.  
        Modified from https://github.com/karpathy/nanoGPT/blob/master/model.py
        """
        total_params = sum(p.numel() for p in self.parameters())
        # remove embedding parameters i.e. token embedding table
        params_no_emb = total_params - self.token_emb.weight.numel()
        return {'total parameters': total_params, 'total except embedding':params_no_emb}


    def forward(self, x):
        assert x.dim() == 2, "Must be of shape (B, T)"
        assert x.shape[1] <= self.block_size, f"Your input is {x.shape[1]} tokens. Cannot process \
                                                inputs which have more than {self.block_size} tokens."

        # forward the Music Transformer
        x = self.token_emb(x)
        x += self.abs_pe(x)
        x = self.dropout(x)

        for layer in self.decoder:
            x = layer(x)

        x = self.ln(x)

        x = self.ln(x)
        logits = self.lm_head(x) 
        return logits
    

    def get_loss(self, yhat, y, lf=F.cross_entropy):
        assert y.dim() == 2, "Logits must be of shape (B, T, C)"
        assert yhat.dim() == 3, "Predictions must be of shape (B, T)"

        yhat = yhat.view(yhat.shape[0]*yhat.shape[1], yhat.shape[2])   # (B*T, C)
        y = y.view(y.shape[0]*y.shape[1])                     # (B*T)
        loss = lf(yhat, y)

        return loss


    def generate(self, idx=None, num_tokens=1):
        ''' generation function for NN'''

        for i in range(num_tokens):
            # if the context is larger than the block_size, crop it
            if idx.shape[1] > self.block_size:
                inp = idx[:, -self.block_size:]
            else:
                inp = idx

            logits = self(inp)
            norm_logits = F.softmax(logits, dim=-1)
            probs = norm_logits[:, -1, :]
            next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat([idx, next], dim=-1)

        return idx



        
        

