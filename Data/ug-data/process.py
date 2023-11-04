''' Processes the Ulimate Guitar (UG) data and splits it into test and val
splits for the NN. Different than POP909 in that genre and time period MLPs 
will be generated from here as well. Also, the UG dataset will have errors
in chords that will be taken care of.'''

import os 
from ugdata import songs
import cleanup
import numpy as np 
import pickle

# big lists 
all_chords = []
artists = []


# process data
for i in range(len(songs)):
    song = songs[i]

    # append stuff to files
    chords = song[5].split(",")
    all_chords.append(np.array(chords))
    artist = song[2]
    artists.append(artist)

# clean chords and keys
tchords = cleanup.cleanup(all_chords)
print(f"tchords has a length of {len(tchords)}")


# get info about the transposed chords
unique_chords = sorted(list(set([ch for s in tchords for ch in s])))
vocab_size = len(unique_chords) # num parameters for NN
# print(unique_chords)
print("all unique chords", "   ".join(unique_chords))
print("vocab size: ", vocab_size)


# create mappings
os.chdir("../Research P1 23-24/Data/pop909")
with open("info.pkl", "rb") as f:
    info_pop909 = pickle.load(f)
    ctoi_pop909 = info_pop909['ctoi']
    itoc_pop909 = info_pop909['itoc']


# Bdim, Cdim, & F#dim in UG dataset but not in POP909
ctoi = ctoi_pop909 | {"B:dim":len(ctoi_pop909), "C:dim":len(ctoi_pop909)+1, 
                      "F#:dim":len(ctoi_pop909)+2, "Db:sus4":len(ctoi_pop909)+3 }
itoc = {y:x for x, y in ctoi.items()}
def convert(d):
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
train_ids = [np.array(convert(s)) for s in train_data]
val_ids = [np.array(convert(s)) for s in val_data]

# exporting
info = {
    'vocab_size': vocab_size,
    'num_chords': num_chords,
    'ctoi': ctoi,
    'itoc': itoc,
}

# not working? that's weird. guess we would need to import this file everytime?
with open(os.path.join(os.path.dirname(__file__), 'info.pkl'), 'wb') as f:
    print("here, executing this command")
    pickle.dump(info, f)

# Data distributions
freq_dict = {c:0 for c, i in ctoi.items()}
for s in tchords: 
    for ch in s:
        freq_dict[ch] += 1
freq_dict = {round(100*i/num_chords, 4):c for c, i in freq_dict.items()}
for k, v in sorted(freq_dict.items()):
    print(f"{k}\t\t{v}")