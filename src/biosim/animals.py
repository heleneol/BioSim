"""
Template for Animals class.
"""
import random
import math
from general import animal_const, getnestdict


class herbivore:

    def __init__(self, age=None, weight=None):
        self.classname = self.__class__.__name__

        self.age = age if age is not None else 0
        random_weight = random.gauss(getnestdict(animal_const, self.classname, 'w_birth'), getnestdict(animal_const, self.classname, 'sigma_birth'))
        self.weight = weight if weight is not None else random_weight
        self.fitness = None

    def update_age(self, years=None):
        self.age += years if years is not None else 1

    def update_weight(self, fooder):
        beta = getnestdict(animal_const, self.classname, 'beta')
        eta = getnestdict(animal_const, self.classname, 'eta')
        self.weight = (beta*fooder) - (eta*self.weight)

#    def update_fitness(self):
#        a_half = getnestdict(animal_const, self.classname, 'a_half')
#        phi_age = getnestdict(animal_const, self.classname, 'phi_age')
#        w_half = getnestdict(animal_const, self.classname, 'w_half')
#        phi_weight = getnestdict(animal_const, self.classname, 'phi_weight')
#
#        q_pos = (1/(1 + math.exp(phi_age*(self.age - a_half))))
#        q_neg = (1/(1 + math.exp(-phi_weight*(self.weight - w_half))))
#
#        if self.weight <= 0:
#            self.fitness = 0
#
#        else:
#            self.fitness = q_pos * q_neg
#
#        if self.fitness > 1:
#            self.fitness = 1

'''
    def update_fitness(self):
        def q(x, x_half, phi, sign):
            if sign == 'pos':
                return (1 / (1 + (math.exp(phi * (x - x_half)))))
            elif sign == 'neg':
                return (1 / (1 + (math.exp((-1) * phi * (x - x_half)))))

        if self.weight <= 0:
            self.fitness = 0
        else:
            a_half = getnestdict(animal_const, self.classname, 'a_half')
            phi_age = getnestdict(animal_const, self.classname, 'phi_age')
            w_half = getnestdict(animal_const, self.classname, 'w_half')
            phi_weight = getnestdict(animal_const, self.classname, 'phi_weight')
            self.fitness = (q(self.age, a_half, phi_age, 'pos') * q(self.weight, w_half, phi_weight, 'neg'))
            if self.fitness > 1:
                self.fitness = 1'''

h1 = herbivore()
for year in range(10):
    print(f'Year: {year}, age is {h1.age} and weight is {h1.weight}')
    h1.update_age()
    h1.update_weight(fooder=13)
    h1.update_fitness()
