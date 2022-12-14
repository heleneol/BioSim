"""
Module implementing the island itself.
"""

from biosim.landscape import Lowland, Highland, Desert, Water
from biosim.animals import Herbivore, Carnivore

import random
import numpy as np


class Island:
    """
    Class representing the entire island.
    """
    sample_animals = {'herbivore': Herbivore(),
                      'carnivore': Carnivore()}

    parameters = {'L': Lowland(),
                  'H': Highland(),
                  'D': Desert(),
                  'W': Water()}

    def __init__(self, geogr):
        r"""
        Initializing island with map made of :class:`landscape.Landscape` subclasses.

        :param geogr: Multi-line string specifying island geography
        :type geogr: str

        Example
        -------
        ::

            geographie =   \
                            WWW
                            WLW
                            WWW
            island  = Island(geogr = geographie)

            note: geographie str must be inside tripple bracketes
            -----
        """
        self.map = self.createmap(geogr)

    def createmap(self, geogr=None):
        """
        Making the given map into a dictionary with location as keys
        and landscape-objects as value.
        The given map must have a rectangular-shape,
        and all border cells have to be water.
        All cells have to indicate a landscape-subclass of:

         * L - Lowland
         * H - Highland
         * D - Desert
         * W - Water

        :param geogr: Multi-line string specifying island geography
        :type geogr: str

        :return: dictionary of island map.
        :rtype: dict

        """
        geogr = geogr.split(sep='\n') if geogr is not None else str

        unique_row_lenghts = {len(row) for row in geogr}
        if len(unique_row_lenghts) != 1:
            raise ValueError('The map has to be a rectangular shape! \n'
                             'All rows do not contain the same amount of letters')

        island_map = {}
        for row, string in enumerate(geogr, start=1):
            for column, letter in enumerate(string, start=1):
                if row == 1 or row == len(geogr):
                    if letter != 'W':
                        raise ValueError('Cells at the border have to be water!')
                if column == 1 or column == len(string):
                    if letter != 'W':
                        raise ValueError('Cells at the border have to be water!')

                if letter in self.parameters.keys():
                    loc = (row, column)
                    landscape = type(self.parameters[letter])()
                    island_map[loc] = landscape
                else:
                    if letter == ' ':
                        raise ValueError(f'There is a hole in the map at loc: {(row,column)}.\n'
                                         f'Fill it with a valid habitat type:\n'
                                         f'* L - Lowland\n'
                                         f'* H - Highland\n'
                                         f'* D - Desert\n'
                                         f'* W - Water')
                    else:
                        raise ValueError(f'The {letter} is an Invalid habitat type, change to:\n'
                                         f'* L - Lowland\n'
                                         f'* H - Highland\n'
                                         f'* D - Desert\n'
                                         f'* W - Water')
        return island_map

    def place_population(self, populations):
        """
        Places a population on the map based on its stated location.
        The location has to be within the given map-geography.

        :param populations: A list containing dictionaries with
                            population location and animal information.
        :type populations: list

        Example
        -------
        ::

            herbivores = [{'loc': (2, 2),
                           'pop': [{'species': 'Herbivore',
                                    'age': 5,
                                    'weight': 20}
                                    for _ in range(200)]}]

            Island().place_population(herbivores)

        """
        for population in populations:
            loc = population['loc']
            if loc in self.map.keys():
                cell = self.map[loc]
                cell.add_population(population['pop'])
            else:
                raise ValueError(f'The stated location {loc} is outside the map boundaries')

    def set_animal_parameters_island(self, species, params):
        """
        Setting animal parameters.

        :param species: specifying which species to set the parameters for
        :param params: new parameters to set for the species.

        """
        species = self.sample_animals[species.lower()]
        species.set_parameters(new_params=params)

    def set_landscape_parameters_island(self, landscape, params):
        """
        Setting landscape parameters.

        :param landscape: specifying which subclass
                          of :class:`landscape.Landscape` to set the parameters for
        :param params: new parameters to set for the landscape.
        """
        landscape = self.parameters[landscape]
        landscape.set_parameters(new_params=params)

    def get_number_of_herbs(self):
        """
        Calculates the number of herbivores in total on the island.

        :return: number of herbivores on the island.
        :rtype: int

        """
        herb_count = 0

        for cell in self.map.values():
            herb_count += cell.get_num_herbs()

        return herb_count

    def get_number_of_carns(self):
        """
        Calculates the number of carnivores in total on the island.

        :return: number of carnivores on the island.
        :rtype: int
        """
        carn_count = 0

        for cell in self.map.values():
            carn_count += cell.get_num_carns()

        return carn_count

    def get_number_herbs_per_cell(self):
        """
        Calculates the number of herbivores per cell on the map.

        :return: 2D-array with herbivorecount per cell as values
        :rtype: array

        """

        map_dim = list(self.map.keys())[-1]
        herb_matrix = np.zeros(map_dim)
        for loc, cell in self.map.items():
            herb_matrix[loc[0]-1][loc[1]-1] = cell.get_num_herbs()
        return herb_matrix

    def get_number_carns_per_cell(self):
        """
        Calculates the number of carnivores per cell on the map.

        :return: 2D-array with carnivorecount per cell as values
        :rtype: array

        """
        map_dim = list(self.map.keys())[-1]
        carn_matrix = np.zeros(map_dim)
        for loc, cell in self.map.items():
            carn_matrix[loc[0] - 1][loc[1] - 1] = cell.get_num_carns()
        return carn_matrix

    def get_herbs_fitness(self):
        """
        Makes list of alle the fitnessvalues for the islands herbivore population

        :return: list with values for fitness
        :rtype: list
        """
        herbivores_fitness = []
        for cell in self.map.values():
            for herb in cell.herb_pop:
                herbivores_fitness.append(herb.fitness)
        return herbivores_fitness

    def get_carns_fitness(self):
        """
        Makes list of all the fitnessvalues for the islands carnivore population

        :return: list with values for fitness
        :rtype: list
        """
        carnivores_fitness = []
        for cell in self.map.values():
            for carn in cell.carn_pop:
                carnivores_fitness.append(carn.fitness)
        return carnivores_fitness

    def get_herbs_age(self):
        """
        Makes list of all the age-values for the islands herbivore population

        :return: list with values for age
        :rtype: list
        """
        herbivores_age = []
        for cell in self.map.values():
            for herb in cell.herb_pop:
                herbivores_age.append(herb.age)
        return herbivores_age

    def get_carns_age(self):
        """
        Makes list of all the age-values for the islands carnivore population

        :return: list with values for age
        :rtype: list
        """
        carnivores_age = []
        for cell in self.map.values():
            for carn in cell.carn_pop:
                carnivores_age.append(carn.age)
        return carnivores_age

    def get_herbs_weight(self):
        """
        Makes list of all the weight-values for the islands herbivore population

        :return: list with values for weight
        :rtype: list
        """
        herbivores_weight = []
        for cell in self.map.values():
            for herb in cell.herb_pop:
                herbivores_weight.append(herb.weight)
        return herbivores_weight

    def get_carns_weight(self):
        """
        Makes list of all the weight-values for the islands carnivore population

        :return: list with values for weight
        :rtype: list
        """
        carnivores_weight = []
        for cell in self.map.values():
            for carn in cell.carn_pop:
                carnivores_weight.append(carn.weight)
        return carnivores_weight

    def island_migration(self):
        """
        Function for implementing migration for all animals on the island.

        Gets neighbouring cells and chooses one at random :math:`p = \frac{1}{4}`
        for the animal to emigrate to.
        If the chosen cell is :class:`lanscape.Water`, the animal stays put,
        else it is registered to the chosen
        cells migrant population. Lastly, it adds the migrators to
        their cell's population.

        """
        for loc, cell in self.map.items():
            if cell.classname == 'Water':
                continue
            else:
                neighbours = [self.map[(loc[0]-1, loc[1])],
                              self.map[(loc[0]+1, loc[1])],
                              self.map[(loc[0], loc[1]+1)],
                              self.map[(loc[0], loc[1]-1)]]

                migrators_herb, migrators_carn = cell.animal_migration()

                for herb in migrators_herb:
                    migration_cell = random.choice(neighbours)
                    if migration_cell.classname == 'Water':
                        cell.migrating_herbs.append(herb)
                    else:
                        migration_cell.register_migrants(migrator=herb)

                for carn in migrators_carn:
                    migration_cell = random.choice(neighbours)
                    if migration_cell.classname == 'Water':
                        cell.migrating_carns.append(carn)
                    else:
                        migration_cell.register_migrants(migrator=carn)

        for loc, cell in self.map.items():
            if cell.classname == 'Water':
                continue
            else:
                cell.add_migraters_to_pop()

    def annual_cycle_island(self):
        """
        Method running the annual cycle of the ecosystem on the island.
        In pre migration all cells regrow fodder,
        herbivores eat, carnivores eat and the breeding season plays out.
        Then the migrating animals migrate.
        Lastly, in post migration the animals age, lose weight and some die.
        """
        for cell in self.map.values():
            cell.pre_migration_cycle()

        self.island_migration()

        for cell in self.map.values():
            cell.post_migration_cycle()

    def _clean_island_for_herbs(self):
        """
        Help function for test_island_migration_happens_once in test_island.py
        """
        for cell in self.map.values():
            cell.herb_pop.clear()
