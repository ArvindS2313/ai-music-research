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
def generate(block_size=20, num_tokens=1):
    path = 'saved-models/model.pth'
    tr_model = torch.load(path)
    tr_model.eval()

    itoc = WholeDataset().combined_itoc
    ctoi = WholeDataset().combined_ctoi

    context = torch.tensor([[ctoi["C:maj"]]]).repeat(1, block_size)
    chords = [itoc[x] for x in tr_model.generate(idx=context, num_tokens=80).tolist()[0]][60:]
    return chords



print(generate())

