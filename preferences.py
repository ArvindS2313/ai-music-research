from agents import * 

print("------------- PREFERENCES -------------")

song_complexity = int(input("Song Structure Complexity  "))
length = input("Length  ")
chord_complexity = int(input("Chord Complexity  "))
variety = int(input("Variety  "))
sound = int(input("Consonance & Dissonance  "))
accidentals = int(input("Accidentals  "))
common_chords = input("Common Chords  ").split(" ")
range = input("Highest Note  "), input("Lowest Note  ")
modulaton = input("Modulation  ").split()
key = input("Key  ")
tempo = int(input("Tempo  "))

params = {
    "song_complexity": song_complexity,
    "length": length,
    "chord_complexity": chord_complexity,
    "variety": variety,
    "sound": sound,
    "accidentals": accidentals,
    "common_chords": common_chords,
    "range": range,
    "modulation": modulaton,
    "key": key,
    "tempo": tempo,
}

# Song complexity:
if song_complexity < 3 and length == "short":
    agent = ShortSimpleAgent(params=2)
elif song_complexity < 3 and length == "long":
    agent = SimpleAgent(params)
else:
    agent = LongComplex(params)