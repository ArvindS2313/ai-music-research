'''
A class declaration for a chord object. 
'''

class Chord:

    def __init__(self, name):
        ''' Precondition: name is in format 'root':'type' '''

        # WARNING: assert does not check if the root and type of the chords are valid
        assert ":" in name and name.index(":") > 0 

        self.name = name 
        self._root = name.split(":")[0]
        self._type = name.split(":")[1] if Chord.is_proper(name.split(":")[1]) else 'maj'

    @staticmethod
    def is_proper(type):
        return type in {"maj", "min", "dim", "aug", "sus4", "sus2", "maj7", 
                        "7", "min7", "min7b5", "dim7", "add9"}
    
    def transpose(self, key):
        '''
        Algorithm:
        1) Determine distance from C major to desired key
        2) Travel that distance to determine the chord in the opposite direction in the order list
        3) If we travel too far left, then index into the list and sharp the result
        4) If we travel too far right, normalize the result (mod 7), index into list, and flat the result
        5) Endings do not change. 
        '''

        lookup = {"Db": -5, "Ab": -4, "Eb": -3, "Bb": -2, "F": -1, "C": 0, 
                  "G": 1, "D": 2, "A": 3, "E": 4, "B": 5, "F#":6}
        order = ["B", "E", "A", "D", "G", "C", "F"]

        travel = -(lookup[key] - lookup['C'])
        destination = order.index(self._root[0]) + travel

        if destination < 0:
            if len(self._root) == 1:
                self._root = order[destination] + "#"
            if self._root[1] == "b":
                self._root = order[destination]
        elif destination >= len(order):
            destination %= 7
            if len(self._root) == 1:
                self._root = order[destination] + "b"
            if self._root[1] == "#":
                self._root = order[destination]
        else:
            if len(self._root) == 1:
                self._root = order[destination]
            else:
                self._root = order[destination] + self._root[1]

        self.name = self._root + ":" + self._type
        
    def change_maj_min(self):
        if self._type == "maj" or self._type == "maj7":
            self._type = self._type.replace("maj", "min")
        elif self._type == "min" or self._type == "min7":
            self._type = self._type.replace("min", "maj")
        elif self._type == "dim":
            self._type = "aug"
        elif self._type == "aug":
            self._type = "dim"
        elif self._type == "sus" or self._type == "sus4":
            self._type = "sus2"
        elif self._type == "sus2":
            self._type = "sus4"
        self.name = self._root + ":" + self._type

    def add_rem7(self):
        if self._type == "min" or self._type == "maj":
            self._type += "7"
        elif self._type == "min7":
            self._type = "min"
        elif self._type == "maj7":
            self._type = "maj"
        self.name = self._root + ":" + self._type

    def accidentalize(self, direction):
        pass

    def __repr__(self):
        return self.name
    