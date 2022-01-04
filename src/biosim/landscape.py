"""
Template for Landscape class.
"""

from .general import animal_const, landscape_const, getnestdict

class Lowland:
    """
    Class representing Lowland squares on the island.
    """

    def __init__(self, fodder=None, pop_herb=None):
        self.classname = self.__class__.__name__
        self.fodder = fodder if fodder is not None else getnestdict(landscape_const, self.classname, 'f_max')
        # Needs revising ^
        self.herbivore_population = #Input herbivore population in a tile?

    def update_fodder(self):
        herbivore_portion = getnestdict(animal_const, 'herbivore', 'F')

        if self.fodder >= herbivore_portion:
            self.fodder -= herbivore_portion

        elif 0 < self.fodder < herbivore_portion:
            self.fodder = 0
            rest_fodder = self.fodder #? Restene av maten om det er under 10

        else:
            pass #?


    def eat_fodder(self):
        #Each herbuvore in sorted fitness list eats off available fodder and adds weight



# def regrow_fodder(self, self.year): Til senere under generell Landscape