"""
Template for Animals class.
"""
import random
from general import animal_const and getnestdict







class herbivore:


    def __init__(self, age = None, weight = None):
        self.classname = self.__class__.__name__
        self.age = age if age is not None else 0
        random_weight = random.gauss(getnestdict(animal_const, self.classname, 'w_birth'), getnestdict(animal_const, self.classname, 'sigma_birth'))
        self.weight = weight if weight is not None else random_weight

    def update_age(self):
        self.age += 1

    def update_weight(self):
        a = 2



    def update_fitness(self):
        a = 2


h1 = herbivore(age= 2, weight= 4)
print(f'age = {h1.age} and weight = {h1.weight}')



