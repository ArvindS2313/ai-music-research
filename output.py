import pretty_midi

def output(chords, melodies, tempo):
    midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    piano = pretty_midi.Instrument(program=1)   # for chords
    violin = pretty_midi.Instrument(program=41) # for melody
    
    # Populate the piano chords
    time = 0
    for ch in chords:
        notes = [str(n) for n in ch['chord'].notes]
        notes = [pretty_midi.note_name_to_number(n) for n in notes]
        rhythm = ch['rhythm']

        # convert rhythm beats into seconds
        num_secs = beats_to_sec(rhythm, tempo)
        for num in notes:
            n = pretty_midi.Note(velocity=100, pitch=num, start=time, 
                                 end=time+num_secs)
            piano.notes.append(n)
        time += num_secs

    # Populate the violin melody 
    time = 0
    for note in melodies:
        num = 0 if str(note['note']) == 'r' else pretty_midi.note_name_to_number \
            (str(note['note']))
        num_secs = beats_to_sec(note['rhythm'], tempo)

        if num != 0:
            n = pretty_midi.Note(velocity=100, pitch=num, start=time, end=time+num_secs)
            violin.notes.append(n)
        time += num_secs    
        
    midi.instruments.append(piano)
    midi.instruments.append(violin)
    midi.write('music/ug-with-violin-melody.midi')


def beats_to_sec(num, tempo):
    return num / (tempo/60)



