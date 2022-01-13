import pytest
import scipy.stats as stats

from src.biosim.animals import *



# Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests
ALPHA = 0.01  # significance level for statistical tests

@pytest.fixture
def set_herbivore_parameters(request):
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
    default_parameters = Herbivore.parameters.copy()
    Herbivore.set_parameters(request.param)
    yield
    Herbivore.set_parameters(default_parameters)


@pytest.fixture
def set_carnivore_parameters(request):
    """
    Fixture setting class parameters on Carnivore.

    The fixture sets Carnivore parameters when called for setup,
    and resets them when called for teardown. This ensures that modified
    parameters are always reset before leaving a test.

    This fixture should be called via parametrize with indirect=True.

    Based on https://stackoverflow.com/a/33879151

    Parameters
    ----------
    request
        Request object automatically provided by pytest.
        request.param is the parameter dictionary to be passed to
        Carnivore.set_params()
    """
    default_parameters = Carnivore.parameters.copy()
    Carnivore.set_parameters(request.param)
    yield
    Carnivore.set_parameters(default_parameters)

# Fixture for Herbivore og Carnivore? Siden vi bruker dem i så mange tester.

def test_input_param():
    """ Testing input of new parameters """
    new_params = {'w_birth': 7.0,
                  'beta': 0.80}

    Carnivore.set_parameters(new_params)
    assert Carnivore.parameters['w_birth'] == 7.0
    assert Carnivore.parameters['beta'] == 0.80


def test_wrong_param():
    """ Testing raising errors when input parameters are erroneous. """
    with pytest.raises(KeyError):
        Herbivore.set_parameters({'wbirth': 7.0})

    with pytest.raises(ValueError):
        Herbivore.set_parameters({'w_birth': -2.0})


def test_value_error_of_age_and_weight():
    """ Testing whether ValueError is raised for error in input age and weight."""
    with pytest.raises(ValueError, match='Animal age has to be >= 0'):
        Herbivore(age=-5)

    with pytest.raises(ValueError, match='Animal weight has to be >= 0'):
        Carnivore(weight=0)


def test_fitness_no_weight():
    """ Testing if the animals weight is zero, the fitness is also zero. """
    carn = Carnivore()
    carn.set_weight(new_weight=0)

    for _ in range(50):
        carn.update_fitness()
        assert carn.fitness == 0


def test_fitness_by_halfvalues():
    herb = Herbivore()
    herb.update_age(years=herb.parameters['a_half'])
    herb.set_weight(new_weight=herb.parameters['w_half'])

    for _ in range(50):
        herb.update_fitness()
        assert herb.fitness == 1/4


def test_fitness_value():
    """ Testing fitness is between 0 and 1. """
    herb = Herbivore()

    for _ in range(50):
        herb.update_fitness()
        assert 0 <= herb.fitness <= 1


def test_animal_aging():
    """ Testing that Herbivores and Carnivores age with 1 year. """
    herb = Herbivore()
    carn = Carnivore()
    for n in range(10):
        herb.update_age()
        carn.update_age()
        assert herb.age == n + 1
        assert carn.age == n + 1


def test_death_by_too_low_weight():
    # denne kan passere tilfeldig om vekten er lav siden død da er bestemt av sannsynlighet
    herb = Herbivore()
    carn = Carnivore()
    herb.set_weight(new_weight=-2)
    carn.set_weight(new_weight=0)
    assert herb.dies()
    assert carn.dies()


#@pytest.mark.parametrize('set_herbivore_parameters', [{'omega': 100}], indirect=True)
#def test_death_by_higher_omega(set_herbivore_parameters):
#    herb = Herbivore()
#    assert herb.parameters['omega'] == 100
#
#    for _ in range(50):
#        assert herb.dies()
# Synes vi kan ditche denne testen ^.


# Tror denne er unødvendig, siden denne teknisk sett tester formel og ikke kode:
def test_no_population_no_birth():
    herb = Herbivore()
    carn = Carnivore()
    assert herb.gives_birth(N=1) is None
    assert carn.gives_birth(N=1) is None

# Test gives_birth():
@pytest.mark.parametrize('set_carnivore_parameters', [{'preg_prob': 0.4}], indirect=True)
def test_birthrate_z_test(set_carnivore_parameters):
    random.seed(SEED)
    num = 100
    p = Carnivore.get_param()['preg_prob']

    c = Carnivore
    n = sum(c.gives_birth() for _ in range(num))

    mean = num * p
    var = num * p * (1-p)
    # noinspection PyPep8Naming
    Z = (n - mean) / math.sqrt(var)
    phi = 2 * stats.norm.cdf(-abs)

    assert phi > ALPHA

# kanskje en statistisk test som sjekker om fordelingen er som forventet
# Test if self.weight<xi*newborn.weight returns None, and if species is herbivore it runs Herbivore()


def test_animal_metabolism():
    herb = Herbivore()
    h_weight_before = herb.weight

    carn = Carnivore()
    c_weight_before = carn.weight

    for _ in range(50):
        herb.metabolism()
        carn.metabolism()
        assert herb.weight < h_weight_before
        assert carn.weight < c_weight_before


# Hva må vi egentlig teste i herb_feeding?
def test_herb_weightchange_fodder():
    herb = Herbivore()
    weight_before = herb.weight

    herb.herbivore_feeding(landscape_fodder=herb.appetite)
    assert herb.weight == weight_before + (herb.parameters['beta'] * herb.appetite)


def test_herb_fitnesschange_fodder():
    herb = Herbivore()
    fitness_before = herb.fitness

    herb.herbivore_feeding(landscape_fodder=herb.appetite)
    assert herb.fitness > fitness_before
