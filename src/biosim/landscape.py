"""
Module implementing the landscape on the island, using the Landscape superclass.
"""
import random

from biosim.animals import Herbivore, Carnivore


class Landscape:
    """
    Superclass containing methods on population for different landscapes on the island.

    Subclasses:
    * Lowland
    * Highland
    * Desert
    * Water
    """

    @classmethod
    def set_parameters(cls, new_params):
        """
        set class parameters.

        :param new_params: new parameter values.
        :type new_params: dict
        """
        #if cls.classname is Desert or cls.classname is Water:
        #    raise AttributeError(f'Fodder amount can only be changed in Highland or Lowland!')

        for key in new_params:
            if key not in cls.parameters:
                raise KeyError(f'Invalid parameter name: {key}')

            elif new_params[key] < 0:
                raise ValueError('The fodder parameter must be a non-negative number')

        cls.parameters.update(new_params)

    def __init__(self, herb_pop=None, carn_pop=None):
        """
        Initializing Landscape objects.

        :param herb_pop: list containing the herbivore population
        :type herb_pop: list
        :param carn_pop: list containing the carnivore population
        :type carn_pop: list
        """
        self.classname = self.__class__.__name__

        self.fodder = self.parameters['f_max']
        self.herb_pop = herb_pop if herb_pop is not None else []
        self.migrating_herbs = []
        self.carn_pop = carn_pop if carn_pop is not None else []
        self.migrating_carns = []
        self.habitability = True if type(self) is not Water else False

    def add_population(self, animals): # denne må revideres, ikke spørr etter species og sjekk opp bruk av append, kontra extend
        """
        Adding population to landscape. Animals are added to either the herbivore or carnivore population based on the
        given information.

        :param animals: list containing dictionaries with animal information about species, age and weight.
        :type animals: list
        """
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
        """
        Return number of herbivores in Landscape.

        :return: the number of herbivores
        :rtype: int
        """
        return len(self.herb_pop)

    def get_num_carns(self):
        """
        Return number of carnivores in Landscape.

        :return: the number of carnivores
        :rtype: int
        """
        return len(self.carn_pop)

    def sort_herbs_by_fitness(self, decreasing):
        """
        Sorts the herbivore population by fitness.

        :param decreasing: If True, herbivores are sorted by decreasing fitness. If False, they are sorted by
        increasing fitness.
        :type decreasing: bool
        """
        if type(decreasing) is bool:
            self.herb_pop.sort(key=lambda animal: animal.fitness, reverse=decreasing)
        else:
            raise ValueError(f'Decreasing has to be a bool! Not a {type(decreasing)}')

    def regrowth(self):
        """Regrows fodder to f_max in Low- and Highlands."""
        self.fodder = self.parameters['f_max']

    def herbivores_eating(self):
        """
        Herbivores consume fodder by descending fitness. Landscape fodder is updated for each portion consumed by a
        herbivore. Feeding stops when there is no more fodder.
        """
        self.sort_herbs_by_fitness(decreasing=True)
        for herb in self.herb_pop:
            herb.regain_appetite()
            if self.fodder > 0:
                herbivore_portion = herb.herbivore_feeding(self.fodder)
                self.fodder -= herbivore_portion
            else:
                break

    def carnivores_eating(self):
        """
        Carnivores, in random order, consume herbivores. The carnivore tries to kill one herbivore at a time, beginning
        with the herbivore with lowest fitness. A carnivore tries to kill until it has attempted to kill each herbivore
        in the cell or it no longer has an appetite.
        """
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
        """
        Function for reproduction in a population. It extends the populations with a list of newborns.
        """
        def newborn_pop(population):
            """
            Generates a list of newborn animal objects based on whether animals in the population get an offspring
            or not.

            :param population: A list of animal objects.
            :type population: list

            :return: list of newborn animal objects.
            :rtype: list
            """
            # noinspection PyPep8Naming
            pop_size = len(population)
            newborns = []
            for parent in population:
                newborn = parent.gives_birth(pop_size)
                if newborn is not False:
                    newborns.append(newborn)
            return newborns

        self.herb_pop.extend(newborn_pop(self.herb_pop))
        self.carn_pop.extend(newborn_pop(self.carn_pop))

    def animal_migration(self):
        """
        The function returns lists of animals that wish to migrate, and updates the landscapes population to animals
        that are staying put.

        :return: Lists of herbivores and carnivores wishing to migrate.
        :rtype: list
        """
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

    def register_migrants(self, migrator):
        """
        Appends animal that is migrating to a list of immigrating animals.

        :param migrator: Animal that is migrating.
        :type migrator: object
        """
        if type(migrator) is Herbivore:
            self.migrating_herbs.append(migrator)
        elif type(migrator) is Carnivore:
            self.migrating_carns.append(migrator)
        else:
            raise ValueError('*** Intruderalarm ***')

    def add_migraters_to_pop(self):
        """
        Adding migrators to the landscape population. Clears the lists of immigrating animals.
        """
        self.herb_pop.extend(self.migrating_herbs)
        self.migrating_herbs.clear()
        self.carn_pop.extend(self.migrating_carns)
        self.migrating_carns.clear()

    def aging(self):
        """
        Aging the population.
        """
        for herb in self.herb_pop:
            herb.update_age()
        for carn in self.carn_pop:
            carn.update_age()

    def weight_loss(self):
        """
        Updates animal weight, due to annual weightloss, for the population.
        """
        for herb in self.herb_pop:
            herb.metabolism()
        for carn in self.carn_pop:
            carn.metabolism()

    def population_death(self):
        """
        Updates the population due to annual death amongst animals.
        """
        surviving_herbs = []
        surviving_carns = []
        for herb in self.herb_pop:
            if herb.dies() is not True:
                surviving_herbs.append(herb)
        for carn in self.carn_pop:
            if carn.dies() is not True:
                surviving_carns.append(carn)
        self.herb_pop = surviving_herbs  # .copy() ??
        self.carn_pop = surviving_carns

    def pre_migration_cycle(self):
        """
        Runs annual cycle up to migration.
        """
        self.regrowth()
        self.herbivores_eating()
        self.carnivores_eating()
        self.reproduction()

    def post_migration_cycle(self):
        """
        Runs annual cycle after migration.
        """
        self.aging()
        self.weight_loss()
        self.population_death()

class Lowland(Landscape):
    """
    Subclass representing Lowland landscape on the island.
    """

    parameters = {'f_max': 800}


class Highland(Landscape):
    """
    Subclass representing Highland landscape on the island.
    """
    parameters = {'f_max': 300}


class Desert(Landscape):
    """
    Subclass representing Desert landscape on the island.
    """
    parameters = {'f_max': 0}

class Water(Landscape):
    """
    Subclass representing Ocean landscape on the island.
    """
    parameters = {'f_max': 0}

ini_pops = [Herbivore() for herb in range(100)]
carnivores = [Carnivore() for carn in range(5)]

l1 = Lowland(herb_pop=ini_pops)

for herb in ini_pops:
    l1.register_migrants(herb)



# l1.carnivores_eating()
'''
herb_count = []
carn_count = []
for year in range(10):
    herb_sum, carn_sum = l1.annual_cycle()
    herb_count.append(herb_sum)
    carn_count.append(carn_count)
'''