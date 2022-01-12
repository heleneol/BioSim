import pytest
from src.biosim.animals import Herbivore, Carnivore


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



def test_animal_aging():
    herb = Herbivore()
    carn = Carnivore()
    for n in range(10):
        herb.update_age()
        carn.update_age()
        assert herb.age == n + 1
        assert carn.age == n + 1

def test_value_error_of_age_and_weight():
    with pytest.raises(ValueError, match = 'Animal age has to be >= 0'):
        Herbivore(age=-5)

    with pytest.raises(ValueError, match = 'Animal weight has to be >= 0'):
        Carnivore(weight=0)

def test_deat_by_to_low_weight():
    #denne kan passere tilfeldig om vekten er lav siden død da er bestemt av sannsynlighet
    herb = Herbivore()
    carn = Carnivore()
    herb.set_weight(new_weight=-2)
    carn.set_weight(new_weight=0)
    assert herb.dies()
    assert carn.dies()

@pytest.mark.parametrize('set_herbivore_parameters', [{'omega': 100}], indirect=True)
def test_death_by_higher_omega(set_herbivore_parameters):
    herb = Herbivore()
    assert herb.parameters['omega'] == 100

    for _ in range(50):
        assert herb.dies()

def test_fitness_by_halfvalues():
    herb = Herbivore()
    herb.update_age(years=herb.parameters['a_half'])
    herb.set_weight(new_weight=herb.parameters['w_half'])

    for _ in range(50):
        herb.update_fitness()
        assert herb.fitness == 1/4

def test_fitness_no_weight():
    herb = Herbivore()
    herb.set_weight(new_weight=0)

    for _ in range(50):
        herb.update_fitness()
        assert herb.fitness == 0

#def test_metabolism():


# Test gives_birth(). Test when N<2 it returns None, if self.weight<xi*newborn.weight returns None

# Test metabolism

# Test feeding herbivores
# ... and feeding carnivores
