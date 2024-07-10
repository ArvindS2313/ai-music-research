from mingus.core import chords as c 
from mingus.core.mt_exceptions import FormatError
from midiutil import MIDIFile
from chord import Chord

'''
Generates an output MIDI file from a list of chords
'''

# Constant MIDI file information
track = 0
channel = 0
octave = 4
tempo = 140
volume = 100

# helper method: convert note to MIDI number
def convert(notes, octave):
    new = []
    min = 0
    for note in notes:
        if "bb" in note:
            note = note.replace("bb", "")
            val = (Chord.NOTES[note] - 2) + 12 * (octave + 1)
        if "##" in note:
            note = note.replace("##", "")
            val = (Chord.NOTES[note] + 2) + 12 * (octave + 1)
        val = Chord.NOTES[note] + 12 * (octave + 1)
        if val < min: val += 12
        min = val
        new.append(val)
    
    return new


def output(chords: list, tempo:int):
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track, 0, tempo)

    time = 0 
    for ch in chords:
        # the_chords, lol
        chord = ch['chords'].name.replace(":", "")
        dur = ch['rhythms']
        try:
            notes = c.from_shorthand(chord)
        except FormatError:
            notes = ["C", "E", "G"]    # C major chord
        
        notes = convert(notes, octave)
        for n in notes:
            MyMIDI.addNote(track, channel, n, time, dur, volume)
        time += dur


    with open(f"music/ug-song-5.midi", "wb") as f:
        MyMIDI.writeFile(f)
        print("File has been outputted.")


