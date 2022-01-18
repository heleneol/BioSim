"""
Island with single lowland cell, showing syntaxt for making BioSim object and how to set
visualization parametres such as:histogram specs, cmax_animals and ymax_animals.
"""

__author__ = 'Johannes Fjeldså'

import textwrap
from biosim.simulation import BioSim

if __name__ == '__main__':
    # geogr is a multistring object using """\....""" syntaxt
    geogr = """\
               WWW
               WLW
               WWW"""

    # removin whitespace in the multiline string to prepear it for the BioSim object
    geogr = textwrap.dedent(geogr)

    # sytaxt for populations:
    # a list containing dictionaries for each population. The dictionaries contain a 'loc' key
    # which should be a tuple. and a 'pop' key containing a list of dictionaries with animal
    # info: 'species', 'age' and 'weight'

    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}]
    ini_carns = [{'loc': (2, 2),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(5)]}]

    seed = 1

    # with cmax_animals we can set the max value for the colorbar for the animal density maps.
    # We use species name as key and an int as value. useful to scale for different island
    # sizes in order to make the graphics exprecive.
    cmax_animals = {'Herbivore': 300,
                    'Carnivore': 100}

    # with ymax_animals we set the max on the y-axis of the animal count,
    # useful to scale for different island sizes
    ymax_animals = 300

    # with hist_specs we can set the max value for histograms x_value with the key 'max' and
    # resulution with 'delta' key. for example to make the simulation run faster we can reduse
    # the resulution as shown bellow
    hist_specs = {'fitness': {'max': 1.0, 'delta': 0.1},
                  'age': {'max': 60.0, 'delta': 4},
                  'weight': {'max': 60, 'delta': 4}}

    # making a BioSim object with geogr as geographie, ini_herbs as the initial pop
    # img_dir tells the BioSim class where to save images and video, img_base is the base for image name
    sim = BioSim(island_map= geogr, ini_pop=ini_herbs, seed=seed,cmax_animals=cmax_animals,
                 ymax_animals=ymax_animals, hist_specs=hist_specs, img_dir='results',img_base='eg_1')

    # with the methode .simulate we run simulations
    sim.simulate(num_years=50)
    # If you want to to pause simulations simply giving sim.simulate() the numbers of years until the pause

    # we can place populations by using .place_population methode
    sim.add_population(population=ini_carns)

    # calling .simulate() again continues the simulation
    sim.simulate(num_years=50)
