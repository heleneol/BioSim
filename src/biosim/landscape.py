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

    parametres = {'f_max': 41}

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
            if key not in cls.parametres:
                raise KeyError('Invalid parameter name: ' + key)

            elif key < 0:
                raise ValueError('The fodder parameter must be a non-negative number')

        for key in cls.parametres:
            if key in new_params:
                cls.parametres.update(new_params)


    def __init__(self, fodder=None, ini_pop=None):
        self.classname = self.__class__.__name__
        self.fodder = fodder if fodder is not None else 0
        self.herb_pop = ini_pop if ini_pop is not None else []
        #self.carn_pop = []


    def sort_by_fitness(self):

        self.herb_pop.sort(key=lambda animal: animal.fitness, reverse=True)


    def regrowth(self):

        self.fodder = self.parametres['f_max']


    def update_fodder(self, herbivore_portion):
        self.fodder -= herbivore_portion

    def herbs_eating(self):
        self.regrowth()
        #sorter herbivore liste

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
        def newborns(population):
            if len(population) >= 2:
                N = len(population)
                for animal in population:
                    zeta = animal.parameters['zeta']
                    w_birth = animal.parameters['w_birth']
                    sigma_birth = animal.parameters['sigma_birth']
                    if animal.weight > zeta*(w_birth + sigma_birth):
                        preg_prob == 0

                    else:
                        gamma = animal.parameters['gamma']
                        preg_prob = gamma * animal.fitness * (N - 1)

            else:
                preg_prob == 0

            newborns = []
            for parent in population:
                if parent.gives_birth(preg_prob):
                    xi = parent.parameters['xi']
                    newborn = Herbivore()
                    if parent.weight > xi*newborn.weight:
                        newborns.append(newborn)
                        parent.post_birth_update_weight(xi_times_newborn_weight= xi*newborn.weight)
            print(newborns)
            return newborns


        self.herb_pop.extend(newborns(self.herb_pop))


ini_pop = [Herbivore() for herb in range(100)]

l1 = Lowland(ini_pop=ini_pop)
print(len(l1.herb_pop))
l1.reproduction()
print(len(l1.herb_pop))


