"""
Template for Landscape class.
"""

from .general import animal_const, landscape_const, getnestdict

class Lowland:
    """
    Class representing Lowland squares on the island.
    """

    def __init__(self, fodder=None, pop_herb=None):
        self.classname = self.__class__.__name__
        self.fodder = fodder if fodder is not None else getnestdict(landscape_const, self.classname, 'f_max')
        # Needs revising ^
        self.herbivore_population = #Input herbivore population in a tile?

    def update_fodder(self):
        herbivore_portion = getnestdict(animal_const, 'herbivore', 'F')

        if self.fodder >= herbivore_portion:
            self.fodder -= herbivore_portion

        elif 0 < self.fodder < herbivore_portion:
            self.fodder = 0
            rest_fodder = self.fodder #? Restene av maten om det er under 10

        else:
            pass #?


    def regrowth(self):

        self.fodder = getnestdict(landscape_const, self.classname, 'f_max')

    def reproduction(self):
        def newborns(population):
            if len(population) >= 2:
                N = len(population)
                for animal in population:
                    zeta = animal.parameters['zeta']
                    w_birth = animal.parameters['w_birth']
                    sigma_birth = animal.parameters['sigma_birth']
                    if animal.weight < zeta*(w_birth + sigma_birth):
                        birth_prob = 0
                    else:
                        gamma = animal.parameters['gamma']
                        birth_prob = gamma * animal.fitness * (N - 1)

            return [Animal() for parent in population if parent.gives_birth(birth_prob)]

        self.population.extend(newborns(self.population))