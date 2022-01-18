"""
Island with complex geographie, showing syntaxt for making BioSim object.
This is an eg. on how to make a simulation with more complex and dynamics
but by reducing the demand from visualization we can get better performance.
Also shows hot to set animal parametres
"""

__author__ = 'Johannes Fjeldså'

import textwrap
from biosim.simulation import BioSim

if __name__ == '__main__':
    # geogr is a multistring object using """\....""" syntaxt
    # in this eg geogr is a more complex island with some natural barriers
    # in form of a river and a desert
    geogr = """\
               WWWWWWWWWWWWWWWWW
               WLLLLLLLLLLHHLLLW
               WLHHHHLLHHLDDDDDW
               WWLHHHWWWWHHDDDDW
               WWWHHHHWWWWHLLLHW
               WLLLLLLLLLWWWWWWW
               WWWLLLLLLHHLLHLLW
               WLLLHHHHHHHHHHHHW
               WLLLLLHLLHLHLLLLW
               WWWWWWWWWWWWWWWWW"""

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
    ini_carns = [{'loc': (6, 5),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}]

    seed = 1000000

    # with cmax_animals we can set the max value for the colorbar for the animal density maps.
    # We use species name as key and an int as value. useful to scale for different island
    # sizes in order to make the graphics exprecive.
    cmax_animals = {'Herbivore': 250,
                    'Carnivore': 200}


    # reducing the resolution (increasing 'delta') to make the hostgorams easier to plot
    hist_specs = {'fitness': {'max': 1.0, 'delta': 0.1},
                  'age': {'max': 60.0, 'delta': 8},
                  'weight': {'max': 60, 'delta': 8}}

    # image_years is set to higher value so the plot updates less frequent
    # This increases the simulation speed and demand of computer
    vis_years = 5

    # making a BioSim object with geogr as geographie, ini_herbs as the initial pop
    # img_dir tells the BioSim class where to save images and video, img_base is the base for image name
    sim = BioSim(island_map= geogr, ini_pop=ini_herbs, seed=seed,cmax_animals=cmax_animals,
                 vis_years=vis_years, hist_specs=hist_specs, img_dir='results',img_base='eg_2')

    # by setting 'F' to 30 we set how much the carnivores want to eat per year
    # 30 is lower then the default 50 so it will reduce the praying on herbivores
    sim.set_animal_parameters(species='Carnivore', params={'F': 30.0,
                                                           'beta': 0.9})
    # with the methode .simulate we run simulations
    sim.simulate(num_years=50)
    # If you want to to pause simulations simply giving sim.simulate() the numbers of years until the pause

    # we can place populations by using .place_population methode
    sim.add_population(population=ini_carns)

    # calling .simulate() again continues the simulation
    sim.simulate(num_years=150)