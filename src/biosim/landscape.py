"""
Template for Landscape class.
"""
import random
from animals import Herbivore


class Landscape:
    """
    Class representing Lowland squares on the island.
    """


    parameters = {'f_max': 41}

    @classmethod
    def set_parameters(cls, new_params):
        """
        set class parameters.

        Parameters
        ________
        new_params: dict

        Raises
        ________
        KeyError
        ValueError
        """

        for key in new_params:
            if key not in cls.parameters:
                raise KeyError('Invalid parameter name: ' + key)

            elif key < 0:
                raise ValueError('The fodder parameter must be a non-negative number')

        cls.parameters.update(new_params)

    def __init__(self, ini_pop=None):
        self.classname = self.__class__.__name__
        self.fodder = self.parameters['f_max'] # fodder if fodder is not None else 0
        self.herb_pop = ini_pop if ini_pop is not None else []
        # self.carn_pop = []

    def sort_by_fitness(self):
        """Sorts the herbivore population by descending fitness."""

        self.herb_pop.sort(key=lambda animal: animal.fitness, reverse=True)

    def regrowth(self):
        """Regrows fodder in Low- and Highlands."""

        self.fodder = self.parameters['f_max']

    def herbs_eating(self):
        """Herbivores consume fodder."""

        for herb in self.herb_pop:
            if self.fodder > 0:
                herbivore_portion = herb.herbivore_feeding(self.fodder)
                self.fodder -= herbivore_portion
            else:
                break

    def aging(self):

        for animal in self.herb_pop:
            animal.update_age()

    def reproduction(self):
        def new_pop(population):
            N = len(population)
            newborns = []
            for parent in population:
                newborn = parent.gives_birth(N)

                if newborn is not None:
                    newborns.append(newborn)
            print(newborns)
            return newborns

        self.herb_pop.extend(new_pop(self.herb_pop))


class Lowland(Landscape):
    parameters = {'f_max': 41}

ini_pops = [Herbivore() for herb in range(6)]

l1 = Lowland(ini_pop=ini_pops)
l1.sort_by_fitness()

for herb in l1.herb_pop:
    print(herb.weight)

l1.herbs_eating()

for herb in l1.herb_pop:
    print(herb.weight)






