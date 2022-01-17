from src.biosim.island import Island
import textwrap
import pytest


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
        def set_animal_parameters_island(self, species, params):
        species = self.sample_animals[species.lower()]
        species.set_parameters(new_params=params)
    """
    i = Island(geography)
    i.set_animal_parameters_island('herbivore', {'beta': 0.85, 'omega': 0.6})

    # assert i.


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
                    'pop': [{'species': 'Carnivore',
                            'age': 3,
                             'weight': 20}
                            for _ in range(number)]}]

    i = Island(geography)
    i.place_population(ini_herbies)

    assert i.get_number_of_herbs() == num + number



