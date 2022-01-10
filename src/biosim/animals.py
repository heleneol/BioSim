"""
Template for Animals class.
"""
import random
import math


class Herbivore:


    parameters = {  'w_birth': 8.0, 'sigma_birth': 1.5,
                    'beta': 0.9, 'eta': 0.05,
                    'a_half': 40.0, 'phi_age': 0.6,
                    'w_half': 10.0, 'phi_weight': 0.1,
                    'mu': 0.25, 'gamma': 0.2,
                    'zeta': 3.5, 'xi': 1.2,
                    'omega': 0.4, 'F': 10.0,
                    'DeltaPhiMax': None}

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


        cls.parameters.update(new_params)


    def __init__(self, age=None, weight=None):
        self.age = age if age is not None else 0
        random_weight = random.gauss(self.parameters['w_birth'], self.parameters['sigma_birth'])
        self.weight = weight if weight is not None else random_weight
        self.update_fitness()


    def update_age(self, years=None):
        """
        Updates age of animal

        Parameters
        ----------
        int:
            number of years to age, 1 if None is spesified
        """
        self.age += years if years is not None else 1

    def herbivore_feeding(self, fodder):

        self.weight = (self.parameters['beta']*fodder)
        self.update_fitness()

    def update_fitness(self):
        def q(x, x_half, phi, sign):
            if sign == 'pos':
                return (1 / (1 + (math.exp(phi * (x - x_half)))))
            elif sign == 'neg':
                return (1 / (1 + (math.exp((-1) * phi * (x - x_half)))))

        if self.weight <= 0:
            self.fitness = 0
        else:
            a_half = self.parameters['a_half']
            phi_age = self.parameters['phi_age']
            w_half = self.parameters['w_half']
            phi_weight = self.parameters['phi_weight']
            self.fitness = (q(self.age, a_half, phi_age, 'pos') * q(self.weight, w_half, phi_weight, 'neg'))
            if self.fitness > 1:
                self.fitness = 1

    def dies(self):
        if self.weight < 0:
            return True
        else:
            omega = self.parameters['omega']
            return random.random() < (omega*(1 - self.fitness))

    def gives_birth(self, N):
        preg_prob = min(1, self.parameters['gamma'] * self.fitness * (N - 1))

        if random.random() < preg_prob:
            newborn = Herbivore()
            if self.weight < self.parameters['xi'] * newborn.weight:
                return None
            else:
                self.weight -= self.parameters['xi'] * newborn.weight
                return newborn
        else:
            return None










class Carnivore(Animal):
    parameters = {  'w_birth': 6.0, 'sigma_birth': 1.0,
                    'beta': 0.75, 'eta': 0.125,
                    'a_half ': 40.0, 'phi_age': 0.3,
                    'w_half': 4.0, 'phi_weight': 00.4,
                    'mu': 0.4, 'gamma': 0.8,
                    'zeta': 3.5, 'xi': 1.1,
                    'omega': 0.8, 'F': 50.0,
                    'DeltaPhiMax': 10.0}

    def __init__(self):





