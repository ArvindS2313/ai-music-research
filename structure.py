import random
from chord import Chord

'''
Class definition for a song structure object (e.g., verse, chorus).
'''

class Structure:

    def __init__(self, name, params):
        self.name = name
        self.params = params
        self.gen_params()
        self.gen_components()

    def __repr__(self):
        return self.name
    
    def gen_components(self):
        alph = "ABCDEFGHIJKL"
        comp_structure = (10 * list(alph)[:self.num_components])[:self.len]
        random.shuffle(comp_structure)

        # randomized letters, so convert back to ABCD... notation
        conv = {}
        place = 0
        for m in comp_structure:
            if m not in conv.keys():
                conv[m] = alph[place] 
                place += 1
        
        # convert entries in comp_structure
        comp_structure = [conv[m] for m in comp_structure]
        self.cs = comp_structure
    
    def gen_params(self):
        ''' Generates the component structure for the song structure'''

        # decide on song length
        # if intro or outro - make shorter
        if self.name == "intro" or self.name == "outro":
            if self.params["song_length"] == 1:
                len = 2
            elif self.params["song_length"] == 2:
                len = 3
            elif self.params["song_length"] < 5:
                len = 4
            else:
                len = 5
        else:
            if self.params["song_length"] == 1:
                len = 5
            elif self.params["song_length"] == 2:
                len = 7
            elif self.params["song_length"] < 5:
                len = 9
            else:
                len = random.randint(10, 11)
        
        # decide on variety
        if self.params["variety"] == 1:
            num_components = min(1 if self.name in ["intro", "outro"] else 2, len)
        elif self.params["variety"] == 2:
            num_components = min(1 if self.name in ["intro", "outro"] else 3, len)
        elif self.params["variety"] == 3:
            num_components = min(4 if len <= 7 else 6, len)
        elif self.params["variety"] == 4:
            num_components = min(7 if len < 10 else random.randint(8, 9), len)
        else:
            num_components = len
        
        # decide on accidentals
        num_repeats = len - num_components
        if self.params["accidentals"] == 1:
            num_acc = min(num_repeats, 1)
        elif self.params["accidentals"] < 4:
            num_acc = min(num_repeats, 3)
        elif self.params["accidentals"] == 4:
            num_acc = min(num_repeats, 4)
        else:
            num_acc = min(num_repeats, random.randint(5,6))

        # Parameters:
        # len = length of song
        # num_components = number of different components in song
        # num_acc = number of accidentals for SAME components only
        self.len, self.num_components, self.num_acc = len, num_components, num_acc
    

    def generate(self, chords):
        '''
        Takes in a set of chords (list of strings) and fills in the measure sequence 
        based on those chords. Chords is a required parameter.
        '''
        assert chords is not None
        assert len(chords) >= 4 + self.num_components

        alph = "ABCDEFGHIJKL"[:self.num_components]
        measure_structures = {}
        # first measure is always the first four chords
        base = chords[:4]
        measure_structures[alph[0]] = base

        # choose one position to be changing position, emphasis on last one
        pos_change = 3 if random.random() > 0.3 else random.randint(0, 2)

        # fill the rest of the components in 
        for i in range(1, self.num_components):
            additive = chords[:4]
            additive[pos_change] = chords[i-1+4]
            measure_structures[alph[i]] = additive

        # remove duplicates if variety rating is 4 or 5
        if self.params['variety'] >= 4:
            for comp in measure_structures.keys():
                prev = []
                prev_names = []
                for ch in measure_structures[comp]:
                    if ch.name not in prev_names:
                        # not a duplicate 
                        prev_names.append(ch.name)
                        prev.append(ch)
                measure_structures[comp] = prev

        self.measure_structures = measure_structures
        self.chords = []
        for c in self.cs:
            self.chords.extend(self.measure_structures[c])





        














