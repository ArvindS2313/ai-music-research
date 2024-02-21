import random
from structure import Structure
import generate

'''conv different for all agents.'''
''' I'll form more agents as time goes on... here are three to begin with'''

class Agent():
    # boilerplate class
    def __init__(self) -> None:
        self.structures = []
        self.s_structure = []        
        self.params = {}
        # The rest of the stuff depends on the agent.
    
    def form_structures(self):
        conv = {"I": "intro", "V":"verse", "C": "chorus", "O":"outro", "B":"bridge"
                , "S": "solo", "IL": "interlude"}
        structs = [Structure(name=conv[x], params=self.params) for x in self.s_structure]
        return structs
    
    def generate(self):
        



class ShortSimple(Agent):
    ''' Short length, simple structures, no changes'''
    def __init__(self, params) -> None:
        super().__init__()
        self.structures = [
            ["I", "V", "C", "V", "C", "O"],
            ["I", "V", "C", "V", "O"],
        ]
        self.s_structure = random.choice(self.structures)
        self.params = params
        self.structs = self.form_structures()


class ShortComplex(Agent):
    ''' Short length, more complex structures, no changes'''
    def __init__(self, params) -> None:
        super().__init__()
        self.structures = [
            ["I", "V", "C", "V", "C", "O"],
            ["I", "V", "V", "C", "B", "C", "O"],
            ["I", "V", "C", "V", "S", "V", "O"],
            ["I", "V", "C", "V", "B", "C", "O"],
        ]
        self.s_structure = random.choice(self.structures)
        self.params = params
        self.structs = self.form_structures()


class MediumSimplistic(Agent):
    '''Medium length, simple structures, few changes'''
    def __init__(self, params) -> None:
        super().__init__()
        self.structures = [
            ["I", "V", "C", "V", "C", "V", "C", "O"],
            ["I", "V", "V", "C", "B", "V", "V" "C", "O"],
            ["I", "V", "C", "V", "IL", "C", "V", "O"],
            ["I", "V", "C", "V", "B", "V", "C", "O"],
        ]
        self.s_structure = random.choice(self.structures)
        self.params = params
        self.structs = self.form_structures()


class MediumComplex(Agent):
    '''Medium length, complex structures, some changes'''
    def __init__(self, params) -> None:
        super().__init__()
        self.structures = [
            ["I", "V", "C", "B", "V", "C", "S", "C", "O"],
            ["I", "V", "C", "IL", "V", "C", "S" "C", "O"],
            ["I", "V", "V", "C", "IL", "V", "S", "C", "O"],
            ["I", "V", "C", "B", "V", "S", "C", "V", "C" "O"],
        ]
        self.s_structure = random.choice(self.structures)
        self.params = params
        self.structs = self.form_structures()


class LongSimplistic(Agent):
    '''Long length, somewhat simplistic structures, some changes'''
    def __init__(self, params) -> None:
        super().__init__()
        self.structures = [
            ["I", "V", "C", "V", "C", "B", "V", "C", "V", "C", "O"],
            ["I", "V", "C", "B", "V", "C", "V", "S", "V", "C", "O"],
            ["I", "V", "V", "C", "V", "B", "V", "C", "S", "C", "O"]
        ]
        self.s_structure = random.choice(self.structures)
        self.params = params
        self.structs = self.form_structures()


class LongComplex(Agent):
    ''' Long length, complex structures, multiple changes'''
    def __init__(self, params) -> None:
        super().__init__()
        self.structures = [
            ["I", "V", "C", "V", "B", "S", "V", "C", "IL", "V", "C", "O"],
            ["I", "V", "C", "V", "C", "S", "V", "B", "V", "S", "C", "O"],
            ["I", "V", "V", "C", "B", "V", "C", "S", "C", "IL", "C", "O"]
        ]
        self.s_structure = random.choice(self.structures)
        self.params = params
        self.structs = self.form_structures()

        