import numpy as np 
import os
import random

''' Cleanup and transpose the chords to C major. Consists of multiple functions.'''

def cleanup(all_chords):
    ''' main method'''

    all_tchords = []
    # loop over all of the songs
    for s in range(len(all_chords)):
        # print(f"Currently on song {s}.")
        song = all_chords[s]
        cchords = []
        echords = []
        tchords = []
        
        # loop over each chord
        for c in range(len(song)):
            uchord = song[c]
            # print(f"Current chord: {uchord}")

            # take care of maj/min
            uchord = uchord.replace("min", "m")
            if "maj" in uchord and "7" not in uchord:
                uchord = uchord.replace("maj", "")

            cchord = clean(uchord)
            # print(f"Cleaned chord: {cchord}")
            cchords.append(cchord)
            echord = uchord[len(cchord):] 
            # print(f"Extra part of chord: {echord}")
            echords.append(echord)

        key = get_key(cchords)
        # print(f"The key of the song is {key} major")
        # print("This will be transposed into C major now.")

        for c in range(len(song)):
            cchord = cchords[c]
            echord = echords[c]
            tchord = transpose(cchord, key) + echord
            # print(f"Chord went from {cchord + echord} to {tchord}")
            tchord = randomize(adjust(simplify_end(tchord)))
            # print(f"FINAL tchord: {tchord}")
            tchords.append(tchord)

        all_tchords.append(np.array(tchords))
                
    return all_tchords


def simplify_end(chord):
    ''' Changes ending to maj, min, dim, sus, 7, maj7, min7'''

    # new clean chord and end chord to make the simplication easier
    acc = ["#", "b"]
    if len(chord) == 1:
        start = chord
        end = ""
    elif chord[1] in acc:
        start = chord[:2]
        end = chord[2:]
    else:
        start = chord[:1]
        end = chord[1:]
    
    final_end = ""
    # no switch statements in python, lol
    if end == "":
        # no ending = major
        final_end = ":maj"
    elif "maj7" in end:
        final_end = ":maj7"
    elif "m7" in end:
        final_end = ":min7"
    elif "dim" in end:
        final_end = ":dim"
    elif "sus4" in end:
        final_end = ":sus4"
    elif "sus2" in end:
        final_end = ":sus2"
    elif "m" in end:
        final_end = ":min"
    elif "b7" in end:
        final_end = ":b7"
    # elif "7" in end:
    #     final_end = ":7"
    else:
        # default to major if nothing works
        final_end = ":maj"
    
    return start + final_end


def get_key(chords):
    ''' determines key based on heuristic algorithm. it may be wrong due to key changes
    or just bad chords entered.'''

    CHARTS = {
    "C": ["C", "Dm", "Em", "F", "G", "Am", "Bdim"],
    "G": ["G", "Am", "Bm", "C", "D", "Em", "F#dim"],
    "D": ["D", "Em", "F#m", "G", "A", "Bm", "C#dim"],
    "A": ["A", "Bm", "C#m", "D", "E", "F#m", "G#dim"],
    "E": ["E", "F#m", "G#m", "A", "B", "C#m", "D#dim"],
    "B": ["B", "C#m", "D#m", "E", "F#", "G#m", "A#dim"],
    "F#": ["F#", "G#m", "A#m", "B", "C#", "D#m", "E#dim"],
    "C#": ["C#", "D#m", "E#m", "F#", "G#", "A#m", "B#dim"],
    "F": ["F", "Gm", "Am", "Bb", "C", "Dm", "Edim"],
    "Bb": ["Bb", "Cm", "Dm", "Eb", "F", "Gm", "Adim"],
    "Eb": ["Eb", "Fm", "Gm", "Ab", "Bb", "Cm", "Ddim"],
    "Ab": ["Ab", "Bbm", "Cm", "Db", "Eb", "Fm", "Gdim"],
    "Db": ["Db", "Ebm", "Fm", "Gb", "Ab", "Bbm", "Cdim"],
    "Gb": ["Gb", "Abm", "Bbm", "Cb", "Db", "Ebm", "Fdim"],
    "Cb": ["Cb", "Dbm", "Ebm", "Fb", "Gb", "Abm", "Bbdim"],
    }
    itok = {x:y for x,y in enumerate(CHARTS.keys())}


    counts = [0 for _ in range(len(itok))]
    # loop over all of the chords
    for c in chords:
        # print(f"chord {c} on right now")
        for i in range(len(itok)):
            # loop over all of the potential keys
            inkey = CHARTS[itok[i]] # inkey = list of allowed chords for key
            if c in inkey:
                # print(f"chord in key of {itok[i]}")
                counts[i] += 1
                # if chord in allowed chords for that key, that key is a potential winner
    
    # DEBUG ONLY - print out key, count pair
    # for i in range(len(counts)):
    #     print(itok[i], counts[i])

    return itok[counts.index(max(counts))]


def transpose(c, key):
    ''' transposes cleaned chord to given key'''
    keys = ["Dbb", "Abb", "Ebb", "Bbb", "Fb", "Cb", "Gb", "Db", "Ab", "Eb", "Bb", 
            "F", "C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "E#", 
            "B#", "F##", "C##", "G##", "D##"] # list of keys including theoreticals
    final = "C" # final key is C
    diff = keys.index(final) - keys.index(key) # diff between final & initial key

    try:
        if "m" in c:
            if "dim" in c:
                # it is a dim chord
                c = c.replace("dim", "")
                tc = keys[keys.index(c)+diff] + "dim"
            else:
                # it is a minor chord
                c = c.replace("m", "")
                tc = keys[keys.index(c)+diff] + "m"
        else:
            # get index, add difference, and assign new key
            tc = keys[keys.index(c)+diff]
    except ValueError:
        tc = "C"

    return tc


def clean(chord):
    ''' return a cleaned up version of the complex chord'''

    # handle maj execptions
    if "maj" in chord:
        return chord[:chord.find("m")]
    # handle dim execeptions:
    if "dim" in chord:
        return chord[:chord.find("dim")+3]
    chord = chord.replace("min", "m") # 'min' is not allowed

    letters = ["A", "B", "C", "D", "E", "F", "G"]
    symbols = ["b", "#", "m"]
    cchord = ""

    # once the chars of the chord are not part of letters/symbols, you've reached end of 
    # the clean key
    for char in chord:
        if char in letters or char in symbols:
            cchord += char
        else:
            break

    return cchord


def adjust(chord):
    ''' Make chord "better" in C major. '''    

    # allowed and notallowed major, minor, and diminished chords
    allowed_maj = ["C", "G", "D", "A", "E", "B", "F", "Bb", "Eb", "Ab", "Db"]
    allowed_min = ["A", "E", "B", "F#", "C#", "G#", "D", "G", "C", "F", "Bb"]
    notallowed_maj = ["F#", "C#", "Gb", "Cb"]
    notallowed_min = ["Eb", "Ab", "Gb", "Db"]
    notallowed_dim = ["F", "Bb", "Eb", "Ab", "Db", "Gb"]

    # any weird chord (e.g. B#) gets converted into its nicer counterpart
    werid_to_normal = {"E#":"F", "B#":"C", "Cb":"B", "Fb":"E", "G#":"Ab", "D#":"Eb", "A#":"Bb"}
    start, end = chord.split(":")
    start = werid_to_normal[start] if start in werid_to_normal.keys() else start

    final_start = start # to begin with 

    # so repetitive, sigh
    if "min" in end:
        if start in notallowed_min: 
            # chord not a proper minor chord - so change needed
            final_start = "A" # for NOW...

            # check if allowed in maj
            for c in allowed_maj:
                if start == c:
                    final_start = c
                    end = "maj"

    elif "dim" in end:
        if start in notallowed_dim:
            final_start = "B"
            # check if allowed in maj
            for c in allowed_maj:
                if start == c:
                    final_start = c
                    end = "maj"

    else:
        if start in notallowed_maj:
            # note: sus chords are considered as maj chords for this purpose
            final_start = "C"
            end = "sus" if "sus" in end else "maj"
            # check if allowed in min
            for c in allowed_min:
                if start == c:
                    final_start = c
                    end = "min"

    return final_start + ":" + end  # phew 


def randomize(tchord):
    ''' randomizes ending if maj/minor chord 50% of the time'''

    # return tchord
    start, end = tchord.split(":")
    if end == "maj" and random.random() < 0.6:
        return start + ":" + random.choices(["maj7", "sus2", "sus4"], weights=[40, 30, 30])[0]
    if end == "min" and random.random() < 0.6:
        return start + ":" + random.choices(["min7"])[0]  

    return start + ":" + end  
   
