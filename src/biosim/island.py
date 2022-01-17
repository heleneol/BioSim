"""
Module implementing the island itself.
"""

from biosim.landscape import Lowland, Highland, Desert, Water
from biosim.animals import Herbivore, Carnivore

import textwrap
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
        """
        Initializing island.

        :param geogr: Multi-line string specifying island geography
        :type geogr: str
        """
        self.map = self.createmap(geogr)

    def createmap(self, geogr=None):
        """
        Making the given map into a dictionary with location as keys and landscape-objects as value. The given map
        must have a rectangular-shape, and all border cells have to be water. All cells have to indicate a
        landscape-subclass of:
         * L - Lowland
         * H - Highland
         * D - Desert
         * W - Water

        :param geogr: Multi-line string specifying island geography
        :type geogr: str

        :return: dictionary of island map.
        :rtype: dict

        raises
        ----------
        ValueError, is raised when habitat letter is erroneous on the map.
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
                        raise ValueError(f'There is a hole in the map at loc: {(row,column)}. Fill it with a valid habitat type:\n'
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
        Places a population on the map based on its stated location. The location has to be within the given
        map-geography.

        :param populations: A list containing dictionaries with population location and animal information.
        :type populations: list

        raises
        -----------
        ValueError: if the location is not included in the map's keys
        """
        for population in populations:
            loc = population['loc']
            if loc in self.map.keys():
                cell = self.map[loc]
                cell.add_population(population['pop'])
            else:
                raise ValueError(f'The stated location {loc} is outside the map boundaries')

    def set_animal_parameters_island(self, species, params):
        species = self.sample_animals[species.lower()]
        species.set_parameters(new_params=params)

    def set_landscape_parameters_island(self, landscape, params):
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
        Calculates the number of carnviores in total on the island.

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
        :rtype:
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
        :rtype:
        """
        map_dim = list(self.map.keys())[-1]
        carn_matrix = np.zeros(map_dim)
        for loc, cell in self.map.items():
            carn_matrix[loc[0] - 1][loc[1] - 1] = cell.get_num_carns()
        return carn_matrix

    def get_herbs_fitness(self):
        herbivores_fitness = [[herb.fitness for herb in cell.herb_pop] for cell in self.map.values()]
        return sorted(herbivores_fitness)

    def get_carns_fitness(self):
        carnivores_fitness = [[carn.fitness for carn in cell.carn_pop] for cell in self.map.values()]
        return sorted(carnivores_fitness)

    def get_herbs_age(self):
        herbivores_age = [[herb.age for herb in cell.herb_pop] for cell in self.map.values()]
        return sorted(herbivores_age)

    def get_carns_age(self):
        carnivores_age = [[carn.age for carn in cell.carn_pop] for cell in self.map.values()]
        return sorted(carnivores_age)

    def get_herbs_weight(self):
        herbivores_weight = [[herb.weight for herb in cell.herb_pop] for cell in self.map.values()]
        return sorted(herbivores_weight)

    def get_carns_weight(self):
        carnivores_weight = [[carn.weight for carn in cell.carn_pop] for cell in self.map.values()]
        return sorted(carnivores_weight)

    def island_migration(self):
        """
        X?

        Gets neighbouring cells and chooses one at random for the animal to emigrate to. If the chosen cell is water,
        the animal stays put, else it is registered to the chosen cells migrant population. Lastly, it adds
        the migrators to their cell's population.
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
        Method running the annual cycle of the ecosystem on the island. In pre migration all cells regrow fodder,
        herbivores eat, carnivores eat and the breeding season plays out. Then the migrating animals migrate.
        Lastly, in post migration the animals age, lose weight and some die.
        """
        for cell in self.map.values():
            cell.pre_migration_cycle()

        self.island_migration()

        for cell in self.map.values():
            cell.post_migration_cycle()


geogr = """\
           WWWWWWWWW
           WLLLWHHHW
           WHLHHHLLW
           WHLLLDDDW
           WLLLWDDDW
           WWWWWWWWW"""


i = Island(textwrap.dedent(geogr))

'''
#i.check_map(geogr)

ini_pop = [{'loc': (2,2),
              'pop': [{'species': 'Herbivore',
                    'age': 5,
                    'weight': 20}
                    for _ in range(50)]}]


i.place_population(populations=ini_pop)
def print_herbs_per_cell(i):
    print('HERBIVORES')
    print('----------')
    herbs_per_cell = i.get_number_herbs()
    for loc, count in herbs_per_cell.items():
        print(loc, ':', count)

def print_carns_per_cell(i):
    print('CARNIVORES')
    print('----------')
    carns_per_cell = i.get_number_carns()
    for loc, count in carns_per_cell.items():
        print(loc, ':', count)
''''''
for indx,year in enumerate(range(30), start=1):

    print(f'Begining of year {indx}')
    print('****************')
    print_herbs_per_cell(i)
    #print_carns_per_cell(i)

    i.pre_migration_anual_cycle()

    print('Pre migration')
    print('*************')

    print_herbs_per_cell(i)
    #print_carns_per_cell(i)

    i.island_migration()

    print('Post migration')
    print('*************')
    print_herbs_per_cell(i)
    #print_carns_per_cell(i)

    i.post_migration_anual_cycle()

    print('End of year')
    print('*************')
    print_herbs_per_cell(i)
    #print_carns_per_cell(i)
'''