import os 
import numpy as np 
from cleanup import cleanup

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

# cleanup chords and keys
cchords = cleanup(chords, keys)

for k in range(1, len(keys)):
    if keys[k][0][2] == "Db:min":
        print(k)