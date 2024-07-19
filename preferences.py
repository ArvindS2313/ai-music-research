from agents import * 
import argparse
import output
from pprint import *

parser = argparse.ArgumentParser(
    prog='preferences.py',
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
# parser.add_argument("-a", "--accidentals", type=int,
#                     help="A numerical rating, on a scale from 1 to 5, of the number of accidental "
#                     "chords. An accidental chord is one that is not in the key of the song.")
# parser.add_argument("-cch", "--common-chords", type=str, 
#                     help="A list of the most common chords that should appear in the song.")
# parser.add_argument("-rh", "--range-high", type=str,
#                     help="The highest piano note that should occur (e.g., C7, A5)")
# parser.add_argument("-rl", "--range-low", type=str,
#                     help="The lowest piano note that should occur (e.g., C3, A2)")
# parser.add_argument("-mod", "--modulation", type=str, 
#                     help="The list of keys that the song should modulate (change keys) to");
# parser.add_argument("-k", "--key", type=str,
#                     help="The key, or the chord center of the song. Keys must be part of the 12"
#                     "well-known ones (excluding Gb major, Cb major, and C# major). Major or minor "
#                     "keys are supported, though theoretical (double sharp/flat) keys are not.")
parser.add_argument("-min", "--min-tempo", type=int)
parser.add_argument("-max", "--max-tempo", type=int)
args = parser.parse_args()
params = vars(args)

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

print("The AI will generate music at least partially in-line with your musical preferences")
print("If you wish to train either the Tranformer AND/OR the MLP, you can do so.")
print("All outputted MIDI files will appear in the music folder.")
agent = assign_agent(params)
agent.generate_chords()
agent.generate_melody()

# OUTPUT DATA FOR EMAIL
print(agent.structs_str)
print("\n\n")
for s in agent.structs.keys():
    print(f"STRUCT: {s}")
    struct = agent.structs[s]
    print(f"ORDER for {s}:   {struct.order}")
    pprint(struct.ms)
    print()
    pprint(struct.melody)
    print()
    print()


all_chords = []
all_melodies = []
for s in agent.structs_str:
    struct = agent.structs[s]
    # loop through all measures in the given struct
    for m in struct.order:
        m_struct = struct.ms[m]
        for i in range(len(m_struct['chords'])):
            all_chords.append({'chord':m_struct['chords'][i], 'rhythm':m_struct['rhythm'][i],
                              'fade': str(struct)=='O'})

    for m in struct.melody:
        for i in range(len(m['notes'])):
            all_melodies.append({'note':m['notes'][i], 'rhythm':m['rhythm'][i], 
                                 'solo': m['solo'], 'fade': str(struct)=='O'})


tempo = random.randint(params['min_tempo'], params['max_tempo'])
output.output(all_chords, all_melodies, tempo)