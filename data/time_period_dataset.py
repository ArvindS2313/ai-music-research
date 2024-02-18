import sys
import os
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

import torch
from torch.utils.data.dataloader import Dataset
from torch.utils.data.dataloader import DataLoader

from data.ugdata import songs
import data.ug_cleanup as ug_cleanup


class TimePeriodDataset(Dataset):

    def __init__(self, time_prd, rand=False, train=True, block_size=5, split=0.9):
        self.rand = rand
        self.train = train 
        self.block_size = block_size
        self.time_prd = time_prd

        self.artists = []
        self.process_times()
        self.artists = [band.strip() for band in self.lookup.keys() if self.time_prd in self.lookup[band]]

        all_chords = []
        for s in songs:
            # song is from artist of the time period
            if s[2] in self.artists:
                all_chords.append(s[5].split(","))
        self.tchords = ug_cleanup.cleanup(all_chords, rand=self.rand)
        self.enumerate()


        self.X = torch.tensor([l[i:i+self.block_size] for l in self.chords for i in range(len(l)-self.block_size)])
        self.Y = torch.tensor([l[i] for l in self.chords for i in range(self.block_size, len(l))])
        max = int(len(self.Y)*split)

        if self.train:
            self.X = self.X[:max]
            self.Y = self.Y[:max]
        else:
            self.X = self.X[max:]
            self.Y = self.Y[max:]


    def enumerate(self):
        # form set and assign numbers
        all = set()
        for s in self.tchords:
            all |= set(s)
        all = sorted(list(all))

        self.itoc = {x:y for x, y in enumerate(all)}
        self.ctoi = {y:x for x, y in self.itoc.items()}
        
        num_chords = []
        for s in self.tchords:
            num_chords.append([self.ctoi[c] for c in s])

        self.chords = num_chords


    def process_times(self):
        with open("data/time-period.txt", "r") as f:
            self.data = f.read().splitlines()

        # create dictionary: keys = band and values = list of decades
        self.lookup = {}
        for band in self.data:
            name, years = band.split("-")
            if years.strip() != "X":
                self.lookup[name] = years.strip().split("/")

    def __getitem__(self, index):
        return self.X[index], self.Y[index]
     
    def __len__(self):
        return len(self.X)
