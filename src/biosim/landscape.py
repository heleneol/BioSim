"""
Template for Landscape class.
"""

from .general import landscape_const, getnestdict


class Lowland:

    def __init__(self, fodder=None, pop_herb=None):
        self.classname = self.__class__.__name__
        self.fodder = fodder if fodder is not None else getnestdict(landscape_const, self.classname, 'f_max')
        self.pop_herb = pop_herb if pop_herb is not None else getnestdict(Xsomelist, len(pop))
