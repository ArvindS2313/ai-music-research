from agents import * 


print("------------- PREFERENCES -------------")
print("AI will try its best to adhere to preferences, but it may not.")
print("Conflicting preferences may not all be followed through by AI.")
print("You'll be informed if the AI couldn't follow through with your prefernces.\n\n")

params = {
    "s_complexity": int(input("Song Structure Complexity:  ")),
    "length": int(input("Length:  ")),
    "chord_complexity": int(input("Chord Complexity:  ")),
    "variety": int(input("Variety:  ")),
    "sound": int(input("Consonance/Dissonance:  ")),
    "accidentals": int(input("Accidentals (range of 1-5):  ")),
    "common_chords": input("List Common Chords:  ").split(),
    "range": (input("Highest Note:  "), input("Lowest Note  ")),
    "modulation": input("List key changes:  ").split(),
    "key": input("Enter key:  "),
    "tempo_range": (int(input("Minimum tempo")), int(input("Maximum Tempo"))),
}

def assign_agent(params):
    pass