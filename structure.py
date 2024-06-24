import random
import generate

'''
Class definition for a song structure object (e.g., verse, chorus).
'''

# TODO: Clean up code 
# TODO: Allow for accidental modification 

class Structure:

    def __init__(self, name, params):
        '''
        Initializes a measure structure object with a name and parameters
        Generates measure structure
        '''
        self.name = name
        self.params = params
        self.all_chords = []    # entire list of chords
        self.ms = []            # outlined measure structures (list: strings)
        self.ms_chords = {}     # measure chords (dict: chord obj)

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
        if self.name == "I" or self.name == "O":
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
        '''
        Fills in outlined measure structures (ms)
        '''

        alph = "ABCDEFGHIJKL"
        self.ms = (10 * list(alph)[:self.num_components])[:self.len]
        random.shuffle(self.ms)

        # randomized letters, so convert back to ABCD... notation
        conv = {}
        place = 0
        for m in self.ms:
            if m not in conv.keys():
                conv[m] = alph[place] 
                place += 1
        
        # convert entries in comp_structure
        self.ms = [conv[m] for m in self.ms]

    
    def generate_rhythm(self, ts):
        if ts != "4/4": return None # only handling 4/4 for now
        if self.params['song_complexity'] == 1:
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

        elif self.params['song_complexity'] == 2:
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
        
        elif self.params['song_complexity'] <= 4:
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

            if 2 in c and self.params['song_complexity'] == 4:
                # replacement of 2 with 0.5 1 0.5
                for b in range(len(c)):
                    if c[b] == 2 and random.random() < 1/2:
                        c[b:b+1] = [0.5, 1, 0.5]

            elif 2 in c: 
                for b in range(len(c)):
                    if c[b] == 2 and random.random() < 1/2:
                        c[b:b+1] = [1.5, 0.5]
            
            
        
        else:
            if random.random() < 0.8:
                c = []
                beat_sum = 0 
                while beat_sum != 4:
                    choice = [5]    # illogical to begin
                    while beat_sum + sum(choice) < 4:
                        r = random.random()
                        if r < 1/5: choice = [1/2]
                        elif r < 1/2: choice = [1/2, 1/2]
                        elif r < 3/4: choice = [1]
                        elif r < 4/5: choice = [2]
                    c.extend(choice)
            else:   
                c = [3, 1] if random.random() < 1/3 else [3, 1/2, 1/2] if \
                    random.random() < 0.5 else [1/2, 1/2, 3]

        return c
            

    def generate(self, type):
        pass



    # def generate(self, chords):
    #     '''
    #     Takes in a set of chords (list of strings) and fills in ms_chords  
    #     and chords based on those chords. Chords is a required parameter.
    #     '''
    #     assert chords is not None
    #     assert len(chords) >= 4 + self.num_components

    #     alph = "ABCDEFGHIJKL"[:self.num_components]
    #     self.ms_chords = {}

    #     # first measure is always the first four chords
    #     base = chords[:4]
    #     self.ms_chords[alph[0]] = base

    #     # choose one position to be changing position, emphasis on last one
    #     pos_change = 3 if random.random() > 0.3 else random.randint(0, 2)

    #     # fill the rest of the components in 
    #     for i in range(1, self.num_components):
    #         additive = chords[:4]
    #         additive[pos_change] = chords[i-1+4]
    #         self.ms_chords[alph[i]] = additive

    #     # Perform necessary changes to allign with user preferences
    #     # self.rem_duplicate_measures()
    #     self.update()
    

    # def rem_duplicate_measures(self):
    #     # remove duplicates if variety rating is 4 or 5
    #     if self.params['variety'] >= 4:
    #         for comp in self.ms_chords.keys():
    #             prev = []
    #             prev_names = []
    #             for ch in self.ms_chords[comp]:
    #                 if ch.name not in prev_names:
    #                     # not a duplicate 
    #                     prev_names.append(ch.name)
    #                     prev.append(ch)
    #             self.ms_chords[comp] = prev


    # def vary_chords(self, extra_chords, start):
    #     '''
    #     Varies the chords in each measure structure if necessary to ensure 
    #     variety rating is met
    #     '''
    #     counter = start
    #     print("varying chords for ", self)
    #     if self.params['variety'] >= 4:
    #         # Option 1 is choosing completely different chords, option 2 is modifying the
    #         # exsisting chords, and option 3 is changing the length duration of the chords
    #         opt = 1 if random.random() < 1/2 else 2 # if random.random() < 0.5 else 3
    #         print("opt is ", opt)

    #         # opt 3 is harder to handle, welp
    #         prev_ch = []    # Strings
    #         for c in "ABCDEFGHIJKL"[:len(self.ms_chords)]:
    #             print("Checking ", self.ms_chords[c])
    #             print("Prev_ch as of now: ", prev_ch)

    #             if [ch.name for ch in self.ms_chords[c]] not in prev_ch:
    #                 prev_ch.append([ch.name for ch in self.ms_chords[c]])
    #                 print(self.ms_chords[c], " added to prev_ch")
                    
    #             elif opt == 1:
    #                 print(self.ms_chords[c], " was already found in prev_ch, applying option 1")
    #                 for ch in self.ms_chords[c]:
    #                     ch.randomize()
    #                 print("Chords have now become: ", self.ms_chords[c])
    #             elif opt == 2:
    #                 print(self.ms_chords[c], "  was already found in prev_ch, applying option 2")
    #                 self.ms_chords[c] = [extra_chords[i] for i in range(counter, counter+len(self.ms_chords[c]))]
    #                 # extra_chords = extra_chords[range(len(self.ms_chords[c])):]
    #                 counter += len(self.ms_chords[c])
    #             print()
    #     print()
    #     print()
    #     return counter

    # def update(self):
    #     for c in self.ms:
    #         self.all_chords.extend(self.ms_chords[c])



params = {"song_complexity":5, "chord_complexity":3, "variety":4, "song_length":3, "accidentals":3}
a = Structure('intro', params)
print(a.generate_rhythm("4/4"))