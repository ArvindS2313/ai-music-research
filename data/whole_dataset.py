import torch
from torch.utils.data.dataloader import Dataset
import numpy as np 
import math 
import os

''' Whole dataset combination from the pop909 and ug-data libraries'''

class WholeDataset(Dataset): 
    
    def __init__(self, train=True): 
        super().__init__()
        
        # load data from pop909 and ug-data and combine them 
        pop909dir = os.path.join("pop909")
        ugdir = os.path.join("ug-data")
        type = "train" if train else "val"

        self.data = {
            f"pop909-rand-{type}": os.path.join("data", pop909dir, f"rand-{type}.bin"),
            f"pop909-{type}": os.path.join("data", pop909dir, f"{type}.bin"),
            f"ug-rand-{type}": os.path.join("data", ugdir, f"rand-{type}.bin"),
            f"ug-{type}": os.path.join("data", ugdir, f"{type}.bin"),
        }




    def __getitem__(self, index):
        return super().__getitem__(index)
     
    def __len__(self):
        pass
