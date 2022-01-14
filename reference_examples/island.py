from src.biosim.landscape import Lowland, Highland, Desert, Water
from src.biosim.landscape import Herbivore
import textwrap

class Island:

    parametres = {'L': Lowland(),
                  'H': Highland(),
                  'D': Desert(),
                  'W': Water()}

    def __init__(self, geogr ):
        self.createmap(geogr)

    def createmap(self, geogr = None):
        geogr = geogr.split(sep='\n') if geogr is not None else str
        map = {}
        for row, string in enumerate(geogr, start=1):
            for column, letter in enumerate(string, start=1):
                if letter in self.parametres.keys():
                    key = (row, column)
                    value = self.parametres[letter]
                    map[key] = value
                else:
                    raise ValueError('Invalid habitat type', letter)
        self.map = map

    def place_population(self, ini_pop):
        for indx, population in enumerate(ini_pop):
            loc = ini_pop[indx].get('loc')
            if loc in self.map.keys():
                self.map[loc].add_population(ini_pop[indx].get('pop'))

    def island_migration(self):

        for location in self.map:
            neighbouring_landscaps = {'north':,
                                      'south':,
                                      'east':,
                                      'west':}
            location.animal_migration(neighbouring_landscaps)


geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)

i = Island(geogr)

ini_herbs = [{'loc': (2, 2),
              'pop': [{ 'species': 'Herbivore',
                        'age': 5,
                        'weight': 20}
                        for _ in range(2)]}]

i.place_population(ini_pop=ini_herbs)
print(i.map[(2, 2)].herb_pop)
i.anual_cycle()
