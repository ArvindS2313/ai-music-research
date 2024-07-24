class Note:
    '''
    A class declaration for a note object. Note objects are like chords,
    but quite simpler. 
    '''

    NOTES = {"B#": 0, "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
         "E": 4, "Fb": 4, "E#": 5, "F": 5, "F#": 6, "Gb": 6, "G": 7,
         "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11, "Cb": 11}

    def __init__(self, name, octave):
        ''' Precondition: name is in format 'root':'type' '''
 
        # WARNING: assert does not check if the root and type of the chords are valid
        assert name in Note.NOTES.keys() 

        self.name = name 
        self.octave = int(octave)
        assert 9 > self.octave > 1, "Outside octave range"
        self.key = "C"
    
    def transpose(self, key):
        '''
        Algorithm:
        1) Determine distance from C major to desired key
        2) Travel that distance to determine the chord in the opposite direction in the order list
        3) If we travel too far left, then index into the list and sharp the result
        4) If we travel too far right, normalize the result (mod 7), index into list, and flat the result
        '''

        lookup = {"Db": -5, "Ab": -4, "Eb": -3, "Bb": -2, "F": -1, "C": 0, 
                  "G": 1, "D": 2, "A": 3, "E": 4, "B": 5, "F#":6}
        order = ["B", "E", "A", "D", "G", "C", "F"]

        travel = -(lookup[key] - lookup[self.key])
        destination = order.index(self.name[0]) + travel

        if destination < 0:
            if len(self.name) == 1:
                self.name = order[destination] + "#"
            if self.name[1] == "b":
                self.name = order[destination]
        elif destination >= len(order):
            destination %= 7
            if len(self.name) == 1:
                self.name = order[destination] + "b"
            if self.name[1] == "#":
                self.name = order[destination]
        else:
            if len(self.name) == 1:
                self.name = order[destination]
            else:
                self.name = order[destination] + self.name[1]

        self.key = key


    def change_octave(self, by_how_much, up_or_down):
        if up_or_down == 'down' and self.octave - by_how_much > 0:
            self.octave -= by_how_much
        if up_or_down == 'up' and self.octave + by_how_much < 8:
            self.octave += by_how_much            

    def __repr__(self):
        return f"{self.name}{self.octave}"