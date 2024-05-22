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
time = 0
duration = 1
tempo = 140
volume = 100

# helper method: convert note to MIDI number
def convert(note, octave):
    if "bb" in note:
        note = note.replace("bb", "")
        return (Chord.NOTES[note] - 2) + 12 * (octave + 1)
    if "##" in note:
        note = note.replace("##", "")
        return (Chord.NOTES[note] + 2) + 12 * (octave + 1)
    return Chord.NOTES[note] + 12 * (octave + 1)


def output(chords: list):
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track, time, tempo)

    counter = 0
    for ch in chords:
        name = ch.name.replace(":", "")
        try:
            notes = c.from_shorthand(name)
        except FormatError:
            print(ch.name + " had a formatting error")
            notes = ["C", "E", "G"]     # C major chord

        for n in notes:
            num = convert(n, octave)
            MyMIDI.addNote(track, channel, num, time+counter, duration, volume)
        
        counter += 1

    with open(f"song-3", "wb") as f:
        MyMIDI.writeFile(f)
        print("File has been outputted.")



