"""
Template for Landscape class.
"""

from .general import animal_const, landscape_const, getnestdict
from .animal import

class Lowland:
    """
    Class representing Lowland squares on the island.
    """

    def __init__(self, fodder=None, pop_herb=None):
        self.classname = self.__class__.__name__
        self.fodder = fodder if fodder is not None else getnestdict(landscape_const, self.classname, 'f_max')

    def update_fodder(self):
        herbivore_portion = getnestdict(animal_const, 'herbivore', 'F')
        self.fodder = self.fodder - herbivore_portion

# def regrow_fodder(self, self.year): Til senere under generell Landscape