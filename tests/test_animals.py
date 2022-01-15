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
# @pytest.fixture(autouse=True)
# def herb_example():
#     herbivore = [Herbivore(age=blablabla
#return herbivore


def test_input_param():
    """
    Testing that input of new parameter values is possible.
    """
    new_params = {'w_birth': 7.0,
                  'beta': 0.80}

    Carnivore.set_parameters(new_params)
    assert Carnivore.parameters['w_birth'] == 7.0
    assert Carnivore.parameters['beta'] == 0.80


def test_wrong_param():
    """
    Testing that errors are raised when input parameters are erroneous.
    """
    with pytest.raises(KeyError):
        Herbivore.set_parameters({'wbirth': 7.0})

    with pytest.raises(ValueError):
        Herbivore.set_parameters({'w_birth': -2.0})


def test_value_error_of_age_and_weight():
    """
    Testing whether ValueError is raised for error in input age and weight.
    """
    with pytest.raises(ValueError):
        Herbivore(age=-5)

    with pytest.raises(ValueError):
        Carnivore(weight=0)


def test_fitness_value():
    """
    Makes sure the fitness function returns a value from 0 to 1.
    """
    herb = Herbivore()

    for _ in range(50):
        herb.update_fitness()
        assert 0 <= herb.fitness <= 1


# Slette?:
def test_fitness_no_weight():
    """
    When the animal's weight is zero, the fitness is also zero.
    """
    carn = Carnivore()
    carn.set_weight(new_weight=0)

    for _ in range(50):
        carn.update_fitness()
        assert carn.fitness == 0


# Could we write 1/4 here?
def test_fitness_values():
    """
    Testing that the animal fitness is correctly calculated.
    """
    herb = Herbivore(age=5, weight=10)
    herb.update_age(years=herb.parameters['a_half'])
    herb.set_weight(new_weight=herb.parameters['w_half'])

    q_pos = 1 / (1 + (math.exp(herb.parameters['phi_age'] * (herb.age - herb.parameters['a_half']))))
    q_neg = 1 / (1 + (math.exp((-1) * herb.parameters['phi_weight'] * (herb.weight - herb.parameters['w_half']))))

    for _ in range(50):
        herb.update_fitness()
        assert herb.fitness == q_pos * q_neg


def test_regains_appetite():
    """
    Testing that the regain_appetite() function successfully sets the animal's appetite as parameter F.
    """
    carn = Carnivore()
    carn.appetite = 0
    carn.regain_appetite()
    assert carn.appetite == carn.parameters['F']


def test_certain_birth(mocker):
    """
    Mocker ensures random.random returns the value zero.
    Weight is set at 1000 to ensure it always surpasses xi*newborn.weight,
    and the function should not return None.
    """
    num = 100
    carn = Carnivore(weight=1000)
    mocker.patch('random.random', return_value=0)

    for _ in range(5):
        assert carn.gives_birth(N=num) is not None


@pytest.mark.parametrize('set_carnivore_parameters', [{'gamma': 0.0}], indirect=True)
def test_no_birth(set_carnivore_parameters):
    """
    If gamma is zero, the birth probability (gamma * fitness * (num - 1)), will be zero.
    Hence, gives_birth() will return None.
    """
    carn = Carnivore()
    num = 100

    for _ in range(50):
        assert carn.gives_birth(N=num) is None


@pytest.mark.parametrize('set_carnivore_parameters', [{'mu': 100}], indirect=True)
def test_certain_migration(set_carnivore_parameters):
    """
    Making sure the animal's fitness * mu > 1.
    """
    carn = Carnivore()
    # Ensuring the carnivore's fitness is large enough.
    carn.fitness = 10

    for _ in range(10):
        assert carn.migrate() is True


def test_animal_aging():
    """
    Testing that Herbivores and Carnivores age with 1 year.
    """
    herb = Herbivore()
    carn = Carnivore()
    for n in range(10):
        herb.update_age()
        carn.update_age()
        assert herb.age == n + 1
        assert carn.age == n + 1


def test_animal_metabolism():
    """
    Testing each animal loses weight with the metabolism function.
    """
    herb = Herbivore()
    h_weight_before = herb.weight

    carn = Carnivore()
    c_weight_before = carn.weight

    for _ in range(50):
        herb.metabolism()
        carn.metabolism()
        assert herb.weight < h_weight_before
        assert carn.weight < c_weight_before


def test_death_by_too_low_weight():
    # denne kan passere tilfeldig om vekten er lav siden død da er bestemt av sannsynlighet
    carn = Carnivore()
    carn.set_weight(new_weight=0)
    assert carn.dies()


@pytest.mark.parametrize('set_carnivore_parameters', [{'omega': 0.6}], indirect=True)
def test_dies_z_test(set_carnivore_parameters):
    """
    Binomial Z-test on the dies()-function with herbivores.

    H0 = The number of times the function returns True, the animal dies, is statistically significant with the
    probability exceeding the set significance level of 0.01 (ALPHA).
    H1 = The function does not return True a statistically significant number of times. We cannot accept H0 as true.

    Based on settinkilde.

    """
    random.seed(SEED)
    num = 100

    #h = Herbivore()
    c = Carnivore()
    p = c.parameters['omega'] * (1 - c.fitness)
    #p = h.parameters['omega'] * (1 - h.fitness)
    n = sum(c.dies() for _ in range(num))  # True == 1, False == 0

    mean = num * p
    var = math.sqrt(num * p * (1 - p))
    # noinspection PyPep8Naming
    Z = (n - mean) / var
    print(Z)
    phi = 2 * stats.norm.cdf(-abs(Z))
    print(phi)
    assert phi > ALPHA

# Test gives_birth():
# kanskje en statistisk test som sjekker om fordelingen er som forventet
# Test if self.weight<xi*newborn.weight returns None, and if species is herbivore it runs Herbivore()


def test_certain_death(mocker):
    """
    Using mocker to set random.random as 0.
    """
    herb = Herbivore()
    mocker.patch('random.random', return_value=0)
    for _ in range(10):
        assert herb.dies() # Trenger ikke is true her?



# Hva må vi egentlig teste i herb_feeding?:
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


def test_carn_nokill():
    """
    Testing the carnivore does not kill herbivore, carnivore_feeding returns True, if the herbivore's fitness
    exceeds the carnivore's fitness.
    """
    carn = Carnivore()
    herb = Herbivore()

    # Ensuring herbivore fitness > carnivore fitness
    carn.fitness = 0.5
    herb.fitness = 1

    for _ in range(10):
        assert carn.carnivore_feeding(herb) is True


@pytest.mark.parametrize('set_carnivore_parameters', [{'DeltaPhiMax': 0.5}], indirect=True)
def test_certain_kill(set_carnivore_parameters, mocker):
    """
    Testing the carnivore kills the herbivore using mocker to set random.random as 0 and.
    Ensuring DeltaPhi > DeltaPhiMax, so that the prey probability is 1.
    """
    carn = Carnivore()
    herb = Herbivore()

    carn.fitness = 1
    herb.fitness = 0.1

    mocker.patch('random.random', return_value=0)
    for _ in range(10):
        assert carn.carnivore_feeding(herb) is False

    # Bytte om på false og true i denne funksjonen?
