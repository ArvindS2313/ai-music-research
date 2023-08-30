import random

class Structure():
    def __init__(self, name, params):
        self.name = name
        self.params = params
        
        # Determine the segment arrangement
        # if params["song_complexity"] == 1 and params["length"] == "short":
        #     pass

        self.generate()

    def __repr__(self):
        return f"Song Structure: {self.name}"
            
    def generate(self):
        ''' Generates the chord sequence using the NN. '''
        pass

