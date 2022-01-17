"""
Module implementing animals on the island.
"""

import random
import math


class Animals:
    """
    Superclass for animals.

    Subclasses:
    * Herbivore
    * Carnivore
    """

    @classmethod
    def set_parameters(cls, new_params):
        """
        set class parameters.

        :param new_params: new parameter values.
        :type new_params: dict
        """

        for key in new_params:
            if key not in cls.parameters:
                raise KeyError('Invalid parameter name: ' + key)

        for key in new_params:
            if new_params[key] < 0:
                raise ValueError('All parameter values need to be positive')

        cls.parameters.update(new_params)

    def __init__(self, age=None, weight=None):
        """
        Initializing animal objects.

        :param age: age of animal
        :type age: float
        :param weight: weight of animal
        :type weight: float
        """
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
        Function calculating the fitness of animals based on weight and age. If weight is 0, fitness is 0, else

        .. math::
        q^{+}(a, a_{\\frac{1}{2}}, \\phi_{age}) \\times q^{-}(w, w_{\\frac{1}{2}}, \\phi_{weight})

        where

        q^{\\pm}(x, x_{\\frac{1}{2}}, \\phi) = \\frac{1}{1 + e^{\\pm \\phi(x-x_{\\frac{1}{2}})}}

        Fitness will always be between 0 and 1.
        """
        if self.weight <= 0:
            self.fitness = 0
        else:
            a_half = self.parameters['a_half']
            phi_age = self.parameters['phi_age']
            w_half = self.parameters['w_half']
            phi_weight = self.parameters['phi_weight']

            q_pos = 1 / (1 + (math.exp(phi_age * (self.age - a_half))))
            q_neg = 1 / (1 + (math.exp((-1) * phi_weight * (self.weight - w_half))))

            self.fitness = q_pos * q_neg


    def regain_appetite(self):
        """
        An animals appetite is set to the animal's parameter 'F' when function is called upon.
        """
        # noinspection PyAttributeOutsideInit
        self.appetite = self.parameters['F']

    # noinspection PyPep8Naming
    def gives_birth(self, pop_size):
        """
        Decides whether an animal gives birth. The probability of giving birth to an offspring in a year
        is 0 if the weight is :math:``\\omega < \\xi(w_{birth} + \\sigma_{birth})``.
        Else the probability is :math:``\\gamma \\times \\phi \\times \\(\\textit{pop_size} - 1)``.
        If the animal gets an offspring, the animal's weight is updated with
        :math:``\\xi \\times \\text{newborn's weight}``, and the fitness is updated accordingly.

        :param pop_size: number of animals of the same species in a cell.
        :return: newborn of class Herbivore or Carnivore, if animal is born.
                 False if no animal is born.
        :rtype: bool or object

        """
        preg_prob = min(1, self.parameters['gamma'] * self.fitness * (pop_size - 1))

        if random.random() < preg_prob:
            newborn = type(self)()
            if self.weight < self.parameters['xi'] * newborn.weight:
                return False
            else:
                self.weight -= self.parameters['xi'] * newborn.weight
                self.update_fitness()
                return newborn

        else:
            return False

    def migrate(self):
        """
        Function determines if animals migrate or not.
        An animal moves with a probability of :math:``\\mu \\times \\phi``.

        :return: True, if animal migrates.
                 False, if animal does not migrate.
        :rtype: bool
        """
        if random.random() < self.parameters['mu']*self.fitness:
            return True
        else:
            return False

    def update_age(self, years=None):
        """
        Updates age of animal, and updates fitness accordingly.

        :param years: number of years the animal ages.
        :type years: int or None
        """
        self.age += years if years is not None else 1
        self.update_fitness()

    def metabolism(self):
        """
        Updates animal weight which is due to annual weightloss, :math:``\\eta \\times \\textit{weight}``,
        and updates fitness accordingly.
        """
        self.weight -= self.parameters['eta']*self.weight
        self.update_fitness()

    def dies(self):
        """
        Decides whether an animal dies. An animal dies with certainty if their weight is 0,
        or with a probability of :math:``\\omega(1-\\phi)``.

        :return: True, if animal dies. False, if animal does not die.
        :rtype: bool
        """
        if self.weight <= 0:
            return True
        else:
            omega = self.parameters['omega']
            return random.random() < (omega*(1 - self.fitness))

    def set_weight(self, new_weight):
        """
        Function allowing to enter new weight for animal when function is called upon.
        """
        self.weight = new_weight


class Herbivore(Animals):
    """
    Subclass for herbivores.
    """

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
        Decides how much fodder each herbivore gets, and updates weight and fitness accordingly.
        Weight is updated with a factor of :math:``\\beta \\times \\text{fodderamount}``

        :param landscape_fodder: amount of fodder available for herbivore.
        :type landscape_fodder: float

        :return: the herbivore's portion.
        :rtype: float
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
                  'w_half': 4.0, 'phi_weight': 0.4,
                  'mu': 0.4, 'gamma': 0.8,
                  'zeta': 3.5, 'xi': 1.1,
                  'omega': 0.8, 'F': 50.0,
                  'DeltaPhiMax': 10.0}

    def carnivore_feeding(self, herbivore):
        """
        Decides how much food each carnivore gets, and updates their weight and fitness accordingly.

        :param herbivore: A herbivore in the same cell as the carnivore.
        :type herbivore: object

        :return: True if the carnivore kills the herbivore, and false if it doesn't
        :rtype: bool
        """
        if self.fitness <= herbivore.fitness:
            return False

        delta_phi = self.fitness - herbivore.fitness
        if 0 < delta_phi < self.parameters['DeltaPhiMax']:
            prey_prob = delta_phi / self.parameters['DeltaPhiMax']
        else:
            prey_prob = 1

        if random.random() < prey_prob:
            self.appetite -= herbivore.weight
            self.weight += self.parameters['beta']*herbivore.weight
            self.update_fitness()
            return True
        else:
            return False
