"""
Template for Landscape class.
"""
import random

from biosim.animals import Herbivore, Carnivore


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

            elif new_params[key] < 0:
                raise ValueError('The fodder parameter must be a non-negative number')

        cls.parameters.update(new_params)

    def __init__(self, herb_pop=None, carn_pop=None):
        self.classname = self.__class__.__name__
        self.fodder = self.parameters['f_max']
        self.herb_pop = herb_pop if herb_pop is not None else []
        self.migrating_herbs = []
        self.carn_pop = carn_pop if carn_pop is not None else []
        self.migrating_carns = []
        self.habitability = True if type(self) is not Water else False

    def add_population(self, animals): # denne må revideres, ikke spørr etter species og sjekk opp bruk av append, kontra extend
        '''
        parameters
        ----------
        population: list of dicts counting animal info
        '''
        if self.habitability is True:
            for animal in animals:
                age = animal['age']
                weight = animal['weight']
                if animal['species'] == 'Herbivore':
                    self.herb_pop.append(Herbivore(age=age, weight=weight))
                elif animal['species'] == 'Carnivore':
                    self.carn_pop.append(Carnivore(age=age, weight=weight))
                else:
                    raise KeyError('Species must be either Herbivore or Carnivore')
        else:
            raise ValueError('Population cannot be placed in water')

    def get_num_herbs(self):
        """Return number of herbivores in Landscape-cell."""
        return len(self.herb_pop)

    def get_num_carns(self):
        """Return number of carnivores in Landscape-cell."""
        return len(self.carn_pop)

    def sort_herbs_by_fitness(self, decreasing):
        """Sorts the herbivore population by descending fitness."""
        self.herb_pop.sort(key=lambda animal: animal.fitness, reverse=decreasing)

    def regrowth(self):
        """Regrows fodder in Low- and Highlands."""
        self.fodder = self.parameters['f_max']

    def herbivores_eating(self):
        """Herbivores consume fodder by descending fitness."""
        self.sort_herbs_by_fitness(decreasing=True)
        for herb in self.herb_pop:
            herb.regain_appetite()
            if self.fodder > 0:
                herbivore_portion = herb.herbivore_feeding(self.fodder)
                self.fodder -= herbivore_portion
            else:
                continue

    def carnivores_eating(self):
        """Carnivores, in random order, consume herbivores."""
        random.shuffle(self.carn_pop)

        for carn in self.carn_pop:
            carn.regain_appetite()
            if len(self.herb_pop) > 0 and carn.appetite > 0:
                self.sort_herbs_by_fitness(decreasing=False)
                survivors = []

                for herb in self.herb_pop:
                    if carn.carnivore_feeding(herb) is False:
                        survivors.append(herb)
                self.herb_pop = survivors.copy()

            else:
                continue

    def reproduction(self):
        def new_pop(population):
            # noinspection PyPep8Naming
            N = len(population)
            newborns = []
            for parent in population:
                newborn = parent.gives_birth(N)
                if newborn is not None:
                    newborns.append(newborn)
            return newborns

        self.herb_pop.extend(new_pop(self.herb_pop))
        self.carn_pop.extend(new_pop(self.carn_pop))

    def animal_migration(self):
        migrators_herb = []
        migrators_carn = []
        staying_herbs = []
        staying_carns = []
        for herb in self.herb_pop:
            if herb.migrate() is True:
                migrators_herb.append(herb)
            else:
                staying_herbs.append(herb)
        self.herb_pop = staying_herbs

        for carn in self.carn_pop:
            if carn.migrate() is True:
                migrators_carn.append(carn)
            else:
                staying_carns.append(carn)
        self.carn_pop = staying_carns

        return migrators_herb, migrators_carn

    def register_for_asylum(self, migrator):
        if type(migrator) is Herbivore:
            self.migrating_herbs.append(migrator)
        elif type(migrator) is Carnivore:
            self.migrating_carns.append(migrator)
        else:
            raise ValueError('*** Intruderalarm ***')

    def add_migraters_to_pop(self):
        self.herb_pop.extend(self.migrating_herbs)
        self.migrating_herbs.clear()
        self.carn_pop.extend(self.migrating_carns)
        self.migrating_carns.clear()

    def aging(self):
        for herb in self.herb_pop:
            herb.update_age()
        for carn in self.carn_pop:
            carn.update_age()

    def weight_loss(self):
        for herb in self.herb_pop:
            herb.metabolism()
        for carn in self.carn_pop:
            carn.metabolism()

    def population_death(self):
        surviving_herbs = []
        surviving_carns = []
        for herb in self.herb_pop:
            if herb.dies() is not True:
                surviving_herbs.append(herb)
        for carn in self.carn_pop:
            if carn.dies() is not True:
                surviving_carns.append(carn)
        self.herb_pop = surviving_herbs
        self.carn_pop = surviving_carns

    def pre_migration_cycle(self):
        self.regrowth()
        self.herbivores_eating()
        self.carnivores_eating()
        self.reproduction()

    def post_migration_cycle(self):
        self.aging()
        self.weight_loss()
        self.population_death()

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
    parameters = {'f_max': 0}





'''

ini_pops = [Herbivore() for herb in range(100)]
carnivores = [Carnivore() for carn in range(5)]

l1 = Lowland(carn_pop=carnivores)

# l1.carnivores_eating()

herb_count = []
carn_count = []
for year in range(10):
    herb_sum, carn_sum = l1.annual_cycle()
    herb_count.append(herb_sum)
    carn_count.append(carn_count)
'''