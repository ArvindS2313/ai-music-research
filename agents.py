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
        stop = -1

        for s in range(len(self.structs)):
            struct = self.structs[s]
            print("Struct  ", struct)

            stop = start + struct.num_components + 4   # technically one extra
            context = self.gen_chords[start:stop]   # set of chords for this song structure
            print("Context for this structure:")
            print(context)

            # Customize the context to make it different from the previous structure
            print("Main Context Changed:")
            print(context[:4])
            context = self.customize(prev=prev, curr=context)
            print(context[:4])

            struct.generate(chords=context)
            prev = context[:]
            start = stop

            print("\n\n\n\n")
                        

    def customize(self, prev, curr):

        if not bool(prev): 
            return curr
        
        # main set of 4 chords
        main_prev = prev[:4]
        main_curr = curr[:4]

        shared_ind = set()
        # double for loop check, not proud
        for i in range(len(main_curr)):
            for j in range(len(main_prev)):
                if main_curr[i].name == main_prev[j].name:
                    shared_ind.add(i)

        if len(shared_ind) <= 1:
            # 1 or 0 chords that are shared, do nothing
            return curr
        
        if self.params['chord_complexity'] <= 2:
            for ind in shared_ind:
                curr[ind].add_rem7()
        else:
            for ind in shared_ind:
                curr[ind].change_maj_min()
        
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
