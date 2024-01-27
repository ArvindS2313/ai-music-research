import torch 
from  data.whole_dataset import WholeDataset
import model.whole_dataset_tr


''' 
Generation function for all types of music models -- Whole Dataset Transformers and the Genre/Time 
Period MLPs. Called from the generate function inside each of the class definitions.
Supports two different types of generation processes: fixed tokens or regressive tokens.
    - Fixed token generation will generate a set number (us er specified) of chords.
    - Regressive generation will generate chord sequences until the stop (<EOS>) token.
'''


# Basic version, for now
def generate(block_size=10, num_tokens=1):
    path = 'saved-models/model.pth'
    tr_model = torch.load(path)
    tr_model.eval()

    itoc = WholeDataset(rand=True).itoc
    ctoi = WholeDataset(rand=True).ctoi
    context = torch.tensor([[ctoi["C:maj"] for i in range(block_size)]])
    chords = tr_model.generate(idx=context, num_tokens=num_tokens)
    chords = [itoc[c] for c in chords.tolist()[0]]
    return chords


print(generate(num_tokens=40))

