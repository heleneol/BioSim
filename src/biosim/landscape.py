"""
Template for Landscape class.
"""

from .animals import *

class Lowland:
    """
    Class representing Lowland squares on the island.
    """

    fodder_param = {'Lowland': {'f_max': 800},
                    'Highland': {'f_max': 300},
                    'Desert': {'f_max': 0},
                    'F': 10.0} #??

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
            if key not in cls.fodder_param:
                raise KeyError('Invalid parameter name: ' + key)

            elif key < 0:
                raise ValueError('The fodder parameter must be a non-negative number')

        for key in cls.fodder_param:
            if key in new_params:
                cls.fodder_param.update(new_params)


    def __init__(self, fodder=None, ini_pop=None):
        self.classname = self.__class__.__name__
        self.fodder = fodder if fodder is not None else self.regrowth()
        self.herb_pop = ini_pop if ini_pop is not None else []
        #self.carn_pop = []


    def sort_by_fitness(self, herb_pop):

        self.herb_pop.sort(key=lambda animal: animal.fitness, reverse=True)


    def regrowth(self):

        self.fodder = self.fodder_param['classname']['f_max']


    def update_fodder(self, herbivore_portion):
        self.fodder -= herbivore_portion

    def herbs_eating(self):
        self.regrowth()
        #sorter herbivore liste

        for herb in self.herb_pop:

            while self.fodder > 0:

                herbivore_portion = herb.parameters['F']

                if 0 < self.fodder < herbivore_portion:
                    herbivore_portion = self.fodder


                self.update_fodder(herbivore_portion)
                herb.update_weight(herbivore_portion)


    def aging(self):

        for animal in self.herbi_pop:
            animal.update_age()


    def reproduction(self):
        def newborns(population):
            if len(population) >= 2:
                N = len(population)
                for animal in population:
                    zeta = animal.parameters['zeta']
                    w_birth = animal.parameters['w_birth']
                    sigma_birth = animal.parameters['sigma_birth']
                    if animal.weight < zeta*(w_birth + sigma_birth):
                        birth_prob = 0
                    else:
                        gamma = animal.parameters['gamma']
                        birth_prob = gamma * animal.fitness * (N - 1)

            return [Animal() for parent in population if parent.gives_birth(birth_prob)]

        self.population.extend(newborns(self.population))