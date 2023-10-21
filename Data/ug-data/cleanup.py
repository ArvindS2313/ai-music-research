import numpy as np 
import os

''' Cleanup and transpose the chords to C major. Consists of multiple functions.'''

def cleanup(all_chords):
    ''' main method'''

    all_tchords = []
    # loop over all of the songs
    for s in range(len(all_chords)):
        song = all_chords[s]
        key = ""
        
        # loop over each chord
        for c in range(len(song)):
            uchord = song[c]

            # take care of maj/min
            uchord = uchord.replace("min", "m")
            if "maj" in uchord and "7" not in uchord:
                uchord = uchord.replace("maj", "")

            cchord = simplify_chord(uchord)
            echord = uchord[len(cchord):] 
            tchord = transpose(cchord, key) + echord
            


    return ""


def transpose(chord, key):
    ''' transposes cleaned chord to given key'''
    keys = ["Bbb", "Fb", "Cb", "Gb", "Db", "Ab", "Eb", "Bb", "F", "C", "G", "D", 
            "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "E#", "B#"] # list of keys
    final = "C"
    diff = keys.index(final) - keys.index(key) # diff between final & initial key

    tchords = []
    try:
        if "m" in c:
            # it is a minor chord
            c = c.replace("m", "")
            tc = keys[keys.index(c)+diff] + "m"
        else:
            # get index, add difference, and assign new key
            tc = keys[keys.index(c)+diff]
    except ValueError:
        tc = "C"

    return tc


def simplify_chord(chord):
    ''' return a cleaned up version of the complex chord'''

    # handle maj execptions
    if "maj" in chord:
        return chord[:chord.find("m")]

    chord = chord.replace("min", "m")
    if len(chord) == 1:
        return chord
    if len(chord) == 2:
        # either Xb, X#, Xm, or XY
        if chord[1] in ["b", "#", "m"]:
            return chord
        else:
            return chord[0]
    if len(chord) >= 3:
        if chord[2] == "m":
            return chord[:3]
        else:
            return chord[:2]
         
    



def get_parts(chord):
    ''' Determines the 'end' part of a chord'''

    start = ""
    end = ""
    
    
    if len(chord) == 1:
          start = chord
          end = ""
    if "m" in chord: 
        if "dim" in chord: 
            # doing this because 'dim' will have 'm' in it
            start = chord[:chord.find('dim')]
            end = chord[chord.find('dim'):]
        elif "maj" in chord:
            start = chord[:chord.find('maj')-4]
            end = chord[chord.find('maj')-4:]
        else:
            # it is a minor chord but not a dim chord
            start = chord[:chord.find('m')+1]
            end = chord[chord.find('m')+1:]
    elif "add" not in chord and "sus" not in chord and "aug" not in chord:
         # some form of major chord
        start += 'maj'

    return start, end 


def fix(chord):
    ''' changes format and adjusts the complex chord to make it simpler'''

    # get rid of inversions
    if "/" in chord:
            chord = chord[:chord.find('/')]

    # change ending to make it simpler
    schord, echord = get_parts(chord)
    allowed = ["7", "dim", "maj", "min", "sus2", "sus4", "min7", "maj7", "b7"]

    final_end = ""
    if echord in allowed:
        final_end = echord
    for e in allowed:
        if e in echord:
            final_end = e
            
    # error check: is final_end empty?
    if final_end == "":
        final_end = "maj"

    return schord + final_end


# print("qwerty"[len("qw"):])
# print(cleanup([["A", "B#m7b4", "Cm73"]]))
print(simplify_chord("Adim"))