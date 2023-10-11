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

def convert(chord):
    ''' Change the chord so that it is 'nicer' in C major'''

    # change bad to good chords
    chord = chord.replace("Fb", "E")
    chord = chord.replace("Cb", "B")
    chord = chord.replace("E#", "F")
    chord = chord.replace("B#", "C")
    chord = chord.replace("A#", "Bb")
    chord = chord.replace("D#", "Eb")
    

    # replace sus with sus4
    if "sus" in chord and "sus4" not in chord and "sus2" not in chord:
        chord = chord.replace("sus", "sus4")
    
    # parenthesis that shouldn't be there
    chord = chord.replace("(", "")
    chord = chord.replace(")", "")

    return chord

print(convert("Asus"))