import argparse
import pretty_midi
from agents import * 
from pprint import *

# ---------------------------- OBTAIN USER INPUT --------------------------- #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='main.py',
        description = "User preferences which will dictate the type of neural networks used"
        ", the song/measure structures, and the planning editing components."
    )

    # arguments 
    parser.add_argument("-sc", "--song-complexity", type=int,
                        help="A numerical rating, on a scale from 1 to 5, of how many complex song " 
                        "structures should be in the song. More complex songs might involve elements"
                        "like interludes or solos, while less complex sounds like mainly verses/choruses")
    parser.add_argument("-l", "--song-length", type=int,
                        help="A numerical rating, on a scale from 1 to 5, regarding number of song"
                        "structures AND length of measures")
    parser.add_argument("-cc", "--chord-complexity", type=int, 
                        help="A numerical rating, on a scale from 1 to 5, of the complexity of the "
                        "chords of the song; higher rating means more complex chords")
    parser.add_argument("-rc", "--rhythm-complexity", type=int, 
                        help="A numerical rating, on a scale from 1 to 3, of the complexity of the "
                        "rhythm/beats of the song; higher rating means more complex rhythms or"
                        "syncopation")
    parser.add_argument("-mc", "--measure-complexity", type=int, 
                        help="A numerical rating, on a scale from 1 to 3, of the complexity of the "
                        "measure structure parts; higher ratings mean more distinct measures in a "
                        "song structure")  
    parser.add_argument("-ss", "--step-size", type=int, 
                        help="A numerical rating, on a scale from 1 to 3, of the general step size "
                        "between two melody notes. Even with a step size of 3, most of the notes, "
                        "in order to ensure listenability, will have a step size of 1.")
    # parser.add_argument("-s", "--sound", type=int, 
    #                     help="A numerical rating, on a scale from 1 to 5, on whether the chords should "
    #                     "be very consonant (sounds pleasant, 'nice' intervals) or very dissonant "
    #                     "(sounds sharp, dark); lower ratings means more consonant.")
    parser.add_argument("-a", "--accidentals", type=int,
                        help="A numerical rating, on a scale from 1 to 5, of the number of accidental "
                        "chords. An accidental chord is one that is not in the key of the song.")
    # parser.add_argument("-cch", "--common-chords", type=str, 
    #                     help="A list of the most common chords that should appear in the song.")
    # parser.add_argument("-mod", "--modulation", type=str, 
    #                     help="The list of keys that the song should modulate (change keys) to");
    parser.add_argument("-k", "--key", type=str,
                        help="The key, or the chord center of the song. Keys must be part of the 12"
                        "well-known ones (excluding Gb major, Cb major, and C# major). Major keys"
                        "are supported, though minor or theoretical (double sharp/flat) keys are not.")
    parser.add_argument("-min", "--min-tempo", type=int)
    parser.add_argument("-max", "--max-tempo", type=int)
    args = parser.parse_args()
    params = vars(args)


### -------------------------------- POPULATE DATA -------------------------------- ###
def assign_agent(params):
    if params["song_length"] <= 2:
        if params["song_complexity"] <= 3:
            agent = ShortSimple(params)
        else:
            agent = ShortComplex(params)
    elif params["song_length"] == 3:
        if params["song_complexity"] <= 2:
            agent = MediumSimplistic(params)
        else:
            agent = MediumComplex(params) 
    else:
        if params["song_complexity"] <= 2:
            agent = LongSimplistic(params)
        else:
            agent = LongComplex(params) 
    
    return agent


def populate(agent):
    agent.generate_chords()
    print("The chords have been generated for the entire song.")
    agent.generate_melody()
    print("The melody has been generated for the entire song.")
    agent.generate_bass()
    print("The bass line has been generated for the entire song.")
    # agent.transpose()
    # print("The song has been transposed to the desired key.")


#### ----------------------------- OUTPUT MIDI & PRINT DATA ----------------------------- ###
def printout(agent):
    print(agent.structs_str)
    print("\n\n")
    for s in agent.structs.keys():
        print(f"STRUCT: {s}")
        struct = agent.structs[s]
        print(f"ORDER for {s}:   {struct.order}")
        pprint(struct.ms)
        print()
        pprint(struct.melody)
        print("\n")
        pprint(struct.bass)
        print("\n")


def output(file_name, agent, tempo):
    midi = pretty_midi.PrettyMIDI(initial_tempo=tempo,)
    piano = pretty_midi.Instrument(program=1)   # for chords
    mel_num = pretty_midi.instrument_name_to_program("flute")
    mel_inst = pretty_midi.Instrument(program=mel_num) # for melody 

    solo_num = pretty_midi.instrument_name_to_program("harpsichord")
    solo_inst = pretty_midi.Instrument(program=solo_num) # for solo 

    bass = pretty_midi.Instrument(program=33) # for pizz double bass 

    chord_fades = []
    solo_fades = []

    ch_time = 0
    mel_time = 0
    bass_time = 0

    for s in agent.structs_str:
        struct = agent.structs[s]
        if str(struct) == "OS":
            os_inst = solo_inst if random.random() < 0.5 else mel_inst

        # Populate the piano chords
        for m in struct.order:
            rhythm, chords = struct.ms[m]['rhythm'], struct.ms[m]['chords']

            # Go through each chord and add it to the piano
            for c in range(len(chords)):
                r, notes = rhythm[c], chords[c].notes
                notes = [pretty_midi.note_name_to_number(str(n)) for n in notes]
                num_secs = beats_to_sec(r, tempo)

                for num in notes:
                    n = pretty_midi.Note(velocity=125, pitch=num, start=ch_time, 
                                        end=ch_time+num_secs)
                    piano.notes.append(n)

                # Chord/solo fade if outro
                if str(struct) == "O" or str(struct) == "OS":
                    chord_fades.append({'notes':notes, 'secs':num_secs})

                ch_time += num_secs


        # Populate the melody and solo
        for m in struct.melody:
            rhythm, notes = m['rhythm'], m['notes']
            # Go through each chord and add it to the piano
            for c in range(len(notes)):
                r, n = rhythm[c], notes[c]
                # convert rhythm beats into seconds
                num_secs = beats_to_sec(r, tempo)
                num = 0 if str(n) == 'r' else pretty_midi.note_name_to_number(str(n))
                n = pretty_midi.Note(velocity=125, pitch=num, start=mel_time, 
                                        end=mel_time+num_secs)
                
                if str(struct) == "S":
                    solo_inst.notes.append(n)
                elif str(struct) == "OS":
                    os_inst.notes.append(n)
                else:
                    mel_inst.notes.append(n)

                # Chord/solo fade if outro
                if str(struct) == "O" or str(struct) == "OS":
                    solo_fades.append({'note':num, 'secs':num_secs})

                mel_time += num_secs


        # Populate the bass line
        for m in struct.bass:
            rhythm, notes = m['rhythm'], m['notes']

            # Go through each note and add it to the bass
            for c in range(len(notes)):
                r, n = rhythm[c], notes[c]
                # convert rhythm beats into seconds
                num_secs = beats_to_sec(r, tempo)
                num = 0 if str(n) == 'r' else pretty_midi.note_name_to_number(str(n))
                n = pretty_midi.Note(velocity=125, pitch=num, start=bass_time, 
                                        end=bass_time+num_secs)
                
                bass.notes.append(n)
                bass_time += num_secs


    assert round(ch_time) == round(mel_time)
    t1, t2 = ch_time, ch_time

    # Perform fade outs for outros and outro solos
    vol = 100
    while vol > 0:
        # Chord fade outs
        for ch in chord_fades:
            for num in ch['notes']:
                n = pretty_midi.Note(velocity=vol, pitch=num, start=t1, 
                                    end=t1+ch['secs'])
                piano.notes.append(n)
            t1 += ch['secs']

        # Solo fade outs
        for note in solo_fades:
            n = pretty_midi.Note(velocity=vol-10, pitch=note['note'], start=t2, 
                                    end=t2+note['secs'])
            solo_inst.notes.append(n)
            t2 += note['secs']

        # IMPORTANT: t2 MUST equal t1!
        assert round(t1) == round(t2), "Solo and chord timings are inacurate!"
        vol -= 25

    midi.instruments.append(piano)
    midi.instruments.append(mel_inst)
    midi.instruments.append(solo_inst)
    midi.instruments.append(bass)
    midi.write(file_name)

def beats_to_sec(num, tempo):
    return num / (tempo/60)


if __name__ == "__main__":
    tempo = random.randint(params['min_tempo'], params['max_tempo'])
    agent = assign_agent(params=params)
    populate(agent)
    output("music/smoothed-song-2" + ".midi", agent, tempo)
    print("The MIDI has been generated and outputted to the music folder.")

