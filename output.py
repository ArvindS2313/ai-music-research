import pretty_midi

def output(chords, melodies, tempo):
    midi = pretty_midi.PrettyMIDI(initial_tempo=tempo,)
    piano = pretty_midi.Instrument(program=1)   # for chords
    flute = pretty_midi.Instrument(program=73) # for melody 
    guitar = pretty_midi.Instrument(program=30) # for solo 
    chord_fades = []
    
    # Populate the piano chords
    time = 0
    for ch in chords:
        notes = [str(n) for n in ch['chord'].notes]
        notes = [pretty_midi.note_name_to_number(n) for n in notes]
        rhythm = ch['rhythm']

        # convert rhythm beats into seconds
        num_secs = beats_to_sec(rhythm, tempo)
        for num in notes:
            n = pretty_midi.Note(velocity=125, pitch=num, start=time, 
                                 end=time+num_secs)
            piano.notes.append(n)
        time += num_secs

        if ch['fade']:
            chord_fades.append({'notes':notes, 'num_secs': num_secs})


    # Populate the flute and guitar melody 
    time = 0
    for note in melodies:
        num = 0 if str(note['note']) == 'r' else pretty_midi.note_name_to_number \
            (str(note['note']))
        num_secs = beats_to_sec(note['rhythm'], tempo)

        if num != 0:
            n = pretty_midi.Note(velocity=105, pitch=num, start=time, end=time+num_secs)
            if note['solo']:
                guitar.notes.append(n)
            else:
                flute.notes.append(n)
        time += num_secs    


    # Perform the necessary fade outs
    vol = 100
    while vol > 0:
        for ch in chord_fades:
            for num in ch['notes']:
                n = pretty_midi.Note(velocity=vol, pitch=num, start=time, 
                                    end=time+ch['num_secs'])
                piano.notes.append(n)
            time += ch['num_secs']
        vol -= 25

        
    midi.instruments.append(piano)
    midi.instruments.append(flute)
    midi.instruments.append(guitar)
    midi.write('music/w-fade-out-complex-rhythm-distorted.midi')


def beats_to_sec(num, tempo):
    return num / (tempo/60)



