"""
Template for Animals class.
"""
import random
import math


class Herbivore:

    parametres = {'w_birth': 8.0, 'sigma_birth': 1.5,
                    'beta': 0.9, 'eta': 0.05,
                    'a_half ': 40.0, 'phi_age': 0.6,
                    'w_half': 10.0, 'phi_weight': 0.1,
                    'mu': 0.25, 'gamma': 0.2,
                    'zeta': 3.5, 'xi': 1.2,
                    'omega': 0.4, 'F': 10.0,
                    'DeltaPhiMax': None}
    @classmethod
    def set_params(cls, new_parametres):
        for key in new_parametres:
            if key not in parametres.keys():
                raise KeyError('Invalid parameter name: ' + key)

    @classmethod
    def get_params(cls):



    def __init__(self, age=None, weight=None, parametres = None):
        self.age = age if age is not None else 0
        random_weight = random.gauss(self.parametres.get('w_birth'), self.parametres.get('sigma_birth'))
        self.weight = weight if weight is not None else random_weight
        self.update_fitness()


    def update_age(self, years=None):
        self.age += years if years is not None else 1

    def update_weight(self, fooder):
        beta = parametres.get('beta')
        eta = parametres.get('eta')
        self.weight = (beta*fooder) - (eta*self.weight)


    def update_fitness(self):
        def q(x, x_half, phi, sign):
            if sign == 'pos':
                return (1 / (1 + (math.exp(phi * (x - x_half)))))
            elif sign == 'neg':
                return (1 / (1 + (math.exp((-1) * phi * (x - x_half)))))

        if self.weight <= 0:
            self.fitness = 0
        else:
            a_half = parametres.get('a_half')
            phi_age = parametres.get('phi_age')
            w_half = parametres.get('w_half')
            phi_weight = parametres.get('phi_weight')
            self.fitness = (q(self.age, a_half, phi_age, 'pos') * q(self.weight, w_half, phi_weight, 'neg'))
            if self.fitness > 1:
                self.fitness = 1

class carnivore:
    parametres = {'w_birth': 6.0, 'sigma_birth': 1.0,
                    'beta': 0.75, 'eta': 0.125,
                    'a_half ': 40.0, 'phi_age': 0.3,
                    'w_half': 4.0, 'phi_weight': 00.4,
                    'mu': 0.4, 'gamma': 0.8,
                    'zeta': 3.5, 'xi': 1.1,
                    'omega': 0.8, 'F': 50.0,
                    'DeltaPhiMax': 10.0}


h1 = Herbivore()
for year in range(10):
    print(f'Year: {year}, age is {h1.age} and weight is {h1.weight}, fitness {h1.fitness}')
    h1.update_age()
    h1.update_weight(fooder=13)
    h1.update_fitness()
