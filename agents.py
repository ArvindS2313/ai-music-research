import random
from structure import Structure

'''conv different for all agents.'''
''' I'll form more agents as time goes on... here are three to begin with'''

class ShortSimpleAgent():
    def __init__(self, params) -> None:
        self.structures = [
            ["I", "V", "C", "V", "C", "O"],
            ["I", "V", "C", "V", "O"],
        ]
        self.s_structure = random.choice(self.structures)
        self.params = params
        self.structs = self.form_structures()

    def form_structures(self):
        conv = {"I": "intro", "V":"verse", "C": "chorus", "O":"outro"}
        structs = [Structure(name=conv[x], params=self.params) for x in self.s_structure]
        return structs


class SimpleAgent():
    def __init__(self, params) -> None:
        structures = [
            ["I", "V", "C", "V", "C", "O"],
            ["I", "V", "V", "C", "B", "C", "O"],
            ["I", "V", "C", "V", "C", "V", "O"],
            ["I", "V", "C", "V", "V", "C", "O"],
        ]
        self.song_structure = random.choice(structures)
        self.params = params
        self.structs = self.form_structures()

    def form_structures(self):
        conv = {"I": "intro", "V":"verse", "C": "chorus", "O":"outro", "B":"bridge"}
        structs = [Structure(name=conv[x], params=self.params) for x in self.s_structure]
        return structs


class LongComplex():
    def __init__(self, params) -> None:
        structures = [
            ["I", "V", "C", "B", "V", "S", "C", "O"],
            ["I", "V", "C", "V", "S", "B", "S", "V", "O"],
            ["I", "V", "V", "C", "B", "V", "S", "V", "C", "O"],
            ["I", "V", "S", "C", "V", "B", "V", "C", "O"],
            ["I", "V", "C", "V", "B", "S", "V", "B", "C", "O"]
        ]
        self.song_structure = random.choice(structures)
        self.structs = self.form_structures()

    def form_structures(self):
        conv = {"I": "intro", "V":"verse", "C": "chorus", "O":"outro", "B":"bridge"
                , "S": "solo"}
        structs = [Structure(name=conv[x], params=self.params) for x in self.s_structure]
        return structs

