import torch 
from data.whole_dataset import WholeDataset
from data.time_period_dataset import TimePeriodDataset

''' 
Generation function for all types of music models -- Whole Dataset Transformers and the Genre/Time 
Period MLPs. Called from the generate function inside each of the class definitions.
Supports two different types of generation processes: fixed tokens or regressive tokens.
    - Fixed token generation will generate a set number (us er specified) of chords.
    - Regressive generation will generate chord sequences until the stop (<EOS>) token.
'''

def tr_gen(path, context: list , block_size=20, num_tokens=1):
    assert len(context) == block_size
    model = torch.load(path)
    model.eval()

    # get itoc and ctoi 
    itoc = WholeDataset().itoc
    ctoi = WholeDataset().ctoi

    idx = torch.tensor([[ctoi[c] for c in context]]) # batch_size = 1
    chords = model.generate(idx=idx, num_tokens=num_tokens)
    chords = [itoc[c] for c in chords.tolist()[0]]
    return chords


def mlp_gen(type, kind, context, path=None, block_size=5, num_tokens=1):
    assert len(context) == block_size
    
    if path is None:
        path = f"saved-models/{kind}s.pth"
    model = torch.load(path)
    model.eval()

    if type == "time":
        itoc = TimePeriodDataset(time_prd=kind).itoc
        ctoi = TimePeriodDataset(time_prd=kind).ctoi

    idx = torch.tensor([[ctoi[c] for c in context]])
    chords = model.generate(idx=idx, num_tokens=num_tokens)
    chords = [itoc[c] for c in chords.tolist()[0]]
    return chords

context1 = ["C:maj7", "D:min", "D:maj", "G:maj", "G:maj", "E:min7", "A:min", "A:maj", "D:maj7", 
            "B:min", "G:maj", "G:sus4", "G:sus4", "C:maj", "G:maj", "F:maj7", "C:maj", "G:sus4", "A:min", "A:min"]
context2 = ["C:maj", "E:min", "D:min", "G:maj", "D:maj", "B:min", "F#:min", "G:maj", "G:maj"]
context3 = ["G:maj", "G:maj", "A:min", "A:maj", "E:maj", "E:min", "A:min7", "C:maj", "C:maj"]
context4 = ["D:min", "G:min", "G:maj", "G:min", "F:maj", "F:min", "G:min", "C:maj", "C:maj"]
context5 = ["C:maj", "E:min", "D:min", "C:maj", "G:maj"]
context6 = ["C:maj", "A:min", "G:maj", "G:maj", "B:min"]

# chords = mlp_gen(type="time", kind="70", context=context4, block_size=9, num_tokens=20)
# # append to file
# with open("70s-chords.txt", "a") as f:
#     f.write('    '.join(chords))
#     f.write('\n')

