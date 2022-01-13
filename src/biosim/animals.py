"""
Template for Animals class.
"""
import random
import math


class Animals:
    """ Superclass for herbivores and carnivores """

    @classmethod
    def set_parameters(cls, new_params):
        """
        set class parameters.

        Parameters
        ________
        new_params: dict

        Raises
        ________
        KeyError
        """

        for key in new_params:
            if key not in cls.parameters:
                raise KeyError('Invalid parameter name: ' + key)

        for value in new_params:
            if new_params[value] < 0:
                raise ValueError('All parameter values need to be positive')  # Er dette sant?

        cls.parameters.update(new_params)

    def __init__(self, age=None, weight=None):
        self.classname = self.__class__.__name__

        self.age = age if age is not None else 0
        if self.age < 0:
            raise ValueError('Animal age has to be >= 0')

        random_weight = random.gauss(self.parameters['w_birth'], self.parameters['sigma_birth'])
        self.weight = weight if weight is not None else random_weight
        if self.weight <= 0:
            raise ValueError('Animal weight has to be >= 0')

        self.update_fitness()
        self.regain_appetite()

    def update_fitness(self):
        """
        Function calculating the fitness to animals based on weight and age.
        """
        def q(x, x_half, phi, sign):
            if sign == 'pos':
                return 1 / (1 + (math.exp(phi * (x - x_half))))
            elif sign == 'neg':
                return 1 / (1 + (math.exp((-1) * phi * (x - x_half))))

        if self.weight <= 0:
            self.fitness = 0
        else:
            a_half = self.parameters['a_half']
            phi_age = self.parameters['phi_age']
            w_half = self.parameters['w_half']
            phi_weight = self.parameters['phi_weight']
            self.fitness = (q(self.age, a_half, phi_age, 'pos') * q(self.weight, w_half, phi_weight, 'neg'))
            if self.fitness > 1:
                # noinspection PyAttributeOutsideInit
                self.fitness = 1

    def regain_appetite(self):
        # noinspection PyAttributeOutsideInit
        self.appetite = self.parameters['F']

    # noinspection PyPep8Naming
    def gives_birth(self, N):
        """
        Decides whether an animal gives birth.

        Parameter
        ----------
        N: number of animals in a population

        """
        preg_prob = min(1, self.parameters['gamma'] * self.fitness * (N - 1))

        if random.random() < preg_prob:
            if self.classname == 'Herbivore':
                newborn = Herbivore()
            else:
                newborn = Carnivore()
            if self.weight < self.parameters['xi'] * newborn.weight:
                return None
            else:
                self.weight -= self.parameters['xi'] * newborn.weight
                self.update_fitness()
                return newborn
        else:
            return None

    # def migrate(self): ObsObs pass på at alle age-r riktig når de migrerer.

    def update_age(self, years=None):
        """
        Updates age of animal.

        Parameters
        ----------
        years:
            number of years to age, 1 if None is specified
        """
        self.age += years if years is not None else 1
        self.update_fitness()

    def metabolism(self):
        """
        Updates animal weight which is due to annual weightloss.
        """
        self.weight -= self.parameters['eta']*self.weight
        self.update_fitness()

    def dies(self):
        """
        Decides whether an animal dies.
        """
        if self.weight <= 0:
            return True
        else:
            omega = self.parameters['omega']
            return random.random() < (omega*(1 - self.fitness))

    def set_weight(self, new_weight):
        self.weight = new_weight


class Herbivore(Animals):
    """ Subclass for herbivores. """

    parameters = {'w_birth': 8.0, 'sigma_birth': 1.5,
                  'beta': 0.9, 'eta': 0.05,
                  'a_half': 40.0, 'phi_age': 0.6,
                  'w_half': 10.0, 'phi_weight': 0.1,
                  'mu': 0.25, 'gamma': 0.2,
                  'zeta': 3.5, 'xi': 1.2,
                  'omega': 0.4, 'F': 10.0,
                  'DeltaPhiMax': None}

    def herbivore_feeding(self, landscape_fodder):
        """
        Decides how much food each herbivore gets, and updates weight and fitness accordingly.

        Parameter
        ----------
        landscape_fodder:

        """

        if 0 < landscape_fodder < self.appetite:
            herbivore_portion = landscape_fodder
        else:
            herbivore_portion = self.appetite

        self.weight += self.parameters['beta']*herbivore_portion
        self.update_fitness()

        return herbivore_portion


class Carnivore(Animals):
    """ Subclass for carnivores. """

    parameters = {'w_birth': 6.0, 'sigma_birth': 1.0,
                  'beta': 0.75, 'eta': 0.125,
                  'a_half': 40.0, 'phi_age': 0.3,
                  'w_half': 4.0, 'phi_weight': 00.4,
                  'mu': 0.4, 'gamma': 0.8,
                  'zeta': 3.5, 'xi': 1.1,
                  'omega': 0.8, 'F': 50.0,
                  'DeltaPhiMax': 10.0}

    def carnivore_feeding(self, herb):
        """
        Decides how much food each carnivore gets, and updates their weight and fitness accordingly.
        """
        if self.fitness <= herb.fitness:
            return True

        delta_phi = self.fitness - herb.fitness
        if 0 < delta_phi < self.parameters['DeltaPhiMax']:
            prey_prob = delta_phi / self.parameters['DeltaPhiMax']
        else:
            prey_prob = 1

        if random.random() < prey_prob:
            self.appetite -= herb.weight
            self.weight += self.parameters['beta']*herb.weight
            self.update_fitness()
            return False

        else:
            return True
