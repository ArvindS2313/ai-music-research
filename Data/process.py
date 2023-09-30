from ugdata import songs

def process(band):
    band_songs = [s[5].split(",") for s in songs if s[2] == band]
    return band_songs

print(process("The Beatles"))