import sys
import os
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

import torch
from torch.utils.data.dataloader import Dataset
import time

from data.ugdata import songs
import data.ug_cleanup as ug_cleanup
import data.pop909_cleanup as pop909_cleanup


''' Whole dataset combination from the pop909 and ug-data libraries'''

def clean_pop909(rand=False):
    # "Big" arrays
    chords = []
    keys = []

    # download/get data files
    if os.getcwd() == d:
        os.chdir("../")
    for i in range(1, 910): # pop909 has 909 songs
        num = f"{'0'*(3-len(str(i)))}{i}"
        # read in data, split, and convert to nparray
        with open(f"POP909/{num}/chord_audio.txt") as ca:
            ca_arr = [line.split("\t") for line in ca.read().splitlines()]
        with open(f"POP909/{num}/chord_midi.txt") as cm:
            cm_arr = [line.split("\t") for line in cm.read().splitlines()]
        with open(f"POP909/{num}/key_audio.txt") as k:
            k_arr = [line.split("\t") for line in k.read().splitlines()]

        chords.append(ca_arr)
        chords.append(cm_arr)
        keys.append(k_arr)
        keys.append(k_arr) # twice b/c the chords are getting appended twice


    tchords = pop909_cleanup.cleanup(chords, keys, rand=rand)
    return tchords
    

def clean_ug(rand=False):
    # big lists 
    all_chords = []
    artists = []

    # process data
    for i in range(len(songs)):
        song = songs[i]

        # append stuff to files
        chords = song[5].split(",")
        all_chords.append(chords)
        artist = song[2]
        artists.append(artist)

    tchords = ug_cleanup.cleanup(all_chords, rand=rand)
    return tchords
     

class WholeDataset(Dataset):
    '''
    1. Preprocesses the data from respective files and transposes into C major
    2. Converts to numerical representation and saved an itoc and a ctoi
    3. Uses PyTorch to save the entire representation to be used in train.py
    '''

    def __init__(self, rand=False, train=True, block_size=8, split=0.9):
        super().__init__()
        self.rand = rand    
        self.train = train
        self.block_size = block_size
        self.enumerate()

        self.X = torch.tensor([l[i:i+block_size] for l in self.chords for i in range(len(l)-self.block_size)])
        self.Y = torch.tensor([l[i:i+block_size] for l in self.chords for i in range(1, len(l)-self.block_size+1)])
        max = int(len(self.Y)*split)

        if self.train:
            self.X = self.X[:max]
            self.Y = self.Y[:max]
        else:
            self.X = self.X[max:]
            self.Y = self.Y[max:]

        
    def enumerate(self):
        self.ug_chords = clean_ug(self.rand)
        self.pop909_chords = clean_pop909(self.rand)
        self.chords = self.ug_chords # + self.pop909_chords
 
        # form set and assign numbers
        all = set()
        for s in self.chords:
            all |= set(s)
        all = sorted(list(all))

        self.itoc = {x:y for x, y in enumerate(all)}
        self.ctoi = {y:x for x, y in self.itoc.items()}
        
        num_chords = []
        for s in self.chords:
            num_chords.append([self.ctoi[c] for c in s])

        self.chords = num_chords


    def __getitem__(self, index):
        return self.X[index], self.Y[index]
     
    def __len__(self):
        return len(self.X)

