import random
from structure import Structure
from chord import Chord
import generate
from pprint import pprint

class Agent:
    # boilerplate class
    def __init__(self) -> None:
        self.structs_str: list = []     # Strings 
        self.structs: list = []         # Structure class
        self.params = {}
        # The rest of the stuff depends on the agent.
    
    def form_structures(self):
        conv = {"I": "intro", "V":"verse", "C": "chorus", "O":"outro", "B":"bridge"
                , "S": "solo", "IL": "interlude"}
        self.structs = [Structure(name=conv[x], params=self.params) for x in self.structs_str]
    
    def generate(self):
        assert self.params != {}

        self.gen_chords = generate.mlp_gen(context=generate.context2, block_size=len(generate.context2),
                                       num_tokens=500, type="time", kind="00")
        self.gen_chords = [Chord(c) for c in self.gen_chords[len(generate.context1):]]  # convert to Chord objects; don't feed input chords
        
        print(self.gen_chords)
        print()
        print()
        print()

        # apply chord generation for each song structure 
        prev = []
        start = 0
        for s in range(len(self.structs)):
            struct = self.structs[s]
            print("Struct  ", struct)
            context = self.gen_chords[start:start+4+struct.num_components]
            print("Context for this structure:")
            print(context)
            main = context[:4]             # four main chords which are the first measure
            print("Main Context (first measure) of structure:")
            print(main)
            variations = context[4:]       # chords used as variations

            main = self.customize(prev=prev, curr=main)    # customize main chords based on previous main chords
            print("Main Context Changed:")
            print(main)
            context = main[:] + variations[:]
            struct.generate(chords=context)

            prev = main[:]
            start += 4+struct.num_components
            print("\n\n\n")
                        

    def customize(self, prev, curr):
        '''
        Customizes an array of chords to make it more unique from the previous
        chords, if necessary.
        '''
        assert self.params != {}

        same_chords = set([c.name for c in prev]) & set([c.name for c in curr])
        print("Same chords from previous context:")
        print(same_chords)
        if len(same_chords) == 2:
            # two similar chords, modify ending
            for c in range(len(curr)):
                chord = curr[c]
                if self.params['accidentals'] >= 3:
                    chord.change_maj_min()
                else:
                    chord.add_rem7()

        elif len(same_chords) > 2:
            # 3 or 4 similar chords, perform a transposition
            for c in range(len(curr)):
                chord = curr[c]
                key = self.params['modulation'][0] if self.params['modulation'] else 'D'
                chord.transpose(key)

        return curr


class ShortSimple(Agent):
    ''' Short length, simple structures, no changes'''
    def __init__(self, params) -> None:
        super().__init__()
        self.poss_structs = [
            ["I", "V", "C", "V", "C", "O"],
            ["I", "V", "C", "V", "O"],
        ]
        self.structs_str = random.choice(self.poss_structs)
        self.params = params
        self.form_structures()


class ShortComplex(Agent):
    ''' Short length, more complex structures, no changes'''
    def __init__(self, params) -> None:
        super().__init__()
        self.poss_structs = [
            ["I", "V", "C", "V", "C", "O"],
            ["I", "V", "V", "C", "B", "C", "O"],
            ["I", "V", "C", "V", "S", "V", "O"],
            ["I", "V", "C", "V", "B", "C", "O"],
        ]
        self.structs_str = random.choice(self.poss_structs)
        self.params = params
        self.form_structures()


class MediumSimplistic(Agent):
    '''Medium length, simple structures, few changes'''
    def __init__(self, params) -> None:
        super().__init__()
        self.poss_structs = [
            ["I", "V", "C", "V", "C", "V", "C", "O"],
            ["I", "V", "V", "C", "B", "V", "V" "C", "O"],
            ["I", "V", "C", "V", "IL", "C", "V", "O"],
            ["I", "V", "C", "V", "B", "V", "C", "O"],
        ]
        self.structs_str = random.choice(self.poss_structs)
        self.params = params
        self.form_structures()


class MediumComplex(Agent):
    '''Medium length, complex structures, some changes'''
    def __init__(self, params) -> None:
        super().__init__()
        self.poss_structs = [
            ["I", "V", "C", "B", "V", "C", "S", "C", "O"],
            ["I", "V", "C", "IL", "V", "C", "S", "C", "O"],
            ["I", "V", "V", "C", "IL", "V", "S", "C", "O"],
            ["I", "V", "C", "B", "V", "S", "C", "V", "C", "O"],
        ]
        self.structs_str = random.choice(self.poss_structs)
        self.params = params
        self.form_structures()


class LongSimplistic(Agent):
    '''Long length, somewhat simplistic structures, some changes'''
    def __init__(self, params) -> None:
        super().__init__()
        self.poss_structs = [
            ["I", "V", "C", "V", "C", "B", "V", "C", "V", "C", "O"],
            ["I", "V", "C", "B", "V", "C", "V", "S", "V", "C", "O"],
            ["I", "V", "V", "C", "V", "B", "V", "C", "S", "C", "O"]
        ]
        self.structs_str = random.choice(self.poss_structs)
        self.params = params
        self.form_structures()


class LongComplex(Agent):
    ''' Long length, complex structures, multiple changes'''
    def __init__(self, params) -> None:
        super().__init__()
        self.structures = [
            ["I", "V", "C", "V", "B", "S", "V", "C", "IL", "V", "C", "O"],
            ["I", "V", "C", "V", "C", "S", "V", "B", "V", "S", "C", "O"],
            ["I", "V", "V", "C", "B", "V", "C", "S", "C", "IL", "C", "O"]
        ]
        self.structs_str = random.choice(self.structures)
        self.params = params
        self.form_structures()
