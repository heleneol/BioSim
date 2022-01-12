import pytest
from src.biosim.animals import Herbivore, Carnivore


# Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests
ALPHA = 0.01  # significance level for statistical tests

@pytest.fixture
def set_herbivore_parametres(request):
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
        Herbivore.set_params()
    """
    default_parametres = Herbivore.parameters.copy()
    Herbivore.set_parameters(request.param)
    yield
    Herbivore.set_parameters(default_parametres)

@pytest.fixture
def set_carnivore_parametres(request):
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
    default_parametres = Carnivore.parameters.copy()
    Carnivore.set_parametres(request.param)
    yield
    Carnivore.set_parametres(default_parametres)



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
        Herbivore(age = -5)

    with pytest.raises(ValueError, match = 'Animal weight has to be >= 0'):
        Carnivore(weight= 0)

def test_deat_by_to_low_weight():
    #denne kan passere tilfeldig om vekten er lav siden død da er bestemt av sannsynlighet
    herb = Herbivore()
    carn = Carnivore()
    herb.set_weight(new_weight = -2)
    carn.set_weight(new_weight= 0)
    assert herb.dies()
    assert carn.dies()

@pytest.mark.parametrize('set_herbivore_parametres', [{'omega': 100}], indirect=True)
def test_deat_by_high_omega(set_herbivore_parametres):
    herb = Herbivore()
    assert herb.parameters['omega'] == 100
    for _ in range(50):
        assert herb.dies()

def test_update_fitness():


