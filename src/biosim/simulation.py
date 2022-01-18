"""
Module implementing the simulation of the ecosystem through the BioSim class.
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU

from biosim.island import Island
from biosim.graphics import Graphics
import textwrap
import warnings



class BioSim:
    """
    Class for simulating the ecosystem on the :class:`island.Island`.
    """
    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):

        """

        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param vis_years: years between visualization updates (if 0, disable graphics)
        :param img_dir: String with path to directory for figures
        :param img_base: String with beginning of file name for figures
        :param img_fmt: String with file type for figures, e.g. 'png'
        :param img_years: years between visualizations saved to files (default: vis_years)
        :param log_file: If given, write animal counts to this file

        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
        {'Herbivore': 50, 'Carnivore': 20}

        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
        {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.

        If img_dir is None, no figures are written to file. Filenames are formed as

        f'{os.path.join(img_dir, img_base}_{img_number:05d}.{img_fmt}'

        where img_number are consecutive image numbers starting from 0.

        img_dir and img_base must either be both None or both strings.

        example
        -------
        ::

            sim = BioSim(island_map = geogr, ini_pop = population img_dir='results')
        """
        self.island_geographie = textwrap.dedent(island_map)
        self.island = Island(geogr=self.island_geographie)
        self.add_population(population=ini_pop)
        self.graphics = Graphics(img_dir,img_name=img_base,img_fmt=img_fmt)
        self.seed = seed
        self.ymax_animals = ymax_animals if ymax_animals is not None else 20000
        self.cmax_animals = {'Herbivore': 200,
                            'Carnivore': 200}
        if cmax_animals is not None:
            for key, value in cmax_animals.items():
                if key in self.cmax_animals.keys():
                    self.cmax_animals[key] = value
                else:
                    raise KeyError(f'Key {key} is not valid')

        self.hist_specs = {'fitness': {'max': 1.0, 'delta': 0.05},
                           'age': {'max': 60.0, 'delta': 2},
                           'weight': {'max': 60, 'delta': 2}}
        if hist_specs is not None:
            for key, value in hist_specs.items():
                if key in self.hist_specs.keys():
                    self.hist_specs[key] = value
                else:
                    raise KeyError(f'Key {key} is not valid')

        self.vis_years = vis_years if vis_years is not None else 1
        self.img_years = img_years if img_years is not None else vis_years

        if vis_years is not None and img_years is not None:
            if img_years % vis_years != 0:
                raise ValueError('img_steps must be a multiple of vis_steps')

        self.step = 0
        self.final_step = None

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species.`
        """
        self.island.set_animal_parameters_island(species=species, params=params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        self.island.set_landscape_parameters_island(landscape=landscape, params=params)

    def simulate(self, num_years):
        """
        Run simulations with or without graphics (see vis_years contraints). Passes graphics parametres
        to the graphics module in order to visulaize.

        :param num_years: number of years to simulate, must be integer.
        :type num_years: int

        """
        self.final_step = self.step + num_years
        if self.vis_years != 0:
            num_simulations = num_years
            self.graphics.setup(final_step=self.final_step,img_step= self.img_years,
                                vis_years=self.vis_years, island_geographie=self.island_geographie,
                                ymax_animals=self.ymax_animals,
                                hist_specs=self.hist_specs)
            if num_simulations // 1 == num_simulations:
                while self.step < self.final_step:
                    self.island.annual_cycle_island()
                    self.step += 1

                    if self.step % self.vis_years == 0:
                        self.graphics.update(year=self.step, species_count=self.num_animals_per_species,
                                             cmax_animals=self.cmax_animals,
                                             animal_matrix=self.num_animals_per_species_per_cell,
                                             animal_fitness_per_species=self.animal_fitness_per_species,
                                             animal_age_per_species=self.animal_age_per_species,
                                             animal_weight_per_species=self.animal_weight_per_species)
            else:
                raise ValueError(f'Num_years has to be an integer, not a {type(num_years)}')
        else:
            warnings.warn("Warning: Simulation running without graphics due to vis_years is set to 0")
            num_simulations = num_years
            if num_simulations // 1 == num_simulations:
                while self.step < self.final_step:
                    self.island.annual_cycle_island()
                    self.step += 1
            else:
                raise ValueError(f'Num_years has to be an integer, not a {type(num_years)}')


    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.island.place_population(populations=population)

    @property
    def year(self):
        """Last year simulated."""
        return self.step

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.island.get_number_of_carns() + self.island.get_number_of_herbs()

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

        return {'Herbivore': self.island.get_number_of_herbs(),
                'Carnivore': self.island.get_number_of_carns()}

    @property
    def num_animals_per_species_per_cell(self):
        return {'Herbivore': self.island.get_number_herbs_per_cell(),
                'Carnivore': self.island.get_number_carns_per_cell()}

    @property
    def animal_fitness_per_species(self):
        return {'Herbivore': self.island.get_herbs_fitness(),
                'Carnivore': self.island.get_carns_fitness()}

    @property
    def animal_age_per_species(self):
        return {'Herbivore': self.island.get_herbs_age(),
                'Carnivore': self.island.get_carns_age()}

    @property
    def animal_weight_per_species(self):
        return {'Herbivore': self.island.get_herbs_weight(),
                'Carnivore': self.island.get_carns_weight()}

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        self.graphics.make_movie()
