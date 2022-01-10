"""
Template for Landscape class.
"""
import random
from animals import Herbivore


class Landscape:
    """
    Class representing Lowland squares on the island.
    """
    random.seed(123456)

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

        self.herb_pop.sort(key=lambda animal: animal.fitness, reverse=True)

    def regrowth(self):

        self.fodder = self.parameters['f_max']

    def update_fodder(self, herbivore_portion):
        self.fodder -= herbivore_portion

    def herbs_eating(self):
        self.regrowth()
        # sorter herbivore liste
        for herb in self.herb_pop:
            if self.fodder > 0:

                herbivore_portion = herb.parameters['F']

                if 0 < self.fodder < herbivore_portion:
                    herbivore_portion = self.fodder
                self.update_fodder(herbivore_portion)
                herb.update_weight(herbivore_portion)
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

ini_pops = [Herbivore() for herb in range(100)]

l1 = Lowland(ini_pop=ini_pops)
print(len(l1.herb_pop))
l1.reproduction()
print(len(l1.herb_pop))

