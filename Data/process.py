from ugdata import songs


def cleanup(chords):
    ''' Returns cleaned up chords and extra stuff so it can be used later
      to determine the key'''  
    
    cchords = []
    cextras = []

    for chord in chords:
        # get rid of inversions
        if "/" in chord:
            chord = chord[:chord.find('/')]
        chord = chord.replace("maj", "")

        # replace "weird" chords
        chord = chord.replace("D#", "E#")
        chord = chord.replace("A#", "Bb")
        chord = chord.replace("G#", "Ab")
        chord = chord.replace("E#", "F")
        chord = chord.replace("B#", "C")
        chord = chord.replace("Fb", "E")

        # cchord is the cleaned chord
        # cextra is the cleaned extra part 
        # both get returned from the function

        if len(chord) == 1:
            cchord = chord  # one letter chords are already good
            cextra = ""
        elif "m" in chord: 
            if "dim" in chord: 
                # doing this because 'dim' will have 'm' in it
                cchord = chord[:chord.find('dim')]
                cextra = chord[chord.find('dim'):]
            else:
                # it is a minor chord but not a dim chord
                cchord = chord[:chord.find('m')+1]
                cextra = chord[chord.find('m')+1:]
        elif "#" in chord: 
            cchord = chord[:chord.find('#')+1]
            cextra = chord[chord.find('#')+1:]
        elif "b" in chord:
            cchord = chord[:chord.find('b')+1]
            cextra = chord[chord.find('b')+1:]
        else:
            cchord = chord[0]
            cextra = chord[1:]  

        cchords.append(cchord)
        cextras.append(cextra)

    return cchords, cextras

    
def get_key(chords):
    ''' Takes cleaned chords and assumes a key out of them'''

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

    ''' Loop over all chords
    Add to counts which contain keys which contain chord
    Key w max counts is key of chords    
    '''
    counts = [0 for _ in range(len(itok))]
    for c in chords:
        for i in range(len(itok)):
            inkey = CHARTS[itok[i]] # inkey is a list
            if c in inkey:
                counts[i] += 1
    
    # DEBUG ONLY - print out key, count pair
    # for i in range(len(counts)):
    #     print(itok[i], counts[i])

    return itok[counts.index(max(counts))]


def transpose(chords, key):
    ''' transposes chords to key -- only deals with major keys for now'''
    keys = ["Bbb", "Fb", "Cb", "Gb", "Db", "Ab", "Eb", "Bb", "F", "C", "G", "D", 
            "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "E#", "B#"] # list of keys
    final = "C"
    diff = keys.index(final) - keys.index(key) # diff between final & initial key

    tchords = []
    for c in chords:
        if "m" in c:
            # it is a minor chord
            c = c.replace("m", "")
            tc = keys[keys.index(c)+diff] + "m"
        else:
            # get index, add difference, and assign new key
            tc = keys[keys.index(c)+diff]
        tchords.append(tc)

    return tchords
            

def process(band):
    orig_songs = [s[5].split(",") for s in songs if s[2] == band]
    cleaned_songs = []

    for i in range(len(orig_songs)): 
        # Note: song and chords are refering to the same thing
        song = orig_songs[i]
        cchords, extra = cleanup(song)  # cleaned song and cleaned extra part
        key = get_key(cchords) # key of the cleaned chords 

        transposed_no_extra = transpose(cchords, key) # transposed to C major
        transposed_extra = [] # transposed with the extra stuff
        for j in range(len(cchords)):
            final_chord = transposed_no_extra[j] + extra[j]
            transposed_extra.append(final_chord)
        cleaned_songs.append(transposed_extra)
        
    
    return cleaned_songs