import random
import generate
from generate import tr_gen

class Structure:

    def __init__(self, name, params):
        self.name = name
        self.params = params

        self.len, self.num_components, self.num_acc = self.gen_params()
        self.cs = self.gen_components()
        self.generate()

    def __repr__(self):
        return self.name
    
    def gen_components(self):
        comp_structure = (10 * list("ABCDEFGHIJKL")[:self.num_components])[:self.len]
        random.shuffle(comp_structure)
        return comp_structure
    
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
        return len, num_components, num_acc

            
    def generate(self): 
