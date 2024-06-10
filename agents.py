import random
from structure import Structure
from chord import Chord
import generate

class Agent:
    # boilerplate class
    def __init__(self, params) -> None:
        self.params = params
        self.conv = {"I": "intro", "V":"verse", "C": "chorus", "O":"outro", 
                     "B":"bridge", "S": "solo", "IL": "interlude"}

        # Define parameters which will hold the song structures
        self.structs = []
        self.structs_str = []
        self.structs_dict = {}        


    def generate(self):
        assert self.params != {}

        self.chords = generate.mlp_gen(context=generate.context2, block_size=len(generate.context2),
                                       num_tokens=500, type="time", kind="00")
        self.more_chords = generate.mlp_gen(context=self.chords[400:], block_size=len(self.chords[400:]),
                                       num_tokens=500, type="time", kind="00")
        self.gen_chords = [Chord(c) for c in self.chords[len(generate.context2):]]  # convert to Chord objects; don't feed input chords
        self.more_chords = [Chord(c) for c in self.chords[len(self.chords[400:]):]]


        # apply chord generation for each song structure 
        prev = []
        start = 0
        stop = -1

        self.structs = [None for _ in range(len(self.structs_str))]
        for s in range(len(self.structs_str)):
            if self.structs_str[s] not in self.structs_dict.keys():
                struct = Structure(self.structs_str[s], self.params)
                
                stop = start + struct.num_components + 4   # technically one extra
                context = self.gen_chords[start:stop]   # set of chords for this song structure

                # Customize the context to make it different from the previous structure
                context = self.customize(prev=prev, curr=context)

                struct.generate(chords=context)
                prev = context[:]
                start = stop

                self.structs_dict[self.structs_str[s]] = struct

                print(struct)
                print(struct.ms)
                print(struct.ms_chords)
                print(struct.all_chords)
                print("\n\n")

            self.structs[s] = self.structs_dict[self.structs_str[s]]

        print("\n\nApply variation algorithm")
        start = 0
        for s in self.structs_dict.keys():
            start = self.structs_dict[s].vary_chords(self.more_chords, start)
            
        for s in self.structs_dict.keys():
            struct = self.structs_dict[s]
            print(struct)
            print(struct.ms)
            print(struct.ms_chords)
            print(struct.all_chords)
            print("\n\n")

                        

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
            ["I", "V", "V", "C", "B", "C", "O"],
            ["I", "V", "C", "V", "S", "V", "O"],
            ["I", "V", "C", "V", "B", "C", "O"],
        ]
        self.structs_str = random.choice(self.poss_structs)


class MediumSimplistic(Agent):
    '''Medium length, simple structures, few changes'''
    def __init__(self, params) -> None:
        super().__init__(params)
        self.poss_structs = [
            ["I", "V", "C", "V", "C", "V", "C", "O"],
            ["I", "V", "V", "C", "B", "V", "V" "C", "O"],
            ["I", "V", "C", "V", "IL", "C", "V", "O"],
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
            ["I", "V", "V", "C", "IL", "V", "S", "C", "O"],
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
            ["I", "V", "C", "V", "C", "S", "V", "B", "V", "S", "C", "O"],
            ["I", "V", "V", "C", "B", "V", "C", "S", "C", "IL", "C", "O"]
        ]
        self.structs_str = random.choice(self.structures)


