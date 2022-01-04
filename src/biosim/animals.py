"""
Template for Animals class.
"""
import random

animal_const = {'herbivore': {'w_birth' : 8.0 ,
                            'sigma_birth' : 1.5 ,
                            'beta' : 0.9 ,
                            'eta' : 0.05 ,
                            'a_half ' : 40.0 ,
                            'phi_age' : 0.6 ,
                            'w_half' : 10.0 ,
                            'phi_weight' : 0.1 ,
                            'mu' : 0.25 ,
                            'gamma' : 0.2 ,
                            'zeta' : 3.5 ,
                            'xi' : 1.2 ,
                            'omega' : 0.4 ,
                            'F' : 10.0 ,
                            'DeltaPhiMax' : None},
                'carnivore': {'w_birth' : 6.0 ,
                          'sigma_birth' : 1.0 ,
                          'beta' : 0.75 ,
                          'eta' : 0.125 ,
                          'a_half ' : 40.0 ,
                          'phi_age' : 0.3 ,
                          'w_half' : 4.0 ,
                          'phi_weight' : 00.4 ,
                          'mu' : 0.4 ,
                          'gamma' : 0.8 ,
                          'zeta' : 3.5 ,
                          'xi' : 1.1 ,
                          'omega' : 0.8 ,
                          'F' : 50.0 ,
                          'DeltaPhiMax' : 10.0}}

def getnestdict(dict, key1, key2):
    try:
        return dict.get(key1, {}).get(key2)
    except KeyError:
        print('Keyvalue does not exist')
        return None



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



