"""
Module implementing animals on the island.
"""

import random
import math


class Animals:
    """
    Superclass for animals.

    Subclasses:
    * :class:`Herbivore`
    * :class:`Carnivore` *

    """

    @classmethod
    def set_parameters(cls, new_params):
        r"""
        Set class parameters. \n
        Parametre DeltaPhiMax can only be set for Carnivores and must be :math:`\Delta \Phi_{max} > 0`.
        Parametre eta must be :math:`\eta >= 0`.

        :param new_params: new parameter values.
        :type new_params: dict

        """

        for key in new_params:
            if key not in cls.parameters:
                raise KeyError('Invalid parameter name: ' + key)

            elif key == 'DeltaPhiMax':
                if cls.parameters[key] is None:
                    continue
                else:
                    if new_params[key] <= 0:
                        raise ValueError('DeltaPhiMax must be strictly positive!')

            elif key == 'eta':
                if new_params[key] > 1:
                    raise ValueError('Eta must be <= 1 !')
                else:
                    continue

            elif new_params[key] < 0:
                raise ValueError('All parameter values need to be positive')

        cls.parameters.update(new_params)

    def __init__(self, age=None, weight=None):
        """
        Initializing animal objects. Objects get age, weight, fitness and apatite be default.

        :param age: age of animal
        :type age: float
        :param weight: weight of animal
        :type weight: float

        """
        self.classname = self.__class__.__name__

        self.age = age if age is not None else 0
        if self.age < 0 or self.age // 1 != self.age:
            raise ValueError('Animal age has to be an integer >= 0')

        random_weight = random.gauss(self.parameters['w_birth'], self.parameters['sigma_birth'])
        self.weight = weight if weight is not None else random_weight
        if self.weight < 0:
            raise ValueError('Animal weight has to be a positive number')

        self.update_fitness()

        self.regain_appetite()

    def update_fitness(self):
        r"""
        Function calculating the fitness :math:`(\Phi)` of animals based on weight and age.

        If :math:`w <= 0`, :math:`\Phi = 0`

        Else, :math:`\Phi =  q^{+}(a, a_{\frac{1}{2}}, \Phi_{age}) * q^{-}(w, w_{\frac{1}{2}}, \Phi_{weight})`

        where: :math:`q^{\pm}(x, x_half, \Phi) = \frac{1}{1 + e^{\pm\Phi(x-x_{\frac{1}{2}})}}`

        Fitness will always be :math:`0 <= \Phi <= 1`.
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
        Animals appetite is set to the animal's parameter 'F' when function is called upon.

        """
        # noinspection PyAttributeOutsideInit
        self.appetite = self.parameters['F']

    def gives_birth(self, pop_size):
        r"""
        Decides whether an animal gives birth.

        If :math:`w < \zeta(w_{birth} + \sigma_{birth})`, :math:`p_{birth} = 0`,

        also :math:`w < \xi * \textit{newborn's weight}` :math:`p_{birth} = 0`.

        Else :math:`p_{birth} = \gamma * \Phi * (N - 1)`

        where: N is the population size.

        If the animal gets an offspring, the animal's weight is updated with
        :math:`\xi * \text{newborn's weight}`, and the fitness is updated accordingly.

        :param pop_size: number of animals of the same species in a cell.
        :return: newborn of class Herbivore or Carnivore, if animal is born.
                 False if no animal is born.
        :rtype: bool or object

        """
        preg_prob = min(1, self.parameters['gamma'] * self.fitness * (pop_size - 1))

        if random.random() < preg_prob:
            newborn = type(self)()
            if self.weight < self.parameters['zeta'] * (self.parameters['w_birth'] + self.parameters['sigma_birth']):
                return False
            elif self.weight < self.parameters['xi'] * newborn.weight:
                return False
            else:
                self.weight -= self.parameters['xi'] * newborn.weight
                self.update_fitness()
                return newborn

        else:
            return False

    def migrate(self):
        r"""
        Function determines if animals migrate or not.
        An animal moves with a probability of :math:`p_{move} = \mu * \Phi`.

        :return: True, if animal migrates.
                 False, if animal does not migrate.
        :rtype: bool

        """
        if random.random() < self.parameters['mu'] * self.fitness:
            return True
        else:
            return False

    def update_age(self, years=None):
        """
        Updates age of animal, and updates fitness accordingly.
        If years is none the animal will age 1 year else it will age with given amount

        :param years: number of years the animal ages.
        :type years: int or None

        """
        self.age += years if years is not None else 1
        self.update_fitness()

    def metabolism(self):
        r"""
        Updates animal weight which is due to annual weightloss,
        :math:`w_{loss} = \eta * w`, and updates fitness accordingly.

        """
        self.weight -= self.parameters['eta'] * self.weight
        self.update_fitness()

    def dies(self):
        r"""
        Decides whether an animal dies.

        If :math:`w = 0`, :math:`p_{death} = 1`,

        else, :math:`p_{death} = \omega(1-\Phi)`

        :return: True, if animal dies. False, if animal does not die.
        :rtype: bool

        """
        if self.weight <= 0:
            return True
        else:
            return random.random() < (self.parameters['omega'] * (1 - self.fitness))

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
        r"""
        Decides how much fodder each herbivore gets, and updates weight and fitness accordingly.
        Weight is updated with a factor of :math:`\beta * w_{portion}`

        :param landscape_fodder: amount of fodder available for herbivore.
        :type landscape_fodder: float

        :return: the herbivore's portion.
        :rtype: float

        """

        if 0 < landscape_fodder < self.appetite:
            herbivore_portion = landscape_fodder
        else:
            herbivore_portion = self.appetite

        self.weight += self.parameters['beta'] * herbivore_portion
        self.update_fitness()

        return herbivore_portion


class Carnivore(Animals):
    """
    Subclass for carnivores.

    """

    parameters = {'w_birth': 6.0, 'sigma_birth': 1.0,
                  'beta': 0.75, 'eta': 0.125,
                  'a_half': 40.0, 'phi_age': 0.3,
                  'w_half': 4.0, 'phi_weight': 0.4,
                  'mu': 0.4, 'gamma': 0.8,
                  'zeta': 3.5, 'xi': 1.1,
                  'omega': 0.8, 'F': 50.0,
                  'DeltaPhiMax': 10.0}

    def carnivore_feeding(self, herb):
        r"""
        Decides weather or not a carnivore killes a herbivore.

        If :math:`\Phi_{carn} <= \Phi_{herb}`, :math:`p_{kill}=0`,

        also if :math:`0 < \Delta \Phi < \Delta \Phi_{max}`, :math:`p_{kill} = \frac{\Delta \Phi}{\Delta \Phi_{max}}`

        where: :math:`\Delta \Phi = \Phi_{carn} - \Phi_{herb}`

        If a kill is confirmed the carnivores appetite, weight and fitness is updated.

        :param herb: A herbivore in the same cell as the carnivore.
        :type herb: object

        :return: True if the carnivore kills the herbivore, and false if it doesn't
        :rtype: bool

        """
        if self.fitness <= herb.fitness:
            return False
        delta_phi = self.fitness - herb.fitness
        if 0 < delta_phi < self.parameters['DeltaPhiMax']:
            prey_prob = delta_phi / self.parameters['DeltaPhiMax']
        else:
            prey_prob = 1
        if random.random() < prey_prob:
            if 0 < self.appetite < herb.weight:
                carn_portion = self.appetite
            else:
                carn_portion = herb.weight
            self.appetite -= carn_portion
            self.weight += self.parameters['beta'] * carn_portion
            self.update_fitness()
            return True
        else:
            return False
