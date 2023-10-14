import numpy as np 
import os 

def adjust(key, chord):
    ''' Adjusts chord by converting it to its earhamonic to make it fit the key'''
    
    # chord dictionary for conversions
    chord_rep_for = { "C":"B#", "C#":"Db", "D":"Ebb", "D#":"Eb", "E":"Fb", "F":"E#", "F#":"Gb", 
                    "G":"Abb", "G#":"Ab", "A":"Bbb", "A#":"Bb", "B":"Cb"}
    chord_rep_back = {x:y for y,x in chord_rep_for.items()}
    chord_rep = chord_rep_for | chord_rep_back

    cleaned, extra = chord.split(":")


def cleanup(chords, keys):
    ''' Cleans up the chords by doing the following:
    - Removes nonchords
    - Transposes all chords to C major and roman numerals 
    - Accounts for inaccuracies in chord data 
    '''

    cchords = []
    
    # loop through each song
    for i in range(len(chords)):
        song_chords = chords[i]
        song_key = keys[i]
        tchords = []

        # loop through every chord
        for c in range(len(song_chords)):
            # check for no chord
            if song_chords[c][2] == "N":
                continue
            else:
                # determine key using ranges
                key = ""
                min, max = float(song_chords[c][0]), float(song_chords[c][1])
                for k in song_key:
                    mink, maxk = float(k[0]), float(k[1])
                    # print(f"min for key is {mink}, max for key is {maxk}")
                    if mink <= min <= max <= maxk:
                        key = k[2]

                # by the end, key should not be ""
                if key != "":
                    tchord = transpose(key, song_chords[c][2])
                

    return cchords
