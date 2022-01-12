import pytest
import random
from src.biosim.landscape import *
from src.biosim.animals import *

@pytest.fixture
def set_lowland_parameters(request):
    """
    Fixture setting class parameters on Herbivore.

    The fixture sets Herbivore parameters when called for setup,
    and resets them when called for teardown. This ensures that modified
    parameters are always reset before leaving a test.

    This fixture should be called via parametrize with indirect=True.

    Based on https://stackoverflow.com/a/33879151

    Parameters
    ----------
    request
        Request object automatically provided by pytest.
        request.param is the parameter dictionary to be passed to
        Herbivore.set_parameters()
    """
    default_parameters = Lowland.parameters.copy()
    Lowland.set_parameters(request.param)
    yield
    Lowland.set_parameters(default_parameters)

@pytest.fixture
def set_highland_parameters(request):
    """
    Fixture setting class parameters on Herbivore.

    The fixture sets Herbivore parameters when called for setup,
    and resets them when called for teardown. This ensures that modified
    parameters are always reset before leaving a test.

    This fixture should be called via parametrize with indirect=True.

    Based on https://stackoverflow.com/a/33879151

    Parameters
    ----------
    request
        Request object automatically provided by pytest.
        request.param is the parameter dictionary to be passed to
        Herbivore.set_parameters()
    """
    default_parameters = Highland.parameters.copy()
    Highland.set_parameters(request.param)
    yield
    Highland.set_parameters(default_parameters)


def test_landscape_construction():
    number_herb = 50
    number_carn = 10
    herb_pop = [Herbivore(age = 5) for herb in range(number_herb)]
    carn_pop = [Carnivore(age = 2) for carn in range(number_carn)]
    L = Lowland(herb_pop,carn_pop)
    H = Highland(herb_pop, carn_pop)
    D = Desert(herb_pop, carn_pop)

    for landscape in (L,H,D):
        assert landscape.get_num_herbs() == number_herb  and landscape.get_num_carns() == number_carn


for _ in range(10):
    random_fooder = random.randint(0, 800)

@pytest.mark.parametrize('set_lowland_parameters', [{'f_max': random_fooder}], indirect=True)
def test_setting_fooder_amount(set_lowland_parameters):
        L = Lowland()
        assert L.fodder == random_fooder

def test_sort_herbs_by_fitness():
    herb_pop = [Herbivore() for herb in range(10)]

    H = Highland(herb_pop)
    H.sort_herbs_by_fitness(decreasing=True)
    failed = 0
    if (all(H.herb_pop[i].fitness <= H.herb_pop[i + 1].fitness for i in range(len(H.herb_pop) - 1))):
        failed += 1
    assert failed == 0


def test_herbivores_eating():
    herb_pop = [Herbivore() for herb in range(10)]
    H = Highland(herb_pop)

    original_mean_weight = sum([herb.weight for herb in H.herb_pop]) / len(H.herb_pop)
    H.herbivores_eating()
    post_eating_mean_weight = sum([herb.weight for herb in H.herb_pop]) / len(H.herb_pop)
    assert original_mean_weight < post_eating_mean_weight


def test_regrowth():
    L = Lowland()
    L.fodder = 20
    L.regrowth()
    assert L.fodder == L.parameters['f_max']

def test_carnivores_eating():
    herb_pop = [Herbivore() for herb in range(250)]
    carn_pop = [Carnivore() for carn in range(5)]
    D = Desert(herb_pop, carn_pop)

    for hunting_season in range(10):
        herb_pop_before_hunting = D.get_num_herbs()
        D.carnivores_eating()
        assert D.get_num_herbs() <= herb_pop_before_hunting

#def test_reproduction():

def test_aging():
    def get_mean_age(population):
        return sum([animal.age for animal in population]) / len(population)

    herb_pop = [Herbivore(age=age) for herb, age in zip(range(250),[random.randint(0,6) for num in range(250)])]
    carn_pop = [Carnivore() for carn in range(5)]
    L = Lowland(herb_pop, carn_pop)
    herb_age_before = get_mean_age(L.herb_pop)
    L.aging()
    assert get_mean_age(L.herb_pop) < herb_age_before
    assert get_mean_age(L.carn_pop) == 1

def generate_herb_pop(age, weight, num_herbs):
    """write None for age and weight if you dont want to spesify"""
    return [Herbivore(age=age, weight=weight) for herb in range(num_herbs)]
def generate_carn_pop(age, weight, num_carns):
    """write None for age and weight if you dont want to spesify"""
    return [Carnivore(age=age, weight=weight) for carn in range(num_carns)]










