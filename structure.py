import random
from chord import *
from note import *
from pprint import pprint
import generate

# TODO: Clean up code 
# TODO: Remove hardcoded bits and put into a database
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
        
        self.gen_params()
        self.gen_components()

        self.melody = []    # list of dictionaries detailing melody notes & rhythm
        self.bass = []      # list of dictionaries detailing bass line notes 

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
        if self.name == "I" or self.name == "O" or self.name == "OS":
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

        if self.name == "S":
            self.len *= 2

        # decide on number of unique measures (measure_complexity)
        if self.params["measure_complexity"] == 1:
            self.unique_measures = 1
        elif self.params["measure_complexity"] == 2:
            self.unique_measures = 2
        elif self.params["measure_complexity"] == 3:
            self.unique_measures = 3
        elif self.params["measure_complexity"] == 4:
            self.unique_measures = 3
        elif self.params["measure_complexity"] == 5:
            self.unique_measures = 4


    def gen_components(self):
        '''
        Fills in the keys of the measure structure dictionary; sets the values to None
        Later, the value will be a dictionary containing the chords and rhythm
        '''

        alph = "ABCD"[:self.unique_measures]
        self.order = list((100*alph)[:self.len])            
        self.ms = {s:None for s in self.order}


    # long method lol
    @staticmethod
    def generate_chord_rhythm(ts, level):
        assert ts == '4/4', "Only handling 4/4 time signature for now"
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
        1. Adjusts endings of chords based on chord_complexity rating
        2. Keeps required percentage of chords in the key 
        '''

        # Adjust chord endings 
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

        # Adjust accidentals 
        if self.params['accidentals'] == 1:
            percent = 1 
        elif self.params['accidentals'] == 2:
            percent = 0.9; lim = 2
        else:
            percent = 0.8; lim = 3

        in_c = ["Cmaj", "Dm", "Em", "Fmaj", "Gmaj", "Am", "Bdim"]
        for m in self.ms.keys():
            chs = [ch for ch in self.ms[m]['chords']]
            print(f"{m} Chords: \t {chs}")
            print([c.simp_chord for c in chs])
            

    def generate_chords(self, type=None):
        '''
        Fills in self.ms with chords and rhythms for each measure structure
        '''
        
        # 1. For each measure structure in self.ms, generate a rhythm.
        num_chords = 0 
        for s in self.ms.keys():
            # generate rhythm level 
            if self.params['rhythm_complexity'] == 1: 
                rhythm_level = random.choices([1, 2], weights=[0.7, 0.3], k=1)[0]
            elif self.params['rhythm_complexity'] == 2:
                rhythm_level = random.choices([2, 3, 4], weights=[0.3, 0.5, 0.2], k=1)[0]
            else:
                rhythm_level = random.choices([4, 5], weights=[0.8, 0.2])[0]

            if self.ms[s] is None:
                rhythm = Structure.generate_chord_rhythm("4/4", level=rhythm_level)
                self.ms[s] = {'rhythm': rhythm, 'chords':None}
                num_chords += len(rhythm)


        # 2. For each measure structure in self.ms, generate the chords
        chords = generate.tr_gen("saved-models/model-rand-ug.pth", context=generate.context1, 
                                 num_tokens=num_chords)[len(generate.context1):]
        start = 0
        for m in self.order:
            if self.ms[m]['chords'] is None:
                # fill in the chords for that measure structure 
                end = len(self.ms[m]['rhythm'])
                self.ms[m]['chords'] = [Chord(c) for c in chords[start:start+end]]
                start += end


    @staticmethod
    def generate_melody_rhythm(ts, level, include_16ths=False, is_solo=False):
        '''
        Generate the melody rhythm for a measure in 4/4 time
        '''
        assert ts == '4/4', "Only handling 4/4 time signature for now"
        if level == 1:
            choices = [[1, 1, 1, 1], [2, 2], [2, 1, 1], [1, 1, 2], [1, 2, 1]]
            c = random.choices(choices, weights=[0.7, 0.15, 0.05, 0.05, 0.05], k=1)[0]

        elif level == 2:
            if random.random() < 0.1:
                c = random.choice(([3, 1], [1, 3]))
            else:
                choices = [[1], [0.5, 0.5]]
                c = []
                for _ in range(4):
                    c.extend(random.choice(choices))

        else:
            # ugh, I'm not proud of the hardcodings!
            choices, weights = [], []
            if level == 3:
                choices = [[1], [2], [0.5, 0.5], [1.5, 0.5], [0.25, 0.25, 0.25, 0.25]] 
                weights = [0.3, 0.1, 0.2, 0.2, 0.2]
                if not include_16ths: weights = [0.3, 0.1, 0.2, 0.2, 0]
                if is_solo: weights = [0.1, 0.05, 0.1, 0.2, 0.45]
            elif level == 4:
                choices = [
                    [1], [2], [0.5, 0.5], [1.5, 0.5], [0.25, 0.25, 0.25, 0.25],
                    [1.5, 0.25, 0.25], [0.75, 0.25],
                ]
                weights = [0.25, 0.1, 0.2, 0.1, 0.15, 0.1, 0.1]
                if not include_16ths: weights = [0.25, 0.1, 0.2, 0.1, 0, 0, 0]
                if is_solo: weights = [0.1, 0.05, 0.1, 0.1, 0.2, 0.25, 0.2]
            else:
                choices = [
                    [1], [0.5, 0.5], [1.5, 0.5], [0.5, 1, 0.5], 
                    [0.25, 0.25, 0.25, 0.25], [0.25, 0.5, 0.25], 
                    [1.5, 0.25, 0.25], [0.75, 0.25],
                ]
                weights = [0.2, 0.15, 0.1, 0.15, 0.1, 0.1, 0.1, 0.1]
                if not include_16ths: weights = [0.2, 0.15, 0.1, 0.15, 0, 0, 0, 0]
                if is_solo: weights = [0.05, 0.1, 0.1, 0.05, 0.25, 0.1, 0.2, 0.15]

            c = []
            beat_sum = 0
            while beat_sum < 4:
                choice = random.choices(choices, weights, k=1)[0]
                while beat_sum + sum(choice) > 4:
                    choice = random.choices(choices, weights, k=1)[0]
                c.extend(choice)
                beat_sum += sum(choice)

        return c


    def generate_melody(self):
        '''
        Generates the melody for the entire song structure
        '''

        # Don't generate a melody for intros and conclusion
        if self.name == "I" or self.name == "O":
            self.melody = [{'rhythm': [1, 1, 1, 1], 'notes': ['r', 'r', 'r', 'r']}]*self.len
            return

        # Generate a melody for each measure
        for m in range(self.len):        
            # 1/5th chance that this measure will be the same as laclest measure
            include_16ths = False if self.name == "V" or self.name == "C" else True
            is_solo = True if self.name == "S" or self.name == "OS" else False

            # Decide on a rhythm 
            if self.params['rhythm_complexity'] == 1: 
                rhythm_level = random.choices([1, 2, 3, 4, 5], [0.2, 0.3, 0, 0, 0], k=1)[0]
            elif self.params['rhythm_complexity'] == 2:
                rhythm_level = random.choices([1, 2, 3, 4, 5], [0.2, 0.3, 0.3, 0.2, 0], k=1)[0]
            else:
                rhythm_level = random.choices([1, 2, 3, 4, 5], 
                                                [0.15, 0.15, 0.2, 0.25, 0.25], k=1)[0]


            rhythm = Structure.generate_melody_rhythm('4/4', rhythm_level, 
                                                        include_16ths=include_16ths,
                                                        is_solo=is_solo)                                                                                                         

            up_or_down = ['d' for _ in range(len(rhythm)//2)]
            up_or_down += ['u' for _ in range(len(rhythm)-len(up_or_down))]
            random.shuffle(up_or_down)
            if m == 0:  
                # First note of first measure won't have a direction
                up_or_down[0] = "DNE"

            # Generate weights depending on step size preference
            choices, weights = list(range(0, 8)), []
            if self.params['step_size'] == 1:
                weights = [0.3, 0.5, 0.2, 0, 0, 0, 0, 0]
            if self.params['step_size'] == 2:
                weights = [0.13, 0.5, 0.2, 0.10, 0.05, 0, 0, 0]
            if self.params['step_size'] == 3:
                weights = [0.1, 0.48, 0.15, 0.13, 0.07, 0.05, 0.02, 0]

            
            all_notes = list("CDEFGAB")
            melody = []

            # Generate rest of notes
            for d in range(len(up_or_down)):
                dir = up_or_down[d]
                if dir == 'DNE': 
                    # First note of first measure
                    curr_note = random.randint(0, 6)
                    curr_oct = 5 if curr_note < 3 else 4
                    melody.append(Note(all_notes[curr_note], curr_oct))
                else:
                    size = random.choices(choices, weights, k=1)[0]
                    curr_note += size if dir == 'u' else -size
                    
                    # note goes beyond 'B' of current octave 
                    if curr_note >= 7:
                        curr_note %= 7
                        curr_oct += 1
                    
                    # note goes below 'C' of current octave 
                    if curr_note < 0:
                        curr_note %= 7
                        curr_oct -= 1

                    # note hits octave 3 -- to low!
                    if curr_oct < 4:
                        curr_note, curr_oct = random.randint(0, 3), 4 
                        up_or_down[d+1:] = ['u']*len(up_or_down[d+1:])

                    # note hits octave 6 -- to high!
                    if curr_oct > 5:
                        curr_note, curr_oct = random.randint(5, 6), 5
                        up_or_down[d+1:] = ['d']*len(up_or_down[d+1:])

                    melody.append(Note(all_notes[curr_note], curr_oct))


            # 1/6 chance that the rhythm & notes is repeated in half 
            if random.random() < 1/6 and 3 not in rhythm and 4 not in rhythm and self.name not in ["S", "OS"]:
                for i in range(len(rhythm)):
                    if sum(rhythm[:i+1]) == 2:
                        rhythm = rhythm[:i+1] * 2
                        melody = melody[:i+1] * 2
                        break 
            
            # Append the rhythm and notes for the measure into self.melody
            self.melody.append({'rhythm':rhythm, 'notes':melody})


    @staticmethod
    def semitone_dist(n1:Note, n2:Note):
        '''
        Calculates the distance in semitones between the notes
        '''
        dist = abs(Note.NOTES[n1.name] - Note.NOTES[n2.name])
        dist = min(dist, 12-dist)
        return dist 
    

    @staticmethod
    def intersect_ranges(r1, r2):
        start = max(r1[0], r2[0])
        end = min(r1[1], r2[1])
        if start < end:
            return (start, end)


    def smoother(self):
        '''
        Makes the melody and chords cohere by removing clashes
        '''
        # If it is an intro or outro, there is no melody, so return
        if self.name == "I" or self.name == "O":
            return

        for m in range(len(self.melody)):
            msre_struct = self.order[m]
            mel_r, mel_n = self.melody[m]['rhythm'], self.melody[m]['notes']

            mel_time = 0 
            # Loop through each of the notes in the melody measure
            for n in range(len(mel_n)):
                mel_range = (mel_time, mel_time+mel_r[n])   # time range in beats of the melody note
    
                ch_in_range = []
                ch_time = 0 
                # Find all the chords which are in the same range as the note
                for c in range(len(self.ms[msre_struct]['rhythm'])):
                    ch_range = (ch_time, ch_time+self.ms[msre_struct]['rhythm'][c])
                    does_int = Structure.intersect_ranges(mel_range, ch_range)

                    if does_int is not None:
                        # Chord's range intersects with the melody note range
                        ch = self.ms[msre_struct]['chords'][c]
                        ch_in_range.append(ch)
                    ch_time += self.ms[msre_struct]['rhythm'][c]

                if len(ch_in_range) == 1:
                    ch = ch_in_range[0]

                    # Assign a rank & change melody note if needed
                    if 0 in [Structure.semitone_dist(mel_n[n], note) for note in ch.notes]:
                        rank = 1 

                    elif Structure.semitone_dist(mel_n[n], ch.notes[0]) == 1:
                        rank = 4 
                        # Change the note to the root
                        mel_n[n] = Note(ch.notes[0].name, mel_n[n].octave)
                        if mel_n[n].name == "C":
                            mel_n[n].change_octave(1, 'up')
                        if mel_n[n].name == "B":
                            mel_n[n].change_octave(1, 'down')

                    elif 1 in [Structure.semitone_dist(mel_n[n], note) for note in ch.notes]:
                        rank = 3
                        # 75% chance of changing to a better note 
                        if random.random() < 0.75:
                            l = [Structure.semitone_dist(mel_n[n], note) for note in ch.notes]
                            pos = l.index(1)
                            mel_n[n] = Note(ch.notes[pos].name, mel_n[n].octave)
                            if mel_n[n].name == "C":
                                mel_n[n].change_octave(1, 'up')
                            if mel_n[n].name == "B":
                                mel_n[n].change_octave(1, 'down')

                    elif 2 in [Structure.semitone_dist(mel_n[n], note) for note in ch.notes]:
                        rank = 2
                    else:
                        rank = None

                mel_time += mel_r[n]


    def generate_bass(self):
        '''
        Generates a walking bass line; very simple.
        '''

        # No bass line in intro, outro, or outro solos
        if self.name == "I" or "O" in self.name:
            self.bass = [{'rhythm': [1, 1, 1, 1], 'notes': ['r', 'r', 'r', 'r']}]*self.len
            return
        
        # Bass line notes are the notes from the first four chords; if less than 4
        # chords, the remaining notes are rests.
        for s in self.order:
            rhythm = []
            # Possibility that rhythm might become slightly more complex
            for _ in range(4):
                rhythm.extend([1] if random.random() < 0.8 else [1/2, 1/2])

            bass = []
            for ch in self.ms[s]['chords'][:len(rhythm)]:
                bass.append(Note(random.choice(ch.notes).name, 2))
            bass.extend(['r' for _ in range(len(rhythm)-len(bass))])

            self.bass.append({'rhythm': rhythm, 'notes':bass})


    def transpose(self, to_key):
        '''
        Transposes all the notes & chords to the desired key
        '''

        # Transpose the chords in self.ms 
        for m in self.ms.keys():
            for ch in self.ms[m]['chords']:
                ch.transpose(key=to_key)

        # Transpose the melody/solo notes
        for m in self.melody:
            for n in m['notes']:
                if n != "r":
                    n.transpose(key=to_key)


params = {
    'song_complexity': 3,
    'measure_complexity': 4,
    'rhythm_complexity': 3,
    'chord_complexity': 3,
    'song_length': 3,
    'step_size': 3,
    'accidentals': 2
}


a = Structure('V', params=params)
a.generate_chords()
a.clean_chords()
