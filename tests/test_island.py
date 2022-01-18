"""Tests for the Island class provided in biosim/src/island.py """

from biosim.island import Island

import textwrap
import pytest


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
    Tests if an Island is initialized and has the attribute self.map. With an empty geogr the len is zero
    """
    assert len(map_island.map) > 0


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


class test_get_information:
    """
    A test class for all the get-functions of the Island class.
    """

    def __init__(self, geography, ini_pops):

        self.geography = textwrap.dedent(geography)
        self.island = Island(geography)
        self.ini_pops = ini_pops
        self.island.place_population(populations=ini_pops)

    def test_get_num_herbs(self):
        """
        Testing that the function get_num_herbs() returns the total amount of herbivores placed on the island.
        """
        total_herb = 0
        for population in self.ini_pops:
            total_herb += len(population['pop'])
        assert self.island_test.get_number_of_herbs() == total_herb

    def test_get_num_carnivores(self):
        """
        Testing that the function get_num_carns() returns the total amount of carnivores placed on the island.
        """
        total_carn = 0
        for population in self.ini_pops:
            total_carn += len(population['pop'])
        assert self.island_test.get_number_of_carns() == total_carn

    def test_get_number_herbs_per_cell():
        """
        Testing that the function get_number_herbs_per_cell() returns the amount of herbivores in each cell on the island.
        """

        #assert np.any(i.get_number_herbs_per_cell()) == num


    def test_get_number_carns_per_cell():
        """
        Testing that the function get_number_carns_per_cell() returns the amount of carnivores in each cell on the island.
        """


    def test_gives_herbs_fitness(self, ini_pop):
        """
        Testing if get_herbs_fitness indeed returns a list of all the herbivores fitness.
        """

        total_herbivore = 0
        before = len(self.island.get_herbs_fitness())
        self.island.place_population(ini_pops)
        after = len(self.island.get_herbs_fitness())

        assert before < after
        assert after == total_herbivore


    def test_gives_carns_fitness(self):
        """
        Testing if get_carns_fitness indeed returns a list of all the carnivores fitness.
        """
        total_carnviore = 0
        before = len(self.island.get_carns_fitness())
        self.island.place_population(ini_pops)
        after = len(self.island.get_carns_fitness())

        assert before < after
        assert after == total_carnviore


    def test_get_herbs_age(self):
        """
        Testing if get_herbs_age indeed returns the Herbivore's true age.
        """
        total_herbivore = 0
        before = len(self.island.get_herbs_age())
        self.island.place_population(ini_pops)
        after = len(self.island.get_herbs_age())

        assert after == total_herbivore


    def test_get_carns_age(self):
        """
        Testing if get_carns_age indeed returns the Carnivore's true age.
        """
        total_carnviore = 0
        before = len(self.island.get_carns_age())
        self.island.place_population(ini_pops)
        after = len(self.island.get_carns_age())

        assert before < after
        assert after == total_carnviore


    def test_get_herbs_weight(self):
        """
        Testing if get_herbs_weight indeed returns the Herbivore's true weight.
        """
        total_herbivore = 0
        before = len(self.island.get_herbs_weight())
        self.island.place_population(ini_pops)
        after = len(self.island.get_herbs_weight())

        assert after == total_herbivore


    def test_get_carns_weight(self):
        """
        Testing if get_carns_weight indeed returns the Carnivore's true weight.
        """
        total_carnviore = 0
        before = len(self.island.get_carns_weight())
        self.island.place_population(ini_pops)
        after = len(self.island.get_carns_weight())

        assert after == total_carnviore


def test_island_migration():
    """

    """


def test_only_migrates_once():
    """
    """
