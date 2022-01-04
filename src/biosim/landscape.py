"""
Template for Landscape class.
"""

from general import landscape_const
from general import getnestdict


class Lowland:

    def __init__(self, fodder=None, pop=None):
        self.classname = self.__class__.__name__
        self.fodder = fodder if fodder is not None else getnestdict(landscape_const, self.classname, 'f_max')
        self.pop = pop if pop is not None else getnestdict(placement, len('pop'))

