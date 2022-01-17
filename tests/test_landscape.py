import numpy as np

from src.biosim.landscape import Lowland, Highland, Water, Desert
from src.biosim.animals import *

import pytest
import random


@pytest.fixture
def set_lowland_parameters(request):
    """
    Fixture setting class parameters on Lowland, based on H.E. Plesser's biolab/bacteria.py.

    The fixture sets the Lowland parameters when called for setup,
    and resets them when called for teardown. This ensures that modified
    parameters are always reset before leaving a test.

    This fixture should be called via parametrize with indirect=True.

    :param request: Request object automatically provided by pytest.
                    request.param is the parameter dictionary to be passed to
                    Lowland.set_parameters()
    """
    default_parameters = Lowland.parameters.copy()
    Lowland.set_parameters(request.param)
    yield
    Lowland.set_parameters(default_parameters)


@pytest.fixture
def set_highland_parameters(request):
    """
    Fixture setting class parameters on Highland, based on H.E. Plesser's biolab/bacteria.py.

    The fixture sets the Highland parameters when called for setup,
    and resets them when called for teardown. This ensures that modified
    parameters are always reset before leaving a test.

    This fixture should be called via parametrize with indirect=True.

    :param request: Request object automatically provided by pytest.
                    request.param is the parameter dictionary to be passed to
                    Highland.set_parameters()
    """
    default_parameters = Highland.parameters.copy()
    Highland.set_parameters(request.param)
    yield
    Highland.set_parameters(default_parameters)


def test_input_param_landscape():
    """
    Testing that input of new parameter values is possible.
    """
    new_params = {'f_max': 300}

    Highland.set_parameters(new_params)
    assert Highland.parameters['f_max'] == 300


def test_param_wrong_landscape():
    """
    Testing that errors are raised when trying to insert fodder in Desert and Water habitat.
    """
    with pytest.raises(KeyError):
        Desert.set_parameters({'f_max': 20})

    with pytest.raises(KeyError):
        Water.set_parameters({'f_max': 40})


def test_param_mistake_landscape():
    """
    Testing that errors are raised when input parameters are erroneous.
    """
    with pytest.raises(KeyError):
        Highland.set_parameters({'fmax': 20})


def test_value_error_of_age_and_weight():
    """
    Testing whether ValueError is raised for error in input age and weight.
    """
    with pytest.raises(ValueError):
        Highland.set_parameters({'f_max': -40})


def generate_herb_pop(age, weight, num_herbs):
    """
    A function that generates a herbivore population.
    Write None for age and weight if you dont want to specify.
    """
    return [Herbivore(age=age, weight=weight) for _ in range(num_herbs)]


def generate_carn_pop(age, weight, num_carns):
    """
    A function that generates a herbivore population.
    Write None for age and weight if you dont want to specify.
    """
    return [Carnivore(age=age, weight=weight) for _ in range(num_carns)]


def test_landscape_construction():
    """
    Testing that creating landscapes with a given list of animal objects works.
    """
    number_herb = 50
    number_carn = 10
    herb_pop = [Herbivore(age=5) for _ in range(number_herb)]
    carn_pop = [Carnivore(age=2) for _ in range(number_carn)]
    L = Lowland(herb_pop, carn_pop)
    H = Highland(herb_pop, carn_pop)
    D = Desert(herb_pop, carn_pop)

    for landscape in (L, H, D):
        assert landscape.get_num_herbs() == number_herb and landscape.get_num_carns() == number_carn


random_fodder = random.randint(0, 800)


@pytest.mark.parametrize('set_lowland_parameters', [{'f_max': random_fodder}], indirect=True)
def test_setting_fodder_amount(set_lowland_parameters):
    L = Lowland()
    assert L.fodder == random_fodder


#@pytest.mark.parametrize('set_lowland_parameters', [{'f_max': random_fodder}], indirect=True)
#def test_setting_fodder_desert(set_lowland_parameters):
#    D = Desert()
#    with pytest.raises():
#        D.fodder


def test_sort_herbs_by_fitness():
    """
    Testing if the list of herbivores are sorted by decreasing fitness when decreasing=True.
    """
    herb_pop = [Herbivore() for _ in range(10)]

    h = Highland(herb_pop)
    h.sort_herbs_by_fitness(decreasing=True)
    failed = 0
    if all(h.herb_pop[i].fitness <= h.herb_pop[i + 1].fitness for i in range(len(h.herb_pop) - 1)):
        failed += 1
    assert failed == 0


def test_herbivores_eating():
    """
    Testing if herbivores are eating by comparing their weight before and after eating.
    """
    herb_pop = [Herbivore() for _ in range(10)]
    H = Highland(herb_pop)

    original_mean_weight = sum([herb.weight for herb in H.herb_pop]) / len(H.herb_pop)
    H.herbivores_eating()
    post_eating_mean_weight = sum([herb.weight for herb in H.herb_pop]) / len(H.herb_pop)
    assert original_mean_weight < post_eating_mean_weight


def test_regrowth():
    """
    Testing regrowth of fodder sets the fodder amount to f_max.
    """
    low = Lowland()
    low.fodder = 20
    low.regrowth()
    assert low.fodder == low.parameters['f_max']


def test_carnivores_eating():
    """
    Testing the amount of herbivores remain the same or less than before the carnivores feed.
    """
    herb_pop = [Herbivore() for _ in range(250)]
    carn_pop = [Carnivore() for _ in range(5)]
    D = Desert(herb_pop, carn_pop)

    for hunting_season in range(10):
        herb_pop_before_hunting = D.get_num_herbs()
        D.carnivores_eating()
        assert D.get_num_herbs() <= herb_pop_before_hunting


def test_reproduction():
    """
    Testing both populations increase after the breeding season. Setting weight high and age low to ensure good fitness
    and that feeding happens.
    """
    herb_pop = [Herbivore(age=1, weight=50) for _ in range(250)]
    carn_pop = [Carnivore(age=1, weight=50) for _ in range(5)]
    h = Highland(herb_pop, carn_pop)

    herb_count_old = h.get_num_herbs()
    carn_count_old = h.get_num_carns()

    for _ in range(20):
        h.reproduction()
        herb_count = h.get_num_herbs()
        carn_count = h.get_num_carns()
        assert herb_count >= herb_count_old and carn_count >= carn_count_old
        herb_count_old, carn_count_old = herb_count, carn_count


# def test_reproduction_statisticly


def test_aging():
    """
    Testing whether a population ages.
    Using a function for calculating mean age to compare the mean age after aging is bigger than before, or is equal
    to 1 in the carnivore population's case
    """
    def get_mean_age(population):
        return sum([animal.age for animal in population]) / len(population)

    herb_pop = [Herbivore(age=age) for herb, age in zip(range(250), [random.randint(0, 6) for _ in range(250)])]
    carn_pop = [Carnivore(age=0) for _ in range(5)]
    L = Lowland(herb_pop, carn_pop)
    herb_age_before = get_mean_age(L.herb_pop)
    L.aging()
    assert get_mean_age(L.herb_pop) > herb_age_before
    assert get_mean_age(L.carn_pop) == 1


def test_add_population():
    """
    Testing whether adding population to water raises the expected ValueError.
    """
    herb_pop = [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]
    w = Water()
    with pytest.raises(ValueError):
        w.add_population(herb_pop)


def test_animal_migration():
    """
    Testing migration returns an empty migrator list if the number of animals in the population doesn't change after
    running migration, and that it returns a list with animals if there is a change of population.
    """
    l = Lowland()
    l.herb_pop = generate_herb_pop(age=5, weight=None, num_herbs=20)
    l.carn_pop = generate_carn_pop(age=5, weight=None, num_carns=10)
    num_herbs_old = l.get_num_herbs()
    num_carns_old = l.get_num_carns()
    migrators_herb, migrators_carn = l.animal_migration()
    if num_herbs_old > l.get_num_herbs():
        assert len(migrators_herb) > 0
    else:
        assert len(migrators_herb) == 0
    if num_carns_old > l.get_num_carns():
        assert len(migrators_carn) > 0
    else:
        assert len(migrators_carn) == 0
