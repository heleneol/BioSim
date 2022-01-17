from src.biosim.island import Island
import textwrap
import pytest


ini_herbs = [{'loc': (2, 2),
              'pop': [{ 'species': 'Herbivore',
                        'age': 5,
                        'weight': 20}
                        for _ in range(2)]}]


def test_creatmap():
    """
    Tests if an Island i initilized and has the attribute self.map. With an empty geogr the len is zero
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
    Tests what happens if the island geographie is non-rectangular
    """
    geogr = """\
                WWWW
                WLW
                WWW"""
    geogr = textwrap.dedent(geogr)
    with pytest.raises(ValueError, match='The map has to be a rectangular shape! \n'
                             'All rows do not contain the same amount of letters'):
        i = Island(geogr)

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
        i = Island(geogr)

def test_hole_in_the_map():
    """
    Test if the valueerror is raised if there is a hole in the map
    """
    geogr = """\
                WWW
                W W
                WWW"""
    geogr = textwrap.dedent(geogr)
    with pytest.raises(ValueError):
        i = Island(geogr)

def test_placing_population():
    """
    Test if ValueError is raised if a population is placed outside of the map.
    Also test if a population is placed in lowland, and not in water.
    """
    populations = [{'loc': (2, 2),
                    'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(200)]},
                    {'loc': (4, 5),
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

