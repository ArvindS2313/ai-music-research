import numpy as np 
import os 

def transpose(key, chord):
    ''' Transpose chord in a given key to C major or A minor'''
    
    # a lot of extras; better be safe than sorry
    chord_order = ["Fbb", "Cbb", "Gbb", "Dbb", "Abb", "Ebb", "Bbb", "Fb", "Cb", "Gb", "Db", 
                   "Ab", "Eb", "Bb", "F", "C", "G", "D", "A", "E", "B", "F#", "C#", "G#", 
                   "D#", "A#", "E#", "B#", "F##", "C##", "G##", "D##", "A##", "E##", "B##"]
    
    cchord, echord = chord.split(":")
    if "min" in key:
        final_key = "A"
    if "maj" in key:
        final_key = "C"
    ckey, _ = key.split(":")

    # get indicies and convert
    index_key = chord_order.index(ckey)
    index_final_key = chord_order.index(final_key)
    diff = index_final_key - index_key

    index_cchord = chord_order.index(cchord)
    new_index = index_cchord + diff
    # create transposed chord
    tchord = chord_order[new_index] + ":" + echord

    return tchord


def change_key(key):
    ''' Replaces extreme flats with better sharps'''
    key = key.replace("Gb", "F#")
    key = key.replace("Db", "C#")
    key = key.replace("Cb", "B")
    return key


def adjust(chord):
    ''' Make chord "better" in C major. '''    

    allowed_maj = ["C", "G", "D", "A", "E", "B", "F", "Bb", "Eb", "Ab", "Db"]
    notallowed_maj = [["B#", "Dbb"], ["F##", "Abb"], ["C##", "Ebb"], ["G##", "Bbb"], 
                      ["D##", "Fb"], ["A##", "Cb"], ["E#", "Gbb"], ["A#", "Cbb"], 
                      ["D#", "Fbb"], ["G#"], ["C#", "B##"]]
    allowed_min = ["A", "E", "B", "F#", "C#", "G#", "D", "G", "C", "F", "Bb"]
    notallowed_min = [["G##", "Bbb"], ["D##", "Fb"], ["A##", "Cb"], ["Ebb", "Gb"], 
                      ["B##", "Db"], ["Ab"], ["B#", "Dbb"], ["F##", "Abb"], 
                      ["C##", "Ebb"],  ["E#", "Gbb"], ["A#", "Cbb"]]

    cchord, echord = chord.split(":")
    echord = ":" + simplify(echord) # add : to extra
    new_chord = ""
    
    # take care of F#, Gb, Ebm, D#m
    if "maj" in echord or "sus" in echord:
        if cchord in allowed_maj:
            new_chord = cchord
        else:
            for p in range(len(notallowed_maj)):
                if cchord in notallowed_maj[p]:
                    # if the cleaned chord is one of the not allowed chords
                    new_chord = allowed_maj[p]
    if "min" in echord:
        if cchord in allowed_min:
            new_chord = cchord
        else:
            for p in range(len(notallowed_min)):
                if cchord in notallowed_min[p]:
                    # if the cleaned chord is one of the not allowed chords
                    new_chord = allowed_min[p]

    if new_chord == "":
        new_chord = "C" if "maj" in echord else "A"
    
    return new_chord + echord


def simplify(end):
    ''' Simplifies the ending of the chord to one of the six allowed types'''

    allowed = ["7", "dim", "maj", "min", "sus2", "sus4", "min7", "maj7"]
    final_end = ""

    if end in allowed:
        final_end = end
    for e in allowed:
        if e in end:
            final_end = e
            
    # error check: is final_end empty?
    if final_end == "":
        final_end = "maj"

    return final_end


def cleanup(chords, keys):
    ''' Cleans up the chords by doing the following:
    - Removes nonchords
    - Transposes all chords to C major and roman numerals 
    - Accounts for inaccuracies in chord data 
    '''

    all_tchords = []
    
    # loop through each song
    for i in range(len(chords)):
        song_chords = chords[i]
        song_keys = keys[i]
        tchords = []

        # loop through every chord
        for c in range(len(song_chords)):
            # check for no chord
            if song_chords[c][2] == "N":
                continue
            else:
                # determine key using ranges
                key = ""
                minc, maxc = float(song_chords[c][0]), float(song_chords[c][1])

                for k in song_keys:
                    mink, maxk = float(k[0]), float(k[1])
                    if mink <= minc <= maxc <= maxk:
                        # assign key if ranges work out
                        key = k[2]

                # change key if needed
                key = change_key(key)
                if key != "":
                    tchord = adjust(transpose(key, song_chords[c][2]))
                    tchords.append(tchord)
    
        all_tchords.append(tchords)

    return all_tchords
