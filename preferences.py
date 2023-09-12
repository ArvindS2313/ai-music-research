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
    "tempo_range": (int(input("Min tempo  ")), int(input("Max Tempo  "))),
}

def assign_agent(params):
    if params["length"] == 1 or params["length"] == 2:
        if params["s_complexity"] <= 3:
            agent = ShortSimple(params)
        else:
            agent = ShortComplex(params)
    elif params["length"] == 3:
        if params["s_complexity"] < 3:
            # this time < 3, but <= 3
            agent = MediumSimplistic(params)
        else:
            agent = MediumComplex(params) 
    else:
        if params["s_complexity"] < 3:
            # this time < 3, but <= 3
            agent = LongSimplistic(params)
        else:
            agent = LongComplex(params) 
    
    return agent

agent = assign_agent(params)
print(agent.__class__.__name__)
print(agent.structs)
a = agent.structs[0]
print("SETTINGS FOR INTRO\n")
print(f"Length of structure components: {a.len}")
print(f"Number of UNIQUE components: {a.num_components}")
print(f"Number of accidentals (not taken to account): {a.num_acc}")
print(a.cs)
print()