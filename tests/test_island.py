"""Tests for the Island class"""

from biosim.island import Island

import textwrap
import pytest
import numpy as np


@pytest.fixture
def map_island():
    geography = """\
                    WWWWWWWWWWW
                    WLLLHHHLLLW
                    WLLLLLLLLLW
                    WLDDDDLLDDW
                    WLLLLLLLLLW
                    WWWWWWWWWWW"""
    geography = textwrap.dedent(geography)
    return Island(geography)


@pytest.fixture
def ini_pops():
    ini_pops = [{'loc': (2, 2),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 20}
                         for _ in range(20)]},
                {'loc': (3, 3),
                 'pop': [{'species': 'Herbivore',
                          'age': 3,
                          'weight': 20}
                         for _ in range(15)]},
                {'loc': (2, 5),
                 'pop': [{'species': 'Carnivore',
                          'age': 2,
                          'weight': 10}
                         for _ in range(4)]},
                {'loc': (2, 2),
                 'pop': [{'species': 'Carnivore',
                          'age': 2,
                          'weight': 10}
                         for _ in range(6)]}]
    return ini_pops


def test_creatmap(map_island):
    """
    Tests if an Island is initialized and has the attribute self.map
    with an empty geogr the len is zero.
    """
    assert len(map_island.map) > 0


def test_non_rectangular_shape():
    """
    Tests what happens if the island geography is non-rectangular.
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


def test_placing_population(ini_pops):
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


def test_set_animal_parameters(ini_pops, map_island):
    """
    Testing it is possible to set parameters for animals.
    """
    beta = 0.85
    omega = 0.6
    map_island.place_population(ini_pops)
    map_island.set_animal_parameters_island('Herbivore', {'beta': beta, 'omega': omega})

    assert map_island.sample_animals['herbivore']
    assert map_island.sample_animals['herbivore'].parameters['beta'] == beta
    assert map_island.sample_animals['herbivore'].parameters['omega'] == omega


def test_set_landscape_parameters(map_island):
    """
    Testing it is possible to set parameters for the landscape.
    """
    fodder = 700
    map_island.set_landscape_parameters_island('L', {'f_max': fodder})

    assert map_island.parameters['L']
    assert map_island.parameters['L'].parameters['f_max'] == fodder


def test_get_num_herbs(map_island, ini_pops):
    """
    Testing that the functions for getting the total number of a species
    on the island returns the correct total.
    """
    map_island.place_population(ini_pops)
    total_herb = 0
    total_carn = 0
    for population in ini_pops:
        pop = population['pop']
        for animal in pop:
            if animal['species'] == 'Herbivore':
                total_herb += 1
            elif animal['species'] == 'Carnivore':
                total_carn += 1
    assert map_island.get_number_of_herbs() == total_herb
    assert map_island.get_number_of_carns() == total_carn


def test_gives_animal_fitness(map_island, ini_pops):
    """
    Testing if get_'species'_fitness indeed returns a list of all the species' fitness.
    """
    before_herb = len(map_island.get_herbs_fitness())
    before_carn = len(map_island.get_carns_fitness())
    map_island.place_population(ini_pops)
    after_herb = len(map_island.get_herbs_fitness())
    after_carn = len(map_island.get_carns_fitness())

    assert before_herb < after_herb
    assert before_carn < after_carn


def test_get_species_age(map_island, ini_pops):
    """
    Testing if the get "species" age function indeed returns a list of ages of the species.
    """
    before_herb = len(map_island.get_herbs_age())
    before_carn = len(map_island.get_carns_age())
    map_island.place_population(ini_pops)
    after_herb = len(map_island.get_herbs_age())
    after_carn = len(map_island.get_carns_age())

    assert before_herb < after_herb
    assert before_carn < after_carn


def test_get_species_weight(map_island, ini_pops):
    """
    Testing if get "species" weight function indeed returns a list of the animals weight.
    """
    before_herb = len(map_island.get_herbs_weight())
    before_carn = len(map_island.get_carns_weight())
    map_island.place_population(ini_pops)
    after_herb = len(map_island.get_herbs_weight())
    after_carn = len(map_island.get_carns_weight())

    assert before_herb < after_herb
    assert before_carn < after_carn


def test_island_migration_happens(map_island):
    """
    Testing migration happens on the island.
    A large herbivore population, ini_pop, is placed on one cell on the island.
    The function get_number_herbs_per_cell is used to get the
    population-by-cell-matrix before and after the island migration function is called.
    These matrices should not be equal to another if
    some of the herbivore population has migrated to other cells.
    """
    # Setting ini_pop population to 250, and placing them near the middle of the island
    # to ensure some herbivores migrate.
    ini_pop = [{'loc': (3, 4),
                'pop': [{'species': 'Herbivore',
                         'age': 5,
                         'weight': 20}
                        for _ in range(250)]}]

    map_island.place_population(ini_pop)
    before = map_island.get_number_herbs_per_cell()
    map_island.island_migration()
    after = map_island.get_number_herbs_per_cell()

    assert np.array_equal(before, after) is False


def test_island_migration_happens_once(map_island):
    """
    Testing an animal only migrates once per year.
    Forcing migration with low age and large weight,
    so that the animal has to be in a neighbouring cell.
    Checking animal count in neighbouring cells and confirming the cell's
    combined herb_pop = 1.
    Resetting map-populations before running it again.
    """
    ini_pop = [{'loc': (3, 4),
                'pop': [{'species': 'Herbivore',
                         'age': 0,
                         'weight': 100}]}]
    map_island.set_animal_parameters_island('Herbivore', {'mu': 1.5})
    loc = (3, 4)
    neighbors = [map_island.map[(loc[0] - 1, loc[1])],
                 map_island.map[(loc[0] + 1, loc[1])],
                 map_island.map[(loc[0], loc[1] + 1)],
                 map_island.map[(loc[0], loc[1] - 1)]]
    for test in range(10):
        map_island._clean_island_for_herbs()
        map_island.place_population(ini_pop)
        map_island.island_migration()
        herb_count = 0
        for cell in neighbors:
            herb_count += len(cell.herb_pop)
        assert herb_count == 1
