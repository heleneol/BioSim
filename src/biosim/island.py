from biosim.landscape import Landscape,Lowland, Highland, Desert, Water

import textwrap
import random


class Island:
    """Class representing the entire island."""

    parameters = {'L': Lowland(),
                  'H': Highland(),
                  'D': Desert(),
                  'W': Water()}

    def __init__(self, geogr):
        self.map = self.createmap(geogr)

    def createmap(self, geogr=None):
        """
        Making the input map into a dictionary containing the location

        parameters
        -----------
        geogr: str, containing the island map

        return
        ----------
        A dict, with location in a tuple as key and landscape-type as value.

        raises
        ----------
        ValueError, is raised when habitat letter is erroneous on the map.
        """
        geogr = geogr.split(sep='\n') if geogr is not None else str
        island_map = {}
        for row, string in enumerate(geogr, start=1):
            for column, letter in enumerate(string, start=1):
                if row == 0 or row == len(geogr):
                    if letter != "W":
                        raise ValueError('Cells at the border have to be water')
                if column == 0 or column == len(string):
                    if letter != 'W':
                        raise ValueError('Cells at the border have to be water')

                if letter in self.parameters.keys():
                    key = (row, column)
                    value = type(self.parameters[letter])()
                    island_map[key] = value
                else:
                    raise ValueError('Invalid habitat type', letter)
        return island_map

    #def check_map(self, geogr=None):
    #    row_length = [len(row) for row in ]

    #    for row in :
    #        if len(row) != len(row_length[0]):
    #            raise ValueError("All rows in the map have to be of equal length")

    def place_population(self, populations):
        """
        Places a population on the map based on its stated location.

        parameters
        -----------
        populations: a list with population info

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

    def get_number_herbs(self):
        herbs_per_cell = {}
        for loc,cell in self.map.items():
            herbs_per_cell[loc] = cell.get_num_herbs()
        return herbs_per_cell
    def get_number_carns(self):
        carns_per_cell = {}
        for loc, cell in self.map.items():
            carns_per_cell[loc] = cell.get_num_carns()
        return carns_per_cell

    def island_migration(self):
        for loc, cell in self.map.items():
            if cell.classname == 'Water':
                continue
            else:
                neighbours = [self.map[(loc[0]-1, loc[1])],
                              self.map[(loc[0]+1, loc[1])],
                              self.map[(loc[0], loc[1]+1)],
                              self.map[(loc[0], loc[1]-1)]]

                migrators_herb,migrators_carn = cell.animal_migration()

                for herb in migrators_herb:
                    migration_cell = random.choice(neighbours)
                    if migration_cell.classname == 'Water':
                        cell.migrating_herbs.append(herb)
                    else:
                        migration_cell.register_for_asylum(migrator=herb)
                for carn in migrators_carn:
                    migration_cell = random.choice(neighbours)
                    if migration_cell.classname == 'Water':
                        cell.migrating_carns.append(carn)
                    else:
                        migration_cell.register_for_asylum(migrator=carn)

                for loc, cell in self.map.items():
                    if cell.classname == 'Water':
                        continue
                    else:
                        cell.add_migraters_to_pop()


geogr = """\
           WWWWW
           WLLLW
           WLLLW
           WWWWW"""


i = Island(textwrap.dedent(geogr))

#i.check_map(geogr)

ini_pop = [{'loc': (2,2),
              'pop': [{'species': 'Herbivore',
                    'age': 5,
                    'weight': 20}
                    for _ in range(50)]},
           {'loc': (2,4),
            'pop': [{'species': 'Carnivore',
                    'age': 5,
                    'weight': 20}
                    for _ in range(10)]}]


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

print_herbs_per_cell(i)
print_carns_per_cell(i)
for year in range(10):
    i.island_migration()
print_carns_per_cell(i)
print_herbs_per_cell(i)

