from src.biosim.island import Island

import textwrap
import pytest
import numpy as np


ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(2)]}]

geography = """\
                WWWWWWWWWWW
                WLLLHHHLLLW
                WLLLLLLLLLW
                WLDDDDLLDDW
                WLLLLLLLLLW
                WWWWWWWWWWW"""
geography = textwrap.dedent(geography)


def test_creatmap():
    """
    Tests if an Island is initialized and has the attribute self.map. With an empty geogr the len is zero
    """
    geogr = """\
                WWWWWWWWWWW
                WLLLHHHLLLW
                WLLLLLLLLLW
                WLDDDDLLDDW
                WLLLLLLLLLW
                WWWWWWWWWWW"""

    geogr = textwrap.dedent(geogr)
    i = Island(geogr)
    assert len(i.map) > 0


def test_non_rectangular_shape():
    """
    Tests what happens if the island geography is non-rectangular
    """
    geogr = """\
                WWWW
                WLW
                WWW"""
    geogr = textwrap.dedent(geogr)
    with pytest.raises(ValueError, match='The map has to be a rectangular shape! \n'
                       'All rows do not contain the same amount of letters'):
        Island(geogr)


def test_no_water_at_boarder():
    """
    Tests if the ValueError is raised if a non-water landscape at the border of the map
    """
    geogr = """\
                DWW
                WLW
                WWW"""
    geogr = textwrap.dedent(geogr)
    with pytest.raises(ValueError, match='Cells at the border have to be water!'):
        Island(geogr)


def test_hole_in_the_map():
    """
    Test if the ValueError is raised if there is a hole in the map
    """
    geogr = """\
                WWW
                W W
                WWW"""
    geogr = textwrap.dedent(geogr)
    with pytest.raises(ValueError):
        Island(geogr)


def test_invalid_habitat_on_map():
    """
    Test if the ValueError is raised if there is an invalid habitat-letter in the map.
    The only valid habitat letters are W, D, H, L.
    """
    geogr = """\
                WWW
                WdW
                WWW"""
    geogr = textwrap.dedent(geogr)
    with pytest.raises(ValueError):
        Island(geogr)


def test_placing_population():
    """
    Test if ValueError is raised when a population is placed outside of the map.
    Also tests if a population is placed in lowland, and not in water.
    """
    populations = [{'loc': (2, 2),
                    'pop': [{'species': 'Herbivore',
                            'age': 5,
                             'weight': 20}
                            for _ in range(200)]},
                   {'loc': (3, 4),
                    'pop': [{'species': 'Carnivore',
                            'age': 3,
                             'weight': 20}
                            for _ in range(30)]}]
    geogr = """\
                    WWW
                    WLW
                    WWW"""
    geogr = textwrap.dedent(geogr)
    i = Island(geogr)

    with pytest.raises(ValueError):
        i.place_population(populations=populations)

    assert len(i.map[(2, 2)].herb_pop) == 200


def test_place_population_in_water():
    """
    Test that placing a population in water gives a ValueError.
    """
    geogr = """\
                WWW
                WLW
                WWW"""
    geogr = textwrap.dedent(geogr)
    i = Island(geogr)
    populations = [{'loc': (1, 2),
                    'pop': [{'species': 'Herbivore',
                             'age': 5,
                             'weight': 20}
                            for _ in range(200)]}]
    with pytest.raises(ValueError):
        i.place_population(populations)


def test_set_animal_parameters():
    """
    Testing it is possible to set parameters for animals.
    """
    beta = 0.85
    omega = 0.6
    i = Island(geography)
    i.set_animal_parameters_island('Herbivore', {'beta': beta, 'omega': omega})

    assert i.sample_animals['herbivore']
    assert i.sample_animals['herbivore'].parameters['beta'] == beta
    assert i.sample_animals['herbivore'].parameters['omega'] == omega


def test_set_landscape_parameters():
    """
    Testing it is possible to set parameters for the landscape.
    """
    fodder = 700
    i = Island(geography)
    i.set_landscape_parameters_island('L', {'f_max': fodder})

    assert i.parameters['L']
    assert i.parameters['L'].parameters['f_max'] == fodder


def test_set_desert_parameters():
    """
    Testing AttributeError when trying to change f_max for Desert-landscape
    """


def test_get_num_herbs():
    """
    Testing that the function get_num_herbs() returns the total amount of herbivores placed on the island.
    """
    num = 3
    number = 10

    ini_herbies = [{'loc': (2, 2),
                    'pop': [{'species': 'Herbivore',
                            'age': 5,
                             'weight': 20}
                            for _ in range(num)]},
                   {'loc': (3, 3),
                    'pop': [{'species': 'Herbivore',
                            'age': 3,
                             'weight': 20}
                            for _ in range(number)]}]

    i = Island(geography)
    i.place_population(ini_herbies)

    assert i.get_number_of_herbs() == num + number


def test_get_num_carnivores():
    """
    Testing that the function get_num_carns() returns the total amount of carnivores placed on the island.
    """
    num = 5
    number = 4

    ini_carnies = [{'loc': (2, 5),
                    'pop': [{'species': 'Carnivore',
                            'age': 2,
                             'weight': 10}
                            for _ in range(num)]},
                   {'loc': (3, 4),
                    'pop': [{'species': 'Carnivore',
                            'age': 5,
                             'weight': 30}
                            for _ in range(number)]}]

    i = Island(geography)
    i.place_population(ini_carnies)

    assert i.get_number_of_carns() == num + number


def test_get_number_herbs_per_cell():
    """
    Testing that the function get_number_herbs_per_cell() returns the amount of herbivores in each cell on the island.
    """
    num = 4
    number = 5

    ini_herbies = [{'loc': (2, 2),
                    'pop': [{'species': 'Herbivore',
                            'age': 5,
                             'weight': 20}
                            for _ in range(num)]},
                   {'loc': (3, 3),
                    'pop': [{'species': 'Herbivore',
                            'age': 3,
                             'weight': 20}
                            for _ in range(number)]}]

    i = Island(geography)
    i.place_population(ini_herbies)

    #assert np.any(i.get_number_herbs_per_cell()) == num


def test_get_number_carns_per_cell():
    """
    Testing that the function get_number_carns_per_cell() returns the amount of carnivores in each cell on the island.
    """


def test_gives_herbs_fitness():
    """
    Testing if get_herbs_fitness indeed returns a list of all the herbivores fitness.
    """
    i = Island(geography)
    num = 9
    number = 10
    ini_herbies = [{'loc': (2, 5),
                    'pop': [{'species': 'Herbivore',
                             'age': 2,
                             'weight': 10}
                            for _ in range(num)]},
                   {'loc': (2, 2),
                    'pop': [{'species': 'Herbivore',
                             'age': 2,
                             'weight': 10}
                            for _ in range(number)]},
                   ]
    before = len(i.get_herbs_fitness())
    i.place_population(ini_herbies)
    after = len(i.get_herbs_fitness())

    assert before < after
    assert after == num + number


def test_gives_carns_fitness():
    """
    Testing if get_carns_fitness indeed returns a list of all the carnivores fitness.
    """
    i = Island(geography)
    num = 5
    number = 4
    ini_carnies = [{'loc': (2, 5),
                    'pop': [{'species': 'Carnivore',
                             'age': 2,
                             'weight': 10}
                            for _ in range(num)]},
                   {'loc': (2, 2),
                    'pop': [{'species': 'Carnivore',
                             'age': 2,
                             'weight': 10}
                            for _ in range(number)]},
                   ]
    before = len(i.get_carns_fitness())
    i.place_population(ini_carnies)
    after = len(i.get_carns_fitness())

    assert before < after
    assert after == num + number


def test_get_herbs_age():
    """
    Testing if get_herbs_age indeed returns the Herbivore's true age.
    """


def test_get_carns_age():
    """
    Testing if get_carns_age indeed returns the Carnivore's true age.
    """


def test_get_herbs_weight():
    """
    Testing if get_herbs_weight indeed returns the Herbivore's true weight.
    """


def test_get_carns_weight():
    """
    Testing if get_carns_weight indeed returns the Carnivore's true weight.
    """


def test_island_migration():
    """

    """


def test_only_migrates_once():

