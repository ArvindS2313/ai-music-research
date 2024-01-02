import os 
import numpy as np 
from cleanup import cleanup
import pickle
import dill

''' Prepare the POP909 data to be used for the NN. This includes a call 
to the cleanup function which will change chords if necessary'''

# "Big" arrays
chords = []
keys = []


# download/get data files
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

# cleanup chords and keys
rand = True
tchords = cleanup(chords, keys, rand=rand)

# get info about the transposed chords
unique_chords = sorted(list(set([ch for s in tchords for ch in s])))
vocab_size = len(unique_chords) # num parameters for NN
# print(unique_chords)
print("all unique chords", "   ".join(unique_chords))
print("vocab size: ", vocab_size)


# create mappings
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

# not working? that's weird. guess we would need to import this file everytime?
with open(os.path.join(os.path.dirname(__file__), f'pop909{"-rand" if rand else ""}-info.pkl'), 'wb') as f:
    print("here, executing this command")
    dill.dump(info, f)


# export train_ids and val_ids to .bin file
train_ids.tofile(os.path.join(os.path.dirname(__file__), f'{"rand-" if rand else ""}train.bin'))
val_ids.tofile(os.path.join(os.path.dirname(__file__), f'{"rand-" if rand else ""}val.bin')) 

freq_dict = {c:0 for c, i in ctoi.items()}
for s in tchords: 
    for ch in s:
        freq_dict[ch] += 1
freq_dict = {round(100*i/num_chords, 4):c for c, i in freq_dict.items()}
for k, v in sorted(freq_dict.items()):
    print(f"{k}\t\t{v}")
