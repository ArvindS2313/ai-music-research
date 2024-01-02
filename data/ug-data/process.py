''' Processes the Ulimate Guitar (UG) data and splits it into test and val
splits for the NN. Different than POP909 in that genre and time period MLPs 
will be generated from here as well. Also, the UG dataset will have errors
in chords that will be taken care of.'''

import os
from ugdata import songs
import cleanup
import numpy as np 
import pickle
import dill

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

# clean chords and keys
rand = False
tchords = cleanup.cleanup(all_chords, rand=rand)
print(f"tchords has a length of {len(tchords)}")

# get info about the transposed chords
unique_chords = sorted(list(set([ch for s in tchords for ch in s])))
vocab_size = len(unique_chords) # num parameters for NN
# print(unique_chords)
print("all unique chords", "   ".join(unique_chords))
print("vocab size: ", vocab_size)


ctoi = {y:x+1 for x, y in enumerate(unique_chords)}
itoc = {y:x for x, y in ctoi.items()}
def convert(d):
    ctoi = {y:x+1 for x, y in enumerate(unique_chords)}
    itoc = {y:x for x, y in ctoi.items()}
    # convert int to string or string to int
    if type(d[0]) == int:
        return [itoc[i] for i in d]
    else:
        return [ctoi[c] for c in d]

# create NN splits
num_songs = len(tchords)
num_chords = sum([len(song) for song in tchords])
train_data = tchords[:int(0.9*num_songs)]
val_data = tchords[int(0.9*num_songs):]

print(f"entire data has {len(tchords)} songs")
print(f"train data has {len(train_data)} songs")
print(f"val data has {len(val_data)} songs")
print(f"entire data has {sum([len(s) for s in tchords])} chords")
print(f"train data has {sum([len(s) for s in train_data])} chords")
print(f"val data has {sum([len(s) for s in val_data])} chords")

# create integer encodings for splits
train_ids = [convert(s) for s in train_data]
val_ids = [convert(s) for s in val_data]

# make all songs have same length so can be made np.array
max_train = max([len(a) for a in train_ids])
train_ids = np.array([np.array(song + [0 for _ in range(max_train - len(song))]) for song in train_ids], dtype=np.uint16)
max_val = max([len(a) for a in val_ids])
val_ids = np.array([np.array(song + [0 for _ in range(max_val - len(song))]) for song in val_ids], dtype=np.uint16)

# exporting
info = {
    'vocab_size': vocab_size,
    'unique_chords': unique_chords,
    'ctoi': ctoi,
    'itoc': itoc,
    'max_train': max_train,
    'max_val': max_val,
    'len_td': len(train_data),
    'len_vd': len(val_data),
    'convert': convert
}

with open(os.path.join(os.path.dirname(__file__), f'ug{"-rand" if rand else ""}-info.pkl'), 'wb') as f:
    print("here, executing this command")
    dill.dump(info, f)

# export train_ids and val_ids to .bin file
train_ids.tofile(os.path.join(os.path.dirname(__file__), f'{"rand-" if rand else ""}train.bin'))
val_ids.tofile(os.path.join(os.path.dirname(__file__), f'{"rand-" if rand else ""}val.bin')) 


# Data distributions
freq_dict = {c:0 for c, i in ctoi.items()}
for s in tchords: 
    for ch in s:
        freq_dict[ch] += 1
freq_dict = {round(100*i/num_chords, 4):c for c, i in freq_dict.items()}
for k, v in sorted(freq_dict.items()):
    print(f"{k}\t\t{v}")
