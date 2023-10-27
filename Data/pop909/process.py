import os 
import numpy as np 
from cleanup import cleanup
import pickle

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
        ca_arr = np.array(ca_arr)
    with open(f"POP909/{num}/chord_midi.txt") as cm:
        cm_arr = [line.split("\t") for line in cm.read().splitlines()]
        cm_arr = np.array(cm_arr)
    with open(f"POP909/{num}/key_audio.txt") as k:
        k_arr = [line.split("\t") for line in k.read().splitlines()]
        k_arr = np.array(k_arr)

    chords.append(ca_arr)
    chords.append(cm_arr)
    keys.append(k_arr)
    keys.append(k_arr) # twice b/c the chords are getting appended twice

# cleanup chords and keys
tchords = cleanup(chords, keys)

# get info about the transposed chords
unique_chords = sorted(list(set([ch for s in tchords for ch in s])))
vocab_size = len(unique_chords) # num parameters for NN
# print(unique_chords)
print("all unique chords", "   ".join(unique_chords))
print("vocab size: ", vocab_size)


# create mappings
ctoi = {y:x for x, y in enumerate(unique_chords)}
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
# with open(os.path.join(os.path.dirname(__file__), 'info.pkl'), 'wb') as f:
#     print("here, executing this command")
#     pickle.dump(info, f)

freq_dict = {c:0 for c, i in ctoi.items()}
for s in tchords: 
    for ch in s:
        freq_dict[ch] += 1
freq_dict = {round(100*i/num_chords, 4):c for c, i in freq_dict.items()}
for k, v in sorted(freq_dict.items()):
    print(f"{k}\t\t{v}")