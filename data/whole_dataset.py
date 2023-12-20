import torch
from torch.utils.data.dataloader import Dataset
import numpy as np 
import math 
import os

''' Whole dataset combination from the pop909 and ug-data libraries'''

class WholeDataset(Dataset):

    def __init__(self):
        super().__init__()

    def __getitem__(self, index):
        return super().__getitem__(index)
    
    def __len__(self):
        pass


