import torch 
from  data.whole_dataset import WholeDataset
from data.time_period_dataset import TimePeriodDataset
import os

''' 
Generation function for all types of music models -- Whole Dataset Transformers and the Genre/Time 
Period MLPs. Called from the generate function inside each of the class definitions.
Supports two different types of generation processes: fixed tokens or regressive tokens.
    - Fixed token generation will generate a set number (us er specified) of chords.
    - Regressive generation will generate chord sequences until the stop (<EOS>) token.
'''


# Basic version, for now
def generate(block_size=20, num_tokens=1, start="C:maj", rand=True):
    path = f"saved-models/time-prd.pth"
    model = torch.load(path)
    model.eval()

    itoc = TimePeriodDataset(time_prd="00", rand=rand).itoc
    ctoi = TimePeriodDataset(time_prd="00", rand=rand).ctoi
    context = torch.tensor([[ctoi[start] for _ in range(block_size)]])
    chords = model.generate(context=context, num_tokens=num_tokens)
    chords = [itoc[c] for c in chords.tolist()[0]]
    return chords

# rand_chords = generate(block_size=20, num_tokens=20, start="C:maj", rand=True)
# print(' '.join(rand_chords))
# # append to random file
# with open("Research P1 23-24/rand-chords.txt", "a") as f:
#     f.write('    '.join(rand_chords))
#     f.write('\n')

    
chords = generate(block_size=9, num_tokens=20, start="C:maj", rand=False)
print('    '.join(chords))
# append to random file
with open("Research P1 23-24/chords.txt", "a") as f:
    f.write('    '.join(chords))
    f.write('\n')