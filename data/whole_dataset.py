import torch
from torch.utils.data.dataloader import Dataset, DataLoader
import numpy as np 
import dill
import pickle
import os

''' Whole dataset combination from the pop909 and ug-data libraries'''

class WholeDataset(Dataset): 
    
    def __init__(self, train=True, rand=True, block_size=8): 
        super().__init__()

        self.train = train
        self.type = "train" if self.train else "val"
        self.rand = rand
        self.block_size = block_size

        pop909_ids, ug_ids = self._get_ids()
        ids = pop909_ids + ug_ids
        self.X = torch.tensor([l[i:i+block_size] for l in ids for i in range(len(l)-self.block_size)])
        self.Y = torch.tensor([l[i:i+block_size] for l in ids for i in range(1, len(l)-self.block_size+1)])


    def _get_ids(self):
        # load data from pop909 and ug-data and combine them 
        pop909dir = os.path.join("pop909")
        ugdir = os.path.join("ug-data")
        pop909_bin = os.path.join("data", pop909dir, f"{'rand-' if self.rand else ''}{self.type}.bin")
        ug_bin = os.path.join("data", ugdir, f"{'rand-' if self.rand else ''}{self.type}.bin")

        # retrieve and load pkl files 
        pop909_pkl = os.path.join("data", pop909dir, f"pop909-{'rand-' if self.rand else ''}info.pkl")
        ug_pkl = os.path.join("data", ugdir, f"ug-{'rand-' if self.rand else ''}info.pkl")
        with open(pop909_pkl, 'rb') as f:
            pop909_info = dill.load(f)
        with open(ug_pkl, 'rb') as f:
            ug_info = dill.load(f)

        # get the pop909/ug ids
        pop909_ids = np.fromfile(pop909_bin, dtype=np.uint16).reshape(
            pop909_info[f'len_{"td" if self.train else "vd"}'], pop909_info[f'max_{self.type}']).tolist()
        ug_ids = np.fromfile(ug_bin, dtype=np.uint16).reshape(
            ug_info[f'len_{"td" if self.train else "vd"}'], ug_info[f'max_{self.type}']).tolist()
        pop909_ids = [l[:l.index(0)] if 0 in l else l for l in pop909_ids]
        ug_ids = [l[:l.index(0)] if 0 in l else l for l in ug_ids]

        # convert and re-embed to numbers
        pop909_ids = [[pop909_info['itoc'][c] for c in s] for s in pop909_ids]
        ug_ids = [[pop909_info['itoc'][c] for c in s] for s in ug_ids]
        self.combined_itoc = self.get_vocab()
        self.combined_ctoi = {y:x for x,y in self.combined_itoc.items()}

        pop909_ids = [[self.combined_ctoi[c] for c in s] for s in pop909_ids]
        ug_ids = [[self.combined_ctoi[c] for c in s] for s in ug_ids]

        return pop909_ids, ug_ids

    def get_vocab(self):
        pop909dir = os.path.join("pop909")
        ugdir = os.path.join("ug-data")

        pop909_rand = os.path.join("data", pop909dir, f"pop909-rand-info.pkl")
        pop909 = os.path.join("data", pop909dir, f"pop909-info.pkl")
        ug_rand = os.path.join("data", ugdir, f"ug-rand-info.pkl")
        ug = os.path.join("data", ugdir, f"ug-info.pkl")

        vocab = set()
        for p in [pop909_rand, pop909, ug_rand, ug]:
            with open(p, 'rb') as f:
                info = dill.load(f)
                vocab |= set(info['unique_chords'])

        return dict(enumerate(vocab))


    def __getitem__(self, index):
        return self.X[index], self.Y[index]
     
    def __len__(self):
        return len(self.X)
    