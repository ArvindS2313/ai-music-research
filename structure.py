import random

'''
Class definition for a song structure object (e.g., verse, chorus).
'''

# TODO: Clean up code 
# TODO: Allow for accidental modification 

class Structure:

    def __init__(self, name, params):
        self.name = name
        self.params = params
        self.gen_params()
        self.gen_components()

    def __repr__(self):
        return self.name
    
    def gen_params(self):
        ''' 
        Determines three properties of the song: its length (number of measures), 
        number of unique components, and number of accidentals between repeated components.

        Postcondition: num_components <= len; num_acc <= num_repeats
        '''

        # decide on measure length

        # if intro or outro - make shorter
        if self.name == "intro" or self.name == "outro":
            if self.params["song_length"] <= 3:
                len = 2
            else:
                len = 4

        # nornal song structure length if not intro or outro
        else:
            if self.params["song_length"] == 1:
                len = 4
            elif self.params["song_length"] == 2:
                len = 6
            elif self.params["song_length"] <= 4:
                len = 8
            else:
                len = 12
        
        # decide on number of unique components (variety)
        if self.params["variety"] == 1:
            num_components = 1
        elif self.params["variety"] == 2:
            num_components = int(0.5 * len)
        elif self.params["variety"] == 3:
            num_components = 2 if len <= 2 else int(0.67 * len)
        elif self.params["variety"] == 4:
            num_components = 2 if len <= 2 else int(0.75 * len)
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

        self.len, self.num_components, self.num_acc = len, num_components, num_acc

    def gen_components(self):
        alph = "ABCDEFGHIJKL"
        self.comp_structure = (10 * list(alph)[:self.num_components])[:self.len]
        random.shuffle(self.comp_structure)

        # randomized letters, so convert back to ABCD... notation
        conv = {}
        place = 0
        for m in self.comp_structure:
            if m not in conv.keys():
                conv[m] = alph[place] 
                place += 1
        
        # convert entries in comp_structure
        self.comp_structure = [conv[m] for m in self.comp_structure]


    def generate(self, chords):
        '''
        Takes in a set of chords (list of strings) and fills in the measure sequence 
        based on those chords. Chords is a required parameter.
        '''
        assert chords is not None
        assert len(chords) >= 4 + self.num_components

        alph = "ABCDEFGHIJKL"[:self.num_components]
        self.measure_structures = {}

        # first measure is always the first four chords
        base = chords[:4]
        self.measure_structures[alph[0]] = base

        # choose one position to be changing position, emphasis on last one
        pos_change = 3 if random.random() > 0.3 else random.randint(0, 2)

        # fill the rest of the components in 
        for i in range(1, self.num_components):
            additive = chords[:4]
            additive[pos_change] = chords[i-1+4]
            self.measure_structures[alph[i]] = additive

        # remove duplicates if variety rating is 4 or 5
        if self.params['variety'] >= 4:
            for comp in self.measure_structures.keys():
                prev = []
                prev_names = []
                for ch in self.measure_structures[comp]:
                    if ch.name not in prev_names:
                        # not a duplicate 
                        prev_names.append(ch.name)
                        prev.append(ch)
                self.measure_structures[comp] = prev

        # self.chords represents the list of chords for song structure, in proper order
        self.chords = []

        print(self.measure_structures)
        print("\n\n")
        for c in self.comp_structure:
            self.chords.extend(self.measure_structures[c])



