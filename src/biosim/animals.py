"""
Template for Animals class.
"""
import random
import math
from .general import animal_const, getnestdict


class herbivore:


    def __init__(self, age = None, weight = None):
        self.classname = self.__class__.__name__

        self.age = age if age is not None else 0
        random_weight = random.gauss(getnestdict(animal_const, self.classname, 'w_birth'), getnestdict(animal_const, self.classname, 'sigma_birth'))
        self.weight = weight if weight is not None else random_weight

        def calc_fitness(self):
        # fitness
            def q(x, x_half, phi, sign):
                if sign == 'pos':
                    return (1 / (1 + (math.exp(phi * (x - x_half)))))
                elif sign == 'neg':
                    return (1 / (1 + (math.exp(-phi * (x - x_half)))))

            if self.weight <= 0:
                self.fitness = 0
            else:
                a_half = getnestdict(animal_const, self.classname, 'a_half')
                phi_age = getnestdict(animal_const, self.classname, 'phi_age')
                w_half = getnestdict(animal_const, self.classname, 'w_half')
                phi_weight = getnestdict(animal_const, self.classname, 'phi_weight')
                self.fitness = (q(self.age, a_half, phi_age, 'pos')*q(self.weight, w_half, phi_weight, 'neg'))
                if self.fitness > 1:
                    self.fitness = 1
            return self.fitness

        self.fitness = calc_fitness(self.age, self.weight,self.classname)

    def update_age(self, years=None):
        self.age += years if years is not None else 1

    def update_weight(self):
        a = 2

    def update_fitness(self):
        self.fitness = calc_fitness(self)



h1 = herbivore(age= 2, weight= 4)
h2 = herbivore()
print(f'age = {h1.age}, weight = {h1.weight}, fitness = {h1.fitness}')
h2.update_age()
print(f'age = {h2.age},weight = {h2.weight}, fitness = {h2.fitness}')



