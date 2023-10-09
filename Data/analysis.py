import process
from ugdata import songs

def get_bands():
    return set([s[2] for s in songs])

def max_bands():
    band_dict = {}
    for s in songs:
        if s[2] not in band_dict:
            band_dict[s[2]] = 1
        else:
            band_dict[s[2]] += 1

    # long lol
    return [(x, y) for x, y in reversed(sorted([(y, x) for x, y in band_dict.items()]))]

print(max_bands())