from agents import * 
import argparse
import output

print("\n------------- PREFERENCES -------------")
print("AI will try its best to adhere to preferences, but it may not.")
print("Conflicting preferences may not all be followed through by AI.")
print("You'll be informed if the AI couldn't follow through with your prefernces.\n\n")

parser = argparse.ArgumentParser(
    prog='preferences.py',
    description = "User preferences which will dictate the type of neural networks used"
    ", the song/measure structures, and the planning editing components."
)

# arguments 
parser.add_argument("-sc", "--song-complexity", type=int,
                    help="A numerical rating, on a scale from 1 to 5, of the complexity of the " 
                    "overall song structure (e.g. I, V, C, V, B, C, O)")
parser.add_argument("-l", "--song-length", type=int,
                    help="A numerical rating, on a scale from 1 to 5, of the length of the song; "
                    "smaller ratings correlate to a shorter song.")
parser.add_argument("-cc", "--chord-complexity", type=int, 
                    help="A numerical rating, on a scale from 1 to 5, of the complexity of the "
                    "chords of the song; higher rating means more complex chords")
parser.add_argument("-v", "--variety", type=int,
                    help="A numerical rating, on a scale from 1 to 5, describing how repeated "
                    "the chords should be; a lower rating means chords should be fairly repetitive")
parser.add_argument("-s", "--sound", type=int, 
                    help="A numerical rating, on a scale from 1 to 5, on whether the chords should "
                    "be very consonant (sounds pleasant, 'nice' intervals) or very dissonant "
                    "(sounds sharp, dark); lower ratings means more consonant.")
parser.add_argument("-a", "--accidentals", type=int,
                    help="A numerical rating, on a scale from 1 to 5, of the number of accidental "
                    "chords. An accidental chord is one that is not in the key of the song.")
parser.add_argument("-cch", "--common-chords", type=str, 
                    help="A list of the most common chords that should appear in the song.")
parser.add_argument("-rh", "--range-high", type=str,
                    help="The highest piano note that should occur (e.g., C7, A5)")
parser.add_argument("-rl", "--range-low", type=str,
                    help="The lowest piano note that should occur (e.g., C3, A2)")
parser.add_argument("-mod", "--modulation", type=str, 
                    help="The list of keys that the song should modulate (change keys) to");
parser.add_argument("-k", "--key", type=str,
                    help="The key, or the chord center of the song. Keys must be part of the 12"
                    "well-known ones (excluding Gb major, Cb major, and C# major). Major or minor "
                    "keys are supported, though theoretical (double sharp/flat) keys are not.")
parser.add_argument("-min", "--min-tempo", type=int)
parser.add_argument("-max", "--max-tempo", type=int)
args = parser.parse_args()
params = vars(args)

def assign_agent(params):
    if params["song_length"] == 1 or params["song_length"] == 2:
        if params["song_complexity"] <= 3:
            agent = ShortSimple(params)
        else:
            agent = ShortComplex(params)
    elif params["song_length"] == 3:
        if params["song_complexity"] < 3:
            # this time < 3, but <= 3
            agent = MediumSimplistic(params)
        else:
            agent = MediumComplex(params) 
    else:
        if params["song_complexity"] < 3:
            # this time < 3, but <= 3
            agent = LongSimplistic(params)
        else:
            agent = LongComplex(params) 
    
    return agent

ls = assign_agent(params)
ls.generate()

full_chords = []
for s in ls.structs:
    full_chords.extend(s.chords)

print(full_chords)
output.output(full_chords)