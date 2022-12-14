"""Tests for the Landscape superclass with associated subclasses."""

from biosim.landscape import Lowland, Highland, Water, Desert
from biosim.animals import *

import pytest
import random


@pytest.fixture
def set_lowland_parameters(request):
    """
    Fixture setting class parameters for Lowland, based on H.E. Plesser's biolab/bacteria.py.

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
    Fixture setting class parameters for Highland, based on H.E. Plesser's biolab/bacteria.py.

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


def generate_herb_pop(age, weight, num_herbs):
    """
    A function that generates a herbivore population.
    Write None for age and weight if you do not want to specify.
    """
    return [Herbivore(age=age, weight=weight) for _ in range(num_herbs)]


def generate_carn_pop(age, weight, num_carns):
    """
    A function that generates a herbivore population.
    Write None for age and weight if you do not want to specify.
    """
    return [Carnivore(age=age, weight=weight) for _ in range(num_carns)]


@pytest.fixture
def herb_pop():
    herb_pop = [{'species': 'Herbivore',
                 'age': 5,
                 'weight': 20}
                for _ in range(150)]
    return herb_pop


@pytest.fixture
def highland():
    return Highland()


@pytest.fixture
def lowland():
    return Lowland()


def test_input_param_landscape():
    """
    Testing that input of new parameter values is possible.
    """
    new_params = {'f_max': 300}
    Highland.set_parameters(new_params)
    assert Highland.parameters['f_max'] == 300


def test_param_mistake_landscape():
    """
    Testing that errors are raised when input parameters are erroneous.
    """
    with pytest.raises(KeyError):
        Lowland.set_parameters({'fmax': 20})

    with pytest.raises(ValueError):
        Lowland.set_parameters({'f_max': -40})


def test_landscape_construction():
    """
    Testing that creating landscapes with a given list of animal objects works.
    """
    number_herb = 50
    number_carn = 10
    herb_pop = [Herbivore(age=5) for _ in range(number_herb)]
    carn_pop = [Carnivore(age=2) for _ in range(number_carn)]
    low = Lowland(herb_pop, carn_pop)
    h = Highland(herb_pop, carn_pop)
    d = Desert(herb_pop, carn_pop)

    for landscape in (low, h, d):
        assert landscape.get_num_herbs() == number_herb and landscape.get_num_carns() == number_carn


def test_habitability_true(herb_pop):
    """
    Testing habitability.
    """
    d = Desert(herb_pop)
    w = Water(herb_pop)
    assert d.habitability is True and w.habitability is False


def test_add_population_water(herb_pop):
    """
    Testing whether adding population to water raises the expected ValueError.
    """
    w = Water()
    with pytest.raises(ValueError):
        w.add_population(herb_pop)


def test_add_population_species(highland):
    """
    Testing whether adding population with erroneous assigned species will
    raise a KeyError as expected.
    """
    herb_pop = [{'age': 5,
                'weight': 20}
                for _ in range(150)]

    with pytest.raises(KeyError):
        highland.add_population(herb_pop)


def test_add_population_expected(lowland):
    """
    Testing whether population is added as expected
    """
    num = 30
    carn_pop = [{'species': 'Carnivore',
                 'age': 5,
                 'weight': 20}
                for _ in range(num)]
    lowland.add_population(animals=carn_pop)
    assert len(lowland.carn_pop) == num


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


def test_regrowth(lowland):
    """
    Testing regrowth of fodder sets the fodder amount to f_max.
    """
    lowland.fodder = 20
    lowland.regrowth()
    assert lowland.fodder == lowland.parameters['f_max']


def test_herbivores_eating():
    """
    Testing if herbivores are eating by comparing their mean weight before and after eating.
    """
    herb_pop = generate_herb_pop(None, None, 20)
    h = Highland(herb_pop)
    original_mean_weight = sum([herb.weight for herb in h.herb_pop]) / len(h.herb_pop)
    h.herbivores_eating()
    post_eating_mean_weight = sum([herb.weight for herb in h.herb_pop]) / len(h.herb_pop)
    assert original_mean_weight < post_eating_mean_weight


def test_carnivores_eating():
    """
    Testing the amount of herbivores remain the same or less than before the carnivores feed.
    """
    herb_pop = [Herbivore() for _ in range(100)]
    carn_pop = [Carnivore() for _ in range(5)]
    d = Desert(herb_pop, carn_pop)

    for hunting_season in range(5):
        herb_pop_before_hunting = d.get_num_herbs()
        d.carnivores_eating()
        assert d.get_num_herbs() <= herb_pop_before_hunting


def test_reproduction():
    """
    Testing both populations increase after the breeding season. Setting weight high
    and age low to ensure good fitness and that feeding happens.
    """
    herb_pop = [Herbivore(age=1, weight=50) for _ in range(100)]
    carn_pop = [Carnivore(age=1, weight=50) for _ in range(5)]
    h = Highland(herb_pop, carn_pop)
    herb_count_old = h.get_num_herbs()
    carn_count_old = h.get_num_carns()

    for _ in range(10):
        h.reproduction()
        herb_count = h.get_num_herbs()
        carn_count = h.get_num_carns()
        assert herb_count >= herb_count_old and carn_count >= carn_count_old
        herb_count_old, carn_count_old = herb_count, carn_count


def test_register_migrants():
    """
    Testing that the input animal is appended to the right list of migrating animals.
    """
    herb_pop = [Herbivore(age=1, weight=50) for _ in range(20)]
    carn_pop = [Carnivore(age=2, weight=50) for _ in range(20)]
    low = Lowland(herb_pop=herb_pop, carn_pop=carn_pop)
    for herb in herb_pop:
        low.register_migrants(herb)
    for carn in carn_pop:
        low.register_migrants(carn)
    assert len(low.migrating_herbs) > 0 and len(low.migrating_carns) > 0


def test_add_migrators():
    """
    Testing that the migrators are added to the population,
    and that the list of migrators is emptied.
    """
    carn_pop = [Carnivore(age=1, weight=50) for _ in range(20)]
    h = Highland(carn_pop=carn_pop)
    len_carn_before = len(h.carn_pop)
    h.migrating_carns = [Carnivore(age=1, weight=50) for _ in range(3)]
    h.add_migraters_to_pop()
    len_carn_after = len(h.carn_pop)
    assert len(h.migrating_carns) == 0 and len_carn_after > len_carn_before


def test_aging():
    """
    Testing whether a population ages.
    Using a function for calculating mean age to compare the mean age
    after aging is bigger than before, or is equal to 1 in the carnivore population's case
    """
    def get_mean_age(population):
        return sum([animal.age for animal in population]) / len(population)

    herb_pop = [Herbivore(age=age) for herb, age in zip(range(250),
                                                        [random.randint(0, 6) for _ in range(250)])]
    carn_pop = [Carnivore(age=0) for _ in range(5)]
    low = Lowland(herb_pop, carn_pop)
    herb_age_before = get_mean_age(low.herb_pop)
    low.aging()
    assert get_mean_age(low.herb_pop) > herb_age_before and get_mean_age(low.carn_pop) == 1


def test_population_weightloss():
    """
    Testing the mean weight of a population is lower after the animal's annual weightloss.
    """
    def get_mean_weight(population):
        return sum([animal.weight for animal in population]) / len(population)
    herb_pop = generate_herb_pop(None, None, 10)
    carn_pop = generate_carn_pop(None, None, 10)
    h = Highland(herb_pop, carn_pop)
    herb_weight_before = get_mean_weight(h.herb_pop)
    carn_weight_before = get_mean_weight(h.carn_pop)
    h.weight_loss()
    assert get_mean_weight(h.herb_pop) < herb_weight_before \
           and get_mean_weight(h.carn_pop) < carn_weight_before


def test_population_death_occurs():
    """
    Testing that some of the population die after annually.
    Ensuring some animals are expected to die by setting
    the age high and weight low (bad fitness), and setting the population to 100.
    """
    carn_pop = generate_carn_pop(age=60, weight=2, num_carns=100)
    herb_pop = generate_herb_pop(age=60, weight=2, num_herbs=100)
    d = Desert(herb_pop=herb_pop, carn_pop=carn_pop)
    carn_pop_before = len(d.carn_pop)
    herb_pop_before = len(d.herb_pop)
    d.population_death()
    assert len(d.carn_pop) < carn_pop_before and len(d.herb_pop) < herb_pop_before


def test_animal_migration(lowland):
    """
    Testing migration returns an empty migrator list if the number of animals
    in the population doesn't change after running migration,
    and that it returns a list with animals if there is a change of population.
    """
    lowland.herb_pop = generate_herb_pop(age=5, weight=None, num_herbs=20)
    lowland.carn_pop = generate_carn_pop(age=5, weight=None, num_carns=10)
    num_herbs_old = lowland.get_num_herbs()
    num_carns_old = lowland.get_num_carns()
    migrators_herb, migrators_carn = lowland.animal_migration()
    if num_herbs_old > lowland.get_num_herbs():
        assert len(migrators_herb) > 0
    else:
        assert len(migrators_herb) == 0
    if num_carns_old > lowland.get_num_carns():
        assert len(migrators_carn) > 0
    else:
        assert len(migrators_carn) == 0
