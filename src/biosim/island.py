from biosim.landscape import Landscape,Lowland, Highland, Desert, Water

import textwrap
import random

class Island:

    parametres = {'L': Lowland(),
                  'H': Highland(),
                  'D': Desert(),
                  'W': Water()}

    def __init__(self, geogr):
        self.map = self.createmap(geogr)

    def createmap(self, geogr=None):
        geogr = geogr.split(sep='\n') if geogr is not None else str
        island_map = {}
        for row, string in enumerate(geogr, start=1):
            for column, letter in enumerate(string, start=1):
                if row== 0 or row == len(geogr):
                    if letter!="W":
                        raise ValueError('Cells at the border has to water')
                if column == 0 or column == len(string):
                    if letter != 'W':
                        raise ValueError('Cells at the border has to water')
                if letter in self.parametres.keys():
                    key = (row, column)
                    value = self.parametres[letter]
                    island_map[key] = value
                else:
                    raise ValueError('Invalid habitat type', letter)
        return island_map

    def place_population(self, ini_pop):
        for indx, population in enumerate(ini_pop):
            loc = ini_pop[indx].get('loc')
            if loc in self.map.keys():
                self.map[loc].add_population(ini_pop[indx].get('pop'))
            else:
                ValueError('')

    def island_migration(self):
        for loc,cell in self.map.items():
            print(loc)
            if cell.classname == 'Water':
                continue
            else:
                neighbouring_landscaps = [self.map[(loc[0]-1,loc[1])],
                                          self.map[(loc[0]+1,loc[1])],
                                          self.map[(loc[0], loc[1]+1)],
                                          self.map[(loc[0], loc[1]-1)]]
                migraters = cell.animal_migration()
                for animal in migraters:
                    migration_cell = random.choice(neighbouring_landscaps)
                    if migration_cell.classname == 'Water':
                        print('vaaaannnn')
                        cell.herb_pop.append(animal)
                    else:
                        print('hade')
                        migration_cell.register_for_asylum(migrator=animal)

        #for location, cell in self.map.items():
         #   if cell.classname == 'Water':
         #       continue
         #   else:
        #        cell.add_migraters_to_pop()


geogr = """\
           WWWWW
           WLLLW
           WLLLW
           WWWWW"""


i = Island(textwrap.dedent(geogr))

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                    'age': 5,
                    'weight': 20}
                    for _ in range(40)]}]

i.place_population(ini_pop=ini_herbs)

i.island_migration()

