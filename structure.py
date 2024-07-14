import random
from chord import *
from note import *
import generate

# TODO: Clean up code 
# TODO: Allow for accidental modification 

class Structure:
    '''
    Class definition for a song structure object (e.g., verse, chorus).
    '''

    def __init__(self, name, params):
        '''
        Initializes a measure structure object with a name and parameters
        Generates measure structure
        '''
        self.name = name
        self.params = params
        self.order = []     # measure order
        self.ms = {}    # measure structure dictionary (outlines each measure)
        
        # generate rhythm level 
        if self.params['rhythm_complexity'] == 1: 
            self.rhythm_level = random.choices([1, 2], weights=[0.7, 0.3], k=1)[0]
        elif self.params['rhythm_complexity'] == 2:
            self.rhythm_level = random.choices([2, 3, 4], weights=[0.3, 0.5, 0.2], k=1)[0]
        else:
            self.rhythm_level = random.choices([4, 5], weights=[0.8, 0.2])[0]
                
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

        # decide on number of measures
        # if intro or outro - make shorter
        if self.name == "I" or self.name == "O":
            if self.params["song_length"] <= 3:
                self.len = 2
            else:
                self.len = 4

        # nornal song structure length if not intro or outro
        else:
            if self.params["song_length"] == 1:
                self.len = 4
            elif self.params["song_length"] == 2:
                self.len = 6
            elif self.params["song_length"] <= 4:
                self.len = 8
            else:
                self.len = 12

        # decide on number of unique measures (measure_complexity)
        if self.params["measure_complexity"] == 1:
            self.unique_measures = {'full':1, 'slight':0}
        elif self.params["measure_complexity"] == 2:
            self.unique_measures = {'full':2, 'slight':0}
        elif self.params["measure_complexity"] == 3:
            self.unique_measures = {'full':2, 'slight':1}
        elif self.params["measure_complexity"] == 4:
            self.unique_measures = {'full':3, 'slight':0}
        elif self.params["measure_complexity"] == 5:
            self.unique_measures = {'full':3, 'slight':1}


    def gen_components(self):
        '''
        Fills in the keys of the measure structure dictionary; sets the values to None
        Later, the value will be a dictionary containing the chords and rhythm
        '''

        alph = "ABCD"[:self.unique_measures['full']+self.unique_measures['slight']]
        self.order = list((100*alph)[:self.len])

        if self.unique_measures['slight']:
            to_rep = alph[-1]
            rep_with = random.choice(alph[:-1]) + "'"
            self.order = [a if a != to_rep else rep_with for a in self.order]

        self.ms = {s:None for s in self.order}


    # long method lol
    @staticmethod
    def generate_rhythm(ts, level):
        if ts != "4/4": return None # only handling 4/4 for now
        if level == 1:
            choices = [
                [4], 
                [1, 1, 1, 1], 
                [2, 2], 
                [3, 1], [1, 3]
            ]
            c = random.choice(choices)
            if c == [2, 2]:
                if random.random() < 1/3:
                    c = [2, 1, 1]
                elif random.random() < 0.5:
                    c = [1, 1, 2]

        elif level == 2:
            path = random.random()
            if path < 0.75:
                # generation from scratch using 1s and 2 1/2s 
                c = []
                beat_sum = 0 
                while beat_sum != 4:
                    c.extend([1/2, 1/2] if random.random() < 0.5 else [1])
                    beat_sum += 1
                
                for ind in range(1, len(c)+1):
                    if sum(c[:ind]) == 2:
                        beg = c[:ind]
                        end = c[ind:]
                if random.random() < 1/3:
                    c = beg + [2] if c!= [1, 1, 2] else c
                elif random.random() < 0.5:
                    c = [2] + end if c!= [1, 1, 2] else c

            else: 
                c = [3, 1/2, 1/2] if random.random() < 0.5 else [1/2, 1/2, 3]
        
        elif level <= 4:
            c = []
            beat_sum = 0 
            while beat_sum != 4:
                r = random.random()
                # if sum <=2, can add a 2, else, only 1 or 1/2
                if beat_sum > 2:
                    c.extend([1/2, 1/2] if random.random() < 1/3 else [1])
                    beat_sum += 1
                else:
                    if r < 1/3: c.extend([2]); beat_sum += 2
                    elif r < 2/3: c.extend([1]); beat_sum += 1
                    else: c.extend([1/2, 1/2]); beat_sum += 1

            for b in range(len(c)):
                if c[b] == 2:
                    choices = [[c[b]], [0.5, 1, 0.5], [1.5, 0.5]]
                    if level == 3:
                        weights = [1/3, 0, 2/3]
                    elif level == 4:
                        weights = [1/5, 1/2, 3/10]
                    new = random.choices(choices, weights=weights, k=1)[0]
                    c[b:b+1] = new
            
        else:
            c = []
            beat_sum = 0 

            choices = [1/2, 3/2, 1, 2, 3]
            weights = [0.3, 0.25, 0.20, 0.13, 0.12]
            while beat_sum < 4:
                new = random.choices(choices, weights=weights, k=1)[0]
                while beat_sum + new > 4:
                    new = random.choices(choices, weights=weights, k=1)[0]
                beat_sum += new
                c.append(new)
            
        return c
    

    def clean_chords(self):
        '''
        Adjusts endings of the chords depending on the chord_complexity rating
        '''
        if self.params['chord_complexity'] <= 2:
            # fully major minor 
            percent_maj_min = 1
        elif self.params['chord_complexity'] == 3:
            percent_maj_min = 0.9 
        elif self.params['chord_complexity'] == 4:
            percent_maj_min = 0.8
        else:
            percent_maj_min = 0.7
        
        for m in self.ms.keys():
            maj_min, non_maj_min = [], []
            for ch in range(len(self.ms[m]['chords'])):
                if self.ms[m]['chords'][ch].get_type() in ['maj', 'min']:
                    maj_min.append(ch)
                else:
                    non_maj_min.append(ch)
                
            # simplify/complexify chords if necessary 
            while int(percent_maj_min*len(self.ms[m]['chords'])) != len(maj_min):
                # make more simpler i.e., remove from non_maj_min to maj_min
                if int(percent_maj_min*len(self.ms[m]['chords'])) > len(maj_min):
                    # move from non_maj_min to maj_min
                    remove = random.choice(non_maj_min)
                    self.ms[m]['chords'][remove].simplify_end()
                    maj_min.append(remove)
                    non_maj_min.remove(remove)
                else:
                    # move from maj_min to non_maj_min
                    remove = random.choice(maj_min)
                    self.ms[m]['chords'][remove].randomize()
                    maj_min.remove(remove)
                    non_maj_min.append(remove)


    def generate_chords(self, type=None):
        '''
        Fills in self.ms with chords and rhythms for each measure structure
        '''
        
        # 1. For each measure structure in self.ms, generate a rhythm.
        num_chords = 0 
        for s in self.ms.keys():
            rhythm = Structure.generate_rhythm("4/4", level=self.rhythm_level)
            self.ms[s] = {'ch_rhythm': rhythm, 'chords':None}
            num_chords += len(rhythm)

        # 2. For each measure structure in self.ms, generate the chords
        chords = generate.tr_gen("saved-models/model-rand-ug.pth", context=generate.context1, 
                                 num_tokens=num_chords)[len(generate.context1):]
        start = 0
        for m in self.order:
            if self.ms[m]['chords'] is None:
                # fill in the chords for that measure structure 
                end = len(self.ms[m]['ch_rhythm'])
                self.ms[m]['chords'] = [Chord(c) for c in chords[start:start+end]]
                start += end


    def generate_melody(self):
        for m in self.ms.keys():
            self.ms[m]['mel_rhythm'] = [1, 1, 1, 1]   # to start off with
            melody = []
            for ch in self.ms[m]['chords']:
                r_n = random.choice(ch.notes)
                r_n = Note(r_n.name, r_n.octave)
                r_n.change_octave(by_how_much=2, up_or_down='up')
                melody.append(r_n)
            melody = melody[:len(self.ms[m]['mel_rhythm'])]
            if len(melody) < len(self.ms[m]['mel_rhythm']):
                melody.extend(['r' for _ in range(len(self.ms[m]['mel_rhythm'])-len(melody))])

            self.ms[m]['melody'] = melody

