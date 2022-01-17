"""Tests for the Animal class provided in biosim/src/animals.py """

import pytest
import scipy.stats as stats

from src.biosim.animals import *

# Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests
ALPHA = 0.01  # significance level for statistical tests

@pytest.fixture
def set_herbivore_parameters(request):
    """
    Fixture setting class parameters on Herbivore, based on H. E. Plesser's biolab/bacteria.py

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
    Fixture setting class parameters on Carnivore, based on H. E. Plesser's biolab/bacteria.py.

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

## ??? Skriv test for DeltaPhiMax!!

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

    for _ in range(10):
        herb.update_fitness()
        assert 0 <= herb.fitness <= 1


def test_fitness_no_weight():  # Slette?:
    """
    When the animal's weight is zero, the fitness is also zero.
    """
    carn = Carnivore()
    carn.set_weight(new_weight=0)

    for _ in range(10):
        carn.update_fitness()
        assert carn.fitness == 0


# Could we write 1/4 here?
def test_fitness_values():
    """
    Testing that the animal fitness is correctly calculated.
    Using age = a_half and weight = weight_half. According to the formula given for fitness,
    see update_fitness() in animals.py for formula, this will result in a fitness of 1/4 (q_pos x q_neg = 1/2 * 1/2)
    """
    carn = Carnivore(age=20, weight=10)
    #herb.update_age(years=herb.parameters['a_half'])
    #herb.set_weight(new_weight=herb.parameters['w_half'])

    #q_pos = 1 / (1 + (math.exp(herb.parameters['phi_age'] * (herb.age - herb.parameters['a_half']))))
    #q_neg = 1 / (1 + (math.exp((-1) * herb.parameters['phi_weight'] * (herb.weight - herb.parameters['w_half']))))

    q_pos = 1 / (1 + (math.exp(carn.parameters['phi_age'] * (carn.age - carn.parameters['a_half']))))
    q_neg = 1 / (1 + (math.exp((-1) * carn.parameters['phi_weight'] * (carn.weight - carn.parameters['w_half']))))

    for _ in range(20):
        carn.update_fitness()
        assert carn.fitness == q_pos * q_neg

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
    Testing to ensure birth happens when conditions for birth are met.
    Mocker ensures random.random returns the value zero. Weight is set at 1000 to ensure it always surpasses
    xi*newborn.weight. With these conditions the function should not return False (False meaning no offspring).
    """
    num = 100
    carn = Carnivore(weight=1000)
    mocker.patch('random.random', return_value=0)

    for _ in range(10):
        assert carn.gives_birth(pop_size=num) is not False


@pytest.mark.parametrize('set_carnivore_parameters', [{'gamma': 0.0}], indirect=True)
def test_no_birth(set_carnivore_parameters):
    """
    If gamma is set to zero, the birth probability (gamma * fitness * (num - 1)), will be zero.
    Hence, gives_birth() will return None.
    """
    carn = Carnivore()
    num = 100

    for _ in range(10):
        assert carn.gives_birth(pop_size=num) is False


@pytest.mark.parametrize('set_carnivore_parameters', [{'gamma': 100.0, 'xi': 100}], indirect=True)
def test_no_birth_parentweight_too_low(set_carnivore_parameters, mocker):
    """
    Testing no birth to offspring occurs if the parent's weight < zeta * newborn's weight.
    Setting parameters so random.random < gamma * fitness * (N-1). The animal's weight and xi are set so weight will
    always be lower than xi * newborn's weight.
    """
    mocker.patch('random.random', return_value=0)
    h = Herbivore(weight=0.01)

    for _ in range(10):
        assert h.gives_birth(pop_size=200) is False


@pytest.mark.parametrize('set_carnivore_parameters', [{'mu': 100}], indirect=True)
def test_certain_migration(set_carnivore_parameters):
    """
    Testing migration does happen if the conditions are met.
    Making sure the animal's fitness * mu > 1 by setting mu to 100 and the animal's fitness to 1. Migration should,
    with these conditions, always happen.
    """
    carn = Carnivore()
    # Ensuring the carnivore's fitness is large enough.
    carn.fitness = 1
    for _ in range(10):
        assert carn.migrate() is True


@pytest.mark.parametrize('set_carnivore_parameters', [{'mu': 0}], indirect=True)
def test_cartain_no_migration(set_carnivore_parameters):
    carn = Carnivore()
    for _ in range(10):
        assert carn.migrate() is False


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

    for _ in range(10):
        herb.metabolism()
        carn.metabolism()
        assert herb.weight < h_weight_before
        assert carn.weight < c_weight_before


def test_death_by_too_low_weight():
    """ Testing death occurs when the animal's weight is zero. """
    carn = Carnivore()
    carn.set_weight(new_weight=0)
    assert carn.dies()


@pytest.mark.parametrize('set_carnivore_parameters', [{'omega': 0.6}], indirect=True)
def test_dies_z_test(set_carnivore_parameters):
    """
    Binomial Z-test on the dies()-function with herbivores.

    H0 = The number of times the function returns True, the animal dies, is statistically significant with the
    probability exceeding the set significance level of 0.01 (ALPHA).
    H1 = The function does not return True a statistically significant number of times. We cannot say H0 is true.

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
    phi = 2 * stats.norm.cdf(-abs(Z))
    assert phi > ALPHA

# Test gives_birth():
# kanskje en statistisk test som sjekker om fordelingen er som forventet
# Test if self.weight<xi*newborn.weight returns None, and if species is herbivore it runs Herbivore()


def test_certain_death(mocker):
    """
    Testing death does happen if the conditions are met.
    Using mocker to set random.random as 0.
    """
    herb = Herbivore()
    mocker.patch('random.random', return_value=0)
    for _ in range(10):
        assert herb.dies() # Trenger ikke is true her?


def test_return_herbivores_feeding():
    """
    Testing the herbivore's weight changes as expected after it eats an amount of fodder that is smaller than its
    appetite.
    """
    herb = Herbivore()
    herb.appetite = 8
    weight_before = herb.weight

    landscape_fodder = 3
    herb.herbivore_feeding(landscape_fodder=landscape_fodder)
    assert herb.weight == weight_before + (herb.parameters['beta'] * landscape_fodder)


def test_herb_weightchange_fodder():
    """
    Testing the herbivore's weight changes as expected after it eats a known amount of fodder.
    """
    herb = Herbivore()
    weight_before = herb.weight
    herb.herbivore_feeding(landscape_fodder=herb.appetite)
    assert herb.weight == weight_before + (herb.parameters['beta'] * herb.appetite)


def test_herb_fitnesschange_fodder():
    """
    Testing the herbivore's fitness changes as expected after it eats.
    """
    herb = Herbivore()
    fitness_before = herb.fitness

    herb.herbivore_feeding(landscape_fodder=herb.appetite)
    assert herb.fitness > fitness_before


def test_carn_nokill():
    """
    Testing that the carnivore does not kill a herbivore if the herbivore's fitness exceeds the carnivore's fitness.
    """
    carn = Carnivore()
    herb = Herbivore()

    # Ensuring herbivore fitness > carnivore fitness
    carn.fitness = 0.5
    herb.fitness = 1

    for _ in range(10):
        assert carn.carnivore_feeding(herb) is False


@pytest.mark.parametrize('set_carnivore_parameters', [{'DeltaPhiMax': 0.5}], indirect=True)
def test_certain_kill(set_carnivore_parameters, mocker):
    """
    Testing the carnivore kills the herbivore using mocker to set random.random as 0 and ensuring
    DeltaPhi > DeltaPhiMax, so that the prey probability is 1.
    """
    carn = Carnivore()
    herb = Herbivore()

    carn.fitness = 1
    herb.fitness = 0.1

    mocker.patch('random.random', return_value=0)
    for _ in range(10):
        assert carn.carnivore_feeding(herb) is True


def test_nokill_preyprob(mocker):
    """
    Testing carnivore does not kill herbivore if the random probability of kill does not exceed the prey probability.
    Setting parameters so the prey probability (fitness carnivore - fitness herbivore) / DeltaPhiMax <= 1.
    """
    h = Herbivore()
    c = Carnivore()

    h.fitness = 0.3
    c.fitness = 0.8

    mocker.patch('random.random', return_value=1)

    for _ in range(10):
        assert c.carnivore_feeding(h) is False
