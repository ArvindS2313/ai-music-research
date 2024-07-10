from structure import *
import generate

class Agent:
    # boilerplate class
    def __init__(self, params) -> None:
        self.params = params
        self.conv = {"I": "intro", "V":"verse", "C": "chorus", "O":"outro", 
                     "B":"bridge", "S": "solo", "IL": "interlude"}

        # Define parameters which will hold the song structures
        self.structs_str = []
        self.structs = {} 

    def generate_chords(self):
        '''
        Populates the song with a set of chords
        '''
        assert self.params != {}

        # CAUTION: struct objects are reference types! change with caution!
        for s in self.structs_str:
            if s not in self.structs.keys():
                new_struct = Structure(name=s, params=self.params)
                new_struct.generate_chords()
                new_struct.clean_chords()
                self.structs[s] = new_struct

    def generate_melody(self):
        assert self.structs != {}, "Melody generation must come after chord generation"

        # for now, the melody will simply be quarter notes
        for s in self.structs.keys():
            self.structs[s].generate_melody()



class ShortSimple(Agent):
    ''' Short length, simple structures, no changes'''
    def __init__(self, params) -> None:
        super().__init__(params)
        self.poss_structs = [
            ["I", "V", "C", "V", "C", "O"],
            ["I", "V", "C", "V", "O"],
        ]
        self.structs_str = random.choice(self.poss_structs)


class ShortComplex(Agent):
    ''' Short length, more complex structures, no changes'''
    def __init__(self, params) -> None:
        super().__init__(params)
        self.poss_structs = [
            ["I", "V", "C", "V", "C", "O"],
            ["I", "V", "C", "B", "C", "O"],
            ["I", "V", "C", "V", "S", "O"],
            ["I", "V", "C", "B", "V", "O"],
        ]
        self.structs_str = random.choice(self.poss_structs)


class MediumSimplistic(Agent):
    '''Medium length, simple structures, few changes'''
    def __init__(self, params) -> None:
        super().__init__(params)
        self.poss_structs = [
            ["I", "V", "C", "V", "C", "V", "C", "O"],
            ["I", "V", "C", "V", "B", "V", "V", "C", "O"],
            ["I", "V", "C", "V", "B", "V", "C", "O"],
        ]
        self.structs_str = random.choice(self.poss_structs)


class MediumComplex(Agent):
    '''Medium length, complex structures, some changes'''
    def __init__(self, params) -> None:
        super().__init__(params)
        self.poss_structs = [
            ["I", "V", "C", "B", "V", "C", "S", "C", "O"],
            ["I", "V", "C", "IL", "V", "C", "S", "C", "O"],
            ["I", "V", "C", "IL", "V", "S", "C", "O"],
            ["I", "V", "C", "B", "V", "S", "C", "V", "C", "O"],
        ]
        self.structs_str = random.choice(self.poss_structs)


class LongSimplistic(Agent):
    '''Long length, somewhat simplistic structures, some changes'''
    def __init__(self, params) -> None:
        super().__init__(params)
        self.poss_structs = [
            ["I", "V", "C", "V", "C", "B", "V", "C", "V", "C", "O"],
            ["I", "V", "C", "B", "V", "C", "V", "S", "V", "C", "O"],
            ["I", "V", "V", "C", "V", "B", "V", "C", "S", "C", "O"]
        ]
        self.structs_str = random.choice(self.poss_structs)


class LongComplex(Agent):
    ''' Long length, complex structures, multiple changes'''
    def __init__(self, params) -> None:
        super().__init__(params)
        self.structures = [
            ["I", "V", "C", "V", "B", "S", "V", "C", "IL", "V", "C", "O"],
            ["I", "V", "C", "S", "V", "S", "C", "B", "V", "S", "C", "O"],
            ["I", "V", "V", "C", "B", "V", "C", "S", "C", "IL", "C", "O"]
        ]
        self.structs_str = random.choice(self.structures)
