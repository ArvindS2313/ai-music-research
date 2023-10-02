from ugdata import songs

CHARTS = {
    "C": ["C", "Dm", "Em", "F", "G", "Am", "Bdim"],
    "G": ["G", "Am", "Bm", "C", "D", "Em", "F#dim"],
    "D": ["D", "Em", "F#m", "G", "A", "Bm", "C#dim"],
    "A": ["A", "Bm", "C#m", "D", "E", "F#m", "G#dim"],
    "E": ["E", "F#m", "G#m", "A", "B", "C#m", "D#dim"],
    "B": ["B", "C#m", "D#m", "E", "F#", "G#m", "A#dim"],
    "F#": ["F#", "G#m", "A#m", "B", "C#", "D#m", "E#dim"],
    "C#": ["C#", "D#m", "E#m", "F#", "G#", "A#m", "B#dim"],
    "F": ["F", "Gm", "Am", "Bb", "C", "Dm", "Edim"],
    "Bb": ["Bb", "Cm", "Dm", "Eb", "F", "Gm", "Adim"],
    "Eb": ["Eb", "Fm", "Gm", "Ab", "Bb", "Cm", "Ddim"],
    "Ab": ["Ab", "Bbm", "Cm", "Db", "Eb", "Fm", "Gdim"],
    "Db": ["Db", "Ebm", "Fm", "Gb", "Ab", "Bbm", "Cdim"],
    "Gb": ["Gb", "Abm", "Bbm", "Cb", "Db", "Ebm", "Fdim"],
    "Cb": ["Cb", "Dbm", "Ebm", "Fb", "Gb", "Abm", "Bbdim"],
}

def process(band):
    band_songs = [s[5].split(",") for s in songs if s[2] == band]
    print(band_songs)
    
    # determine key of song
    for s in band_songs:
        table = {
            "C": 0,
            "G": 0,
            "D": 0,
            "A": 0,
            "E": 0,
            "B": 0,
            "F#": 0,
            "C#": 0,
            "F": 0,
            "Bb": 0,
            "Eb": 0,
            "Ab": 0,
            "Db": 0,
            "Gb": 0,
            "Cb": 0,
        }

process("The Beatles")