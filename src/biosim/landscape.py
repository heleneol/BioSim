"""
Template for Landscape class.
"""
import random
from animals import Herbivore


class Lowland:
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
        ValueError
        """

        for key in new_params:
            if key not in cls.parameters:
                raise KeyError('Invalid parameter name: ' + key)

            elif key < 0:
                raise ValueError('The fodder parameter must be a non-negative number')

        for key in cls.parameters:
            if key in new_params:
                cls.parameters.update(new_params)

    def __init__(self, fodder=None, ini_pop=None):
        self.classname = self.__class__.__name__
        self.fodder = fodder if fodder is not None else 0
        self.herb_pop = ini_pop if ini_pop is not None else []
        # self.carn_pop = []

    def sort_by_fitness(self):
        """Sorts the herbivore population by descending fitness."""

        self.herb_pop.sort(key=lambda animal: animal.fitness, reverse=True)

    def regrowth(self):
        """ Regrows fodder, f max, in Low- and Highlands."""

        self.fodder = self.parameters['f_max']

    def update_fodder(self, herbivore_portion):
        """ Updates fodder available as herbivores eat."""

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
        """ Ages all animals by one year."""

        for animal in self.herb_pop:
            animal.update_age()

    def reproduction(self):
        def babies(population):
            if len(population) >= 2:
                N = len(population)
                for animal in population:
                    zeta = animal.parameters['zeta']
                    w_birth = animal.parameters['w_birth']
                    sigma_birth = animal.parameters['sigma_birth']
                    if animal.weight > zeta*(w_birth + sigma_birth):
                        preg_prob = 0

                    else:
                        gamma = animal.parameters['gamma']
                        preg_prob = gamma * animal.fitness * (N - 1)

            else:
                preg_prob = 0

            babies = [] # inn i reproduction ref?
            for parent in population:
                if parent.gives_birth(preg_prob):
                    xi = parent.parameters['xi']
                    baby = Herbivore()
                    if parent.weight > xi*baby.weight:
                        babies.append(baby)
                        parent.post_birth_update_weight(xi_times_newborn_weight= xi*baby.weight)
            print(babies)
            return babies


        self.herb_pop.extend(babies(self.herb_pop))


ini_pops = [Herbivore() for herb in range(100)]

l1 = Lowland(ini_pop=ini_pops)
print(len(l1.herb_pop))
l1.reproduction()
print(len(l1.herb_pop))

