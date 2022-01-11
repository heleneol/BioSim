"""
Template for Landscape class.
"""
import random

from animals import Herbivore, Carnivore


class Landscape:
    """
    Parent class containing methods on population for different landtypes on the island.
    """

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

    def __init__(self, ini_pop=None, carn_pop =None):
        self.classname = self.__class__.__name__
        self.fodder = self.parameters['f_max'] # fodder if fodder is not None else 0
        self.herb_pop = ini_pop if ini_pop is not None else []
        self.carn_pop = carn_pop if carn_pop is not None else []

    def sort_herbs_by_fitness(self, decreasing):
        """Sorts the herbivore population by descending fitness."""

        self.herb_pop.sort(key=lambda animal: animal.fitness, reverse=decreasing)

    def regrowth(self):
        """Regrows fodder in Low- and Highlands."""

        self.fodder = self.parameters['f_max']

    def herbivores_eating(self):
        """Herbivores consume fodder."""

        for herb in self.herb_pop:
            if self.fodder > 0:
                herbivore_portion = herb.herbivore_feeding(self.fodder)
                self.fodder -= herbivore_portion
            else:
                break

    def carnivores_eating(self):
        """Carnivores consume herbivores."""

        random.shuffle(self.carn_pop)

        for carn in self.carn_pop:
            #print(f'Carn fitness {carn.fitness}')

            if len(self.herb_pop) > 0 and carn.appetite > 0:
                self.sort_herbs_by_fitness(decreasing=False)
                survivers = []
                for herb in self.herb_pop:
                    #print(f'Herbs fitness {herb.fitness}')
                    if carn.carnivore_feeding(herb) is None:
                        survivers.append(herb)
                self.herb_pop = survivers
            else:
                break

            carn.regain_appetite()

    def reproduction(self):
        def new_pop(population):
            N = len(population)
            species = population[0].classname
            newborns = []
            for parent in population:
                newborn = parent.gives_birth(N, species)

                if newborn is not None:
                    newborns.append(newborn)
            return newborns

        self.herb_pop.extend(new_pop(self.herb_pop))
        self.carn_pop.extend(new_pop(self.carn_pop))

    def aging(self):

        for herb, carn in zip(self.herb_pop, self.carn_pop):
            herb.update_age()
            carn.update_age()

    def weight_loss(self):

        for herb, carn in zip(self.herb_pop, self.carn_pop):
            herb.metabolism()
            carn.metabolism()

    def population_death(self):
        self.herb_pop = [animal for animal in self.herb_pop if animal.dies() is not True]
        self.carn_pop = [animal for animal in self.carn_pop if animal.dies() is not True]

    def annual_cycle(self):
        self.regrowth()
        #def mean_weight(population):
        #    sum = 0
        #    for animal in population:
        #        sum += animal.weight
        #    return sum/len(population)
        self.sort_herbs_by_fitness(decreasing=True)
        #print(f'gj. snitt før herb ={mean_weight(self.herb_pop)} ')
        self.herbivores_eating()
        #print(f'gj. snitt etter ={mean_weight(self.herb_pop)} ')
        #print(f'gj. snitt før carn ={mean_weight(self.carn_pop)}')
        print(f'antall dyr før spising{len(self.carn_pop)}')
        self.carnivores_eating()
        #print(f'gj. snitt etter carn ={mean_weight(self.carn_pop)}')
        print(f'antall dyr etter spising{len(self.carn_pop)}')
        #print(f'antall dyr før herb {len(self.herb_pop)}')
        #print(f'antall dyr før carn {len(self.carn_pop)}')
        self.reproduction()
        #print(f'antall dyr etter herb {len(self.herb_pop)}')
        #print(f'antall dyr etter carn {len(self.carn_pop)}')
        #print(self.carn_pop[0].age)
        self.aging()
        #print(self.carn_pop[0].age)
        #print(f'gj. snitt før ={mean_weight(self.carn_pop)} ')
        self.weight_loss()
        #print(f'gj. snitt etter ={mean_weight(self.carn_pop)} ')
        #print(f'antall dyr før {len(self.herb_pop)}')
        #print(f'antall dyr før carn {len(self.carn_pop)}')
        self.population_death()
        #print(f'antall dyr etter {len(self.herb_pop)}')
        #print(f'antall dyr etter carn {len(self.carn_pop)}')

class Lowland(Landscape):
    """
    Class representing Lowland squares on the island.
    """
    parameters = {'f_max': 800}

class Highland(Landscape):
    """
    Class representing Highland squares on the island.
    """
    parameters = {'f_max': 300}

class Desert(Landscape):
    """
    Class representing Desert squares on the island.
    """
    parameters = {'f_max': 0}

class Water(Landscape):
    """
    Class representing Ocean squares on the island.
    """

ini_pops = [Herbivore() for herb in range(100)]
carnivores = [Carnivore() for carn in range(5)]

l1 = Lowland(ini_pop=ini_pops, carn_pop=carnivores)

#l1.carnivores_eating()

for year in range(10):
    l1.annual_cycle()

