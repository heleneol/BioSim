"""
Small island of lowland and highland cells, showing syntaxt for making BioSim object.
showing how to save graphics to results directory. For tips on syntaxt
see eg_1.py
"""

__author__ = 'Johannes Fjeldså'

import textwrap
from biosim.simulation import BioSim

if __name__ == '__main__':


    geogr = """\
               WWWWW
               WLHLW
               WHHHW
               WLHLW
               WWWWW"""

    geogr = textwrap.dedent(geogr)


    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(10)]}]
    ini_carns = [{'loc': (4, 4),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(4)]}]

    seed = 100000

    cmax_animals = {'Carnivore': 50}

    ymax_animals = 1000

    # img_years dictate how often we are supposed to save a image from the graphics
    sim = BioSim(island_map= geogr, ini_pop=ini_herbs, seed=seed,cmax_animals=cmax_animals,
                 ymax_animals=ymax_animals, img_dir='results',img_base='eg_3')

    sim.simulate(num_years=40)
    sim.add_population(population=ini_carns)
    sim.simulate(num_years=60)

    # calling make_movie() to make movie from the saved images
    sim.make_movie()

    input('Press ENTER')