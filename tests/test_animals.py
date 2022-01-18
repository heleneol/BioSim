"""Tests for the Animal class provided in biosim/src/animals.py """

import pytest
import scipy.stats as stats

from biosim.animals import *

# Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests
ALPHA = 0.01  # significance level for statistical tests

@pytest.fixture
def set_herbivore_parameters(request):
    """
    Fixture setting class parameters for Herbivore, based on H. E. Plesser's biolab/bacteria.py

    The fixture sets Herbivore parameters when called for setup,
    and resets them when called for teardown. This ensures that modified
    parameters are always reset before leaving a test.

    This fixture should be called via parametrize with indirect=True.

    :param request: Request object automatically provided by pytest.
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
    Fixture setting class parameters for Carnivore, based on H. E. Plesser's biolab/bacteria.py.

    The fixture sets Carnivore parameters when called for setup,
    and resets them when called for teardown. This ensures that modified
    parameters are always reset before leaving a test.

    This fixture should be called via parametrize with indirect=True.

    :param request: Request object automatically provided by pytest.
    request.param is the parameter dictionary to be passed to
    Carnivore.set_parameters()
    """
    default_parameters = Carnivore.parameters.copy()
    Carnivore.set_parameters(request.param)
    yield
    Carnivore.set_parameters(default_parameters)


@pytest.fixture
def carnivore():
    """ Fixture fixing a carnivore."""
    return Carnivore()


@pytest.fixture
def herbivore():
    """ Fixture fixing a herbivore."""
    return Herbivore()


def test_input_param(carnivore):
    """
    Testing that input of new parameter values is possible.
    """
    new_params = {'w_birth': 7.0,
                  'beta': 0.80}

    carnivore.set_parameters(new_params)
    assert carnivore.parameters['w_birth'] == 7.0
    assert carnivore.parameters['beta'] == 0.80


def test_wrong_param(herbivore, carnivore):
    """
    Testing that errors are raised when input parameters are erroneous.
    """
    with pytest.raises(KeyError):
        herbivore.set_parameters({'wbirth': 7.0})

    with pytest.raises(ValueError):
        herbivore.set_parameters({'w_birth': -2.0})

    with pytest.raises(ValueError):
        carnivore.set_parameters({'DeltaPhiMax': -1.0})

    with pytest.raises(ValueError):
        carnivore.set_parameters(({'eta': 1.5}))


def test_value_error_of_age_and_weight():
    """
    Testing whether ValueError is raised for error in input age and weight.
    """
    with pytest.raises(ValueError):
        Herbivore(age=5.25)

    with pytest.raises(ValueError):
        Herbivore(age=-5)

    with pytest.raises(ValueError):
        Carnivore(weight=-1)


def test_fitness_value(herbivore):
    """
    Makes sure the fitness function returns a value from 0 to 1.
    """
    herbivore.update_fitness()
    assert 0 <= herbivore.fitness <= 1


def test_fitness_no_weight(carnivore):
    """
    When the animal's weight is zero, the fitness is also zero.
    """
    carnivore.set_weight(new_weight=0)
    carnivore.update_fitness()
    assert carnivore.fitness == 0


def test_fitness_values_expected(carnivore):
    """
    Testing that the animal fitness is correctly calculated.
    Using age = a_half and weight = weight_half. According to the formula given for fitness,
    see update_fitness() in animals.py for formula, this will result in a fitness of 1/4 (q_pos x q_neg = 1/2 * 1/2)
    """
    carnivore.update_age(years=carnivore.parameters['a_half'])
    carnivore.set_weight(new_weight=carnivore.parameters['w_half'])
    carnivore.update_fitness()

    q_pos = 1 / (1 + (math.exp(carnivore.parameters['phi_age'] * (carnivore.age - carnivore.parameters['a_half']))))
    q_neg = 1 / (1 + (math.exp((-1) * carnivore.parameters['phi_weight'] * (carnivore.weight - carnivore.parameters['w_half']))))

    assert carnivore.fitness == q_pos * q_neg and q_pos * q_neg == 1/4


def test_regains_appetite(carnivore):
    """
    Testing that the regain_appetite() function successfully sets the animal's appetite as parameter F.
    """
    carnivore.appetite = 0
    carnivore.regain_appetite()
    assert carnivore.appetite == carnivore.parameters['F']


def test_certain_birth(mocker, carnivore):
    """
    Testing to ensure birth happens when conditions for birth are met.
    random.random is set to zero and weight at 1000 to ensure the conditions of birthing an offspring are met.
    """
    num = 100
    carnivore.set_weight(new_weight=1000)
    mocker.patch('random.random', return_value=0)

    for _ in range(10):
        assert carnivore.gives_birth(pop_size=num) is not False


@pytest.mark.parametrize('set_carnivore_parameters', [{'gamma': 0.0}], indirect=True)
def test_no_birth(set_carnivore_parameters, carnivore):
    """
    If gamma is set to zero, the birth probability (gamma * fitness * (num - 1)), will be zero.
    Hence, gives_birth() will return False.
    """
    num = 100

    for _ in range(10):
        assert carnivore.gives_birth(pop_size=num) is False


@pytest.mark.parametrize('set_herbivore_parameters', [{'gamma': 100.0, 'zeta': 100}], indirect=True)
def test_no_birth_zeta(set_herbivore_parameters, mocker, herbivore):
    """
    Testing birth to an offspring does not occur if the mother's weight is lower than zeta * (w_birth + sigma_birth).
    """
    num = 100
    mocker.patch('random.random', return_value=0)

    for _ in range(10):
        assert herbivore.gives_birth(pop_size=num) is False


@pytest.mark.parametrize('set_herbivore_parameters', [{'gamma': 100.0, 'xi': 100}], indirect=True)
def test_no_birth_parentweight_too_low(set_herbivore_parameters, mocker, herbivore):
    """
    Testing no birth to offspring occurs if the parent's weight < xi * newborn's weight.
    """
    mocker.patch('random.random', return_value=0)
    num = 200
    h = Herbivore(weight=0.01)

    for _ in range(10):
        assert h.gives_birth(pop_size=num) is False


@pytest.mark.parametrize('set_carnivore_parameters', [{'mu': 100}], indirect=True)
def test_certain_migration(set_carnivore_parameters, carnivore):
    """
    Testing migration does happen if the conditions are met.
    Making sure the animal's fitness * mu > 1 by setting mu to 100 and the animal's fitness to 1.
    """
    # Ensuring the carnivore's fitness is large enough.
    carnivore.fitness = 1
    assert carnivore.migrate() is True


@pytest.mark.parametrize('set_carnivore_parameters', [{'mu': 0}], indirect=True)
def test_cartain_no_migration(set_carnivore_parameters, carnivore):
    """
    Testing migration does not happen by setting mu to zero so random.random > animal's fitness * mu. The function
    should return False in this case.
    """
    assert carnivore.migrate() is False


def test_animal_aging(herbivore, carnivore):
    """
    Testing that Herbivores and Carnivores age with 1 year.
    """
    for n in range(10):
        herbivore.update_age()
        carnivore.update_age()
        assert herbivore.age == n + 1 and carnivore.age == n + 1


def test_animal_metabolism(herbivore, carnivore):
    """
    Testing each animal loses weight with the metabolism function.
    """
    h_weight_before = herbivore.weight
    c_weight_before = carnivore.weight

    herbivore.metabolism()
    carnivore.metabolism()
    assert herbivore.weight < h_weight_before and carnivore.weight < c_weight_before


def test_death_by_too_low_weight(carnivore):
    """ Testing death occurs when the animal's weight is zero. """
    carnivore.set_weight(new_weight=0)
    assert carnivore.dies()


@pytest.mark.parametrize('set_carnivore_parameters', [{'omega': 0.6}], indirect=True)
def test_dies_z_test(set_carnivore_parameters, carnivore):
    """
    Binomial Z-test on the dies()-function with herbivores.

    H0 = The number of times the function returns True, the animal dies, is statistically significant with the
    probability exceeding the set significance level of 0.01 (ALPHA).
    H1 = The function does not return True a statistically significant number of times. We cannot say H0 is true.

    Based on settinkilde.

    """
    random.seed(SEED)
    num = 100
    carnivore.fitness = 0.01
    # Setting fitness so low that probability of death ≈ omega
    p = carnivore.parameters['omega']
    n = sum(carnivore.dies() for _ in range(num))  # True == 1, False == 0

    mean = num * p
    var = math.sqrt(num * p * (1 - p))
    # noinspection PyPep8Naming
    Z = (n - mean) / var
    phi = 2 * stats.norm.cdf(-abs(Z))
    assert phi > ALPHA


def test_certain_death(mocker, herbivore):
    """
    Testing death does happen if the conditions are met.
    Using mocker to set random.random as 0.
    """
    mocker.patch('random.random', return_value=0)
    for _ in range(10):
        assert herbivore.dies() # Trenger ikke is true her?


def test_return_herbivores_feeding(herbivore):
    """
    Testing the herbivore's weight changes as expected after it eats an amount of fodder that is smaller than its
    appetite.
    """
    herbivore.appetite = 8
    weight_before = herbivore.weight
    landscape_fodder = 3
    herbivore.herbivore_feeding(landscape_fodder=landscape_fodder)
    assert herbivore.weight == weight_before + (herbivore.parameters['beta'] * landscape_fodder)


def test_herb_weightchange_fodder(herbivore):
    """
    Testing the herbivore's weight changes as expected after it eats a known amount of fodder.
    """
    weight_before = herbivore.weight
    herbivore.herbivore_feeding(landscape_fodder=herbivore.appetite)
    assert herbivore.weight == weight_before + (herbivore.parameters['beta'] * herbivore.appetite)


def test_herb_fitnesschange_fodder(herbivore):
    """
    Testing the herbivore's fitness changes as expected after it eats.
    """
    fitness_before = herbivore.fitness
    herbivore.herbivore_feeding(landscape_fodder=herbivore.appetite)
    assert herbivore.fitness > fitness_before


def test_carn_nokill(herbivore, carnivore):
    """
    Testing that the carnivore does not kill a herbivore if the herbivore's fitness exceeds the carnivore's fitness.
    """
    # Ensuring herbivore fitness > carnivore fitness
    carnivore.fitness = 0.5
    herbivore.fitness = 1
    assert carnivore.carnivore_feeding(herbivore) is False


@pytest.mark.parametrize('set_carnivore_parameters', [{'DeltaPhiMax': 0.5}], indirect=True)
def test_certain_kill(set_carnivore_parameters, mocker, herbivore, carnivore):
    """
    Testing the carnivore kills the herbivore using mocker to set random.random as 0 and ensuring
    DeltaPhi > DeltaPhiMax, so that the prey probability is 1.
    """
    carnivore.fitness = 1
    herbivore.fitness = 0.1

    mocker.patch('random.random', return_value=0)
    assert carnivore.carnivore_feeding(herbivore) is True


def test_nokill_preyprob(mocker, herbivore, carnivore):
    """
    Testing carnivore does not kill herbivore if the random probability of kill does not exceed the prey probability.
    Setting parameters so the prey probability (fitness carnivore - fitness herbivore) / DeltaPhiMax <= 1.
    """
    herbivore.fitness = 0.3
    carnivore.fitness = 0.8
    mocker.patch('random.random', return_value=1)

    for _ in range(10):
        assert carnivore.carnivore_feeding(herbivore) is False
