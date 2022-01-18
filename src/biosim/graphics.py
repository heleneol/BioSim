"""
:mod:`BioSim.graphics` provides graphics support for BioSim.

.. note::
   * This module requires the program ``ffmpeg`` or ``convert``
     available from `<https://ffmpeg.org>` and `<https://imagemagick.org>`.
   * You can also install ``ffmpeg`` using ``conda install ffmpeg``
   * You need to set the  :const:`_FFMPEG_BINARY` and :const:`_CONVERT_BINARY`
     constants below to the command required to invoke the programs
   * You need to set the :const:`_DEFAULT_FILEBASE` constant below to the
     directory and file-name start you want to use for the graphics output
     files.

"""

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os
import textwrap
import warnings

plt.rc('font', size=6)


# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('..', 'results')
_DEFAULT_GRAPHICS_NAME = 'image'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'


class Graphics:

    """Provides graphics support for BioSim."""

    rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                 'L': (0.0, 0.6, 0.0),  # dark green
                 'H': (0.5, 1.0, 0.5),  # light green
                 'D': (1.0, 1.0, 0.5)}  # light yellow

    def __init__(self, img_dir=None, img_name=None, img_fmt=None):
        """
        Graphic objects for visualization support of the BioSim package.

        :param img_dir: directory for image files; no images if None
        :type img_dir: str
        :param img_name: beginning of name for image files
        :type img_name: str
        :param img_fmt: image file format suffix
        :type img_fmt: str

        """

        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
            if not os.path.isdir(img_dir):
                os.mkdir(img_dir)
        else:
            self._img_base = os.path.join(_DEFAULT_GRAPHICS_DIR, img_name)
            if not os.path.isdir(_DEFAULT_GRAPHICS_DIR):
                os.mkdir(_DEFAULT_GRAPHICS_DIR)

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self._img_ctr = 0
        self._img_step = 1

        # the following atributes will be changed in setup function and
        # is used to make graphs
        self.fig = None
        self.year_ax = None
        self.animal_count_ax = None
        self.herb_heat_map_ax = None
        self.herb_heat_map_plot = None
        self.carn_heat_map_ax = None
        self.carn_heat_map_plot = None
        self.fitness_hist_ax = None
        self.age_hist_ax = None
        self.weight_hist_ax = None
        self.herb_line = None
        self.carn_line = None

    def update(self, year, species_count, animal_matrix, animal_fitness_per_species,
               animal_age_per_species, animal_weight_per_species, cmax_animals):
        """
        Updates graphics with current data and save to file if necessary.

        :param year: current time stamp
        :type year: int
        :param species_count: Dictionary containing animal count per species
        :type species_count: dict
        :param animal_matrix: Dictionary containing one 2d-array per species with animal count per cell as value
        :type animal_matrix: dict
        :param animal_fitness_per_species: Dictionary containing one list per species with animals fitness-values
        :type animal_fitness_per_species: dict
        :param animal_age_per_species: Dictionary containing one list per species with animals age-values
        :type animal_age_per_species: dict
        :param animal_age_per_species: Dictionary containing one list per species with animals weight-values
        :type animal_age_per_species: dict
        :param cmax_animals: Dictionary containing a max value for colorscale of heatmap per specis
        :type cmax_animals: dict
        """
        self._update_year_count(year)
        self._update_count_graph(year, species_count['Herbivore'], species_count['Carnivore'])
        self._update_herb_heat_map(animal_matrix['Herbivore'], cmax_animals)
        self._update_carn_heat_map(animal_matrix['Carnivore'], cmax_animals)
        self._update_fitness_hist(animal_fitness_per_species)
        self._update_age_hist(animal_age_per_species)
        self._update_weight_hist(animal_weight_per_species)
        self.fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-5)  # pause required to pass control to GUI

        self._save_graphics(year)

    def make_movie(self, movie_fmt=None):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg for MP4 and magick for GIF

        The movie is stored as img_base + movie_fmt
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def setup(self, final_step, img_step, vis_years, island_geographie, ymax_animals, hist_specs):
        """
        Prepare graphics.

        Call this before calling :meth:`update()` for the first time after
        the final time step has changed.

        :param final_step: last time step to be visualised (upper limit of x-axis)
        :type final_step: int
        :param img_step: interval between saving image to file
        :type img_step: int
        :param vis_years: intervall between updtaing graph with :meth:`update()`
        :type vis_years: int
        :param island_geographie: multiline textstring containing letters as indicators for colorvalues in map_rgb
        :type island_geographie: str
        :param ymax_animals: if set by user it givves the max for y-axis of animal count graph, default 20 000
        :type ymax_animals: int
        :param hist_specs: hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        :type hist_specs: dict
        """

        self._img_step = img_step

        # create new figure window
        if self.fig is None:
            self.fig = plt.figure()


        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        # add subplot for map

        self.map_ax = self.fig.add_subplot(3, 3, 1)

        island_geographic = textwrap.dedent(island_geographie)
        map_rgb = [[self.rgb_value[column] for column in row] for row in island_geographic.splitlines()]
        self.map_ax.imshow(map_rgb)
        self.map_legend = self.fig.add_axes([0.33, 0.77, 0.1, 0.2])
        self.map_legend.axis('off')
        for ix, landscapename in enumerate(('Water', 'Lowland',
                                            'Highland', 'Desert')):
            self.map_legend.add_patch(plt.Rectangle((0., ix * 0.2), 0.2, 0.05,
                                      edgecolor='none',
                                      facecolor=self.rgb_value[landscapename[0]]))
            self.map_legend.text(0.35, ix * 0.2, landscapename, transform=self.map_legend.transAxes)

        # add subplot for yearcount
        if self.year_ax is None:
            self.year_ax = self.fig.add_axes([0.45, 0.85, 0.1, 0.1])
            self.year_ax.axis('off')
            self.count_template = 'year: {:5d}'
            self.txt = self.year_ax.text(0.5, 0.5, self.count_template.format(0),
                                         horizontalalignment='center',
                                         verticalalignment='center',
                                         transform=self.year_ax.transAxes)

        # Add subplot for animal count per species
        if self.animal_count_ax is None:
            self.animal_count_ax = self.fig.add_subplot(3, 3, 3)
            self.animal_count_ax.set_ylim(0, ymax_animals)

        self.animal_count_ax.set_xlim(0, final_step + 1)

        if self.herb_heat_map_ax is None:
            self.herb_heat_map_ax = self.fig.add_subplot(3, 3, 4)
            self.herb_heat_map_ax.set_title('Herbivore distribution')

        if self.carn_heat_map_ax is None:
            self.carn_heat_map_ax = self.fig.add_subplot(3, 3, 6)
            self.carn_heat_map_ax.set_title('Carnivore distribution')

        fitness_specs = hist_specs['fitness']
        fitness_min = 0
        fitness_max = int(fitness_specs['max'])
        fitness_steps = int((fitness_max - fitness_min)/fitness_specs['delta'])
        if self.fitness_hist_ax is None:
            self.fitness_hist_ax = self.fig.add_subplot(3, 3, 7)
            self.fitness_hist_ax.set_title('Fitness hist.')
            self.fitness_hist_ax.set_ylim(0, 2000)
            self.fitness_bins = np.linspace(fitness_min, fitness_max, fitness_steps)

        age_specs = hist_specs['age']
        age_min = 0
        age_max = int(age_specs['max'])
        age_steps = int((age_max - age_min) / age_specs['delta'])
        if self.age_hist_ax is None:
            self.age_hist_ax = self.fig.add_subplot(3, 3, 8)
            self.age_hist_ax.title.set_text('Age hist.')
            self.age_bins = np.linspace(age_min, age_max, age_steps)

        weight_specs = hist_specs['weight']
        weight_min = 0
        weight_max = int(weight_specs['max'])
        weight_steps = int((weight_max - weight_min) / weight_specs['delta'])
        if self.weight_hist_ax is None:
            self.weight_hist_ax = self.fig.add_subplot(3, 3, 9)
            self.weight_hist_ax.set_title('Weight hist.')
            self.weight_bins = np.linspace(weight_min, weight_max, weight_steps)

        if vis_years > 1:
            linestyle = '-*'
        else:
            linestyle = '-'

        if self.herb_line is None:
            herb_plot = self.animal_count_ax.plot(np.arange(0, final_step+1),
                                                  np.full(final_step+1, np.nan), linestyle, color='blue')
            self.herb_line = herb_plot[0]
        else:
            x_data, y_data = self.herb_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step+1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self.herb_line.set_data(np.hstack((x_data, x_new)),
                                        np.hstack((y_data, y_new)))
        if self.carn_line is None:
            carn_plot = self.animal_count_ax.plot(np.arange(0, final_step+1),
                                                  np.full(final_step+1, np.nan), linestyle, color='red')
            self.carn_line = carn_plot[0]
        else:
            x_data, y_data = self.carn_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step+1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self.carn_line.set_data(np.hstack((x_data, x_new)),
                                        np.hstack((y_data, y_new)))
        warnings.filterwarnings('ignore')
        self.fig.tight_layout(pad=3.0)

    def _update_herb_heat_map(self, herb_map, cmax_animals):
        """
        Updates the heat map showing the density of herbivores.

        :param herb_map: 2d-array per species with herbivore count per cell as value
        :type herb_map: array
        """

        if self.herb_heat_map_plot is not None:
            self.herb_heat_map_plot.set_data(herb_map)
        else:
            self.herb_heat_map_plot = self.herb_heat_map_ax.imshow(herb_map,
                                                                   interpolation='nearest',
                                                                   vmin=0, vmax=cmax_animals['Herbivore'])
            plt.colorbar(self.herb_heat_map_plot, ax=self.herb_heat_map_ax,
                         orientation='vertical', shrink=0.75)

    def _update_carn_heat_map(self, carn_map, cmax_animals):
        """
        Updates the heat map showing the density of carnivores.

        :param carn_map: 2d-array per species with carnivore count per cell as value
        :type carn_map: array
        """
        if self.carn_heat_map_plot is not None:
            self.carn_heat_map_plot.set_data(carn_map)
        else:
            self.carn_heat_map_plot = self.carn_heat_map_ax.imshow(carn_map,
                                                                   interpolation='nearest',
                                                                   vmin=0, vmax=cmax_animals['Carnivore'])
            plt.colorbar(self.carn_heat_map_plot, ax=self.carn_heat_map_ax,
                         orientation='vertical', shrink=0.75)

    def _update_count_graph(self, year, herb_count, carn_count):
        """
        Updates the line for the animal count on the island for both species.

        :param year: what step in the simulation we are in, givves the x-coordinate
        :type year: int
        :param herb_count: the total numbers of herbivores on the island
        :type herb_count: int
        :param carn_count: the total numbers of carnivores on the island
        :type carn_count: int
        """
        y_data = self.herb_line.get_ydata()
        y_data[year] = herb_count
        self.herb_line.set_ydata(y_data)

        y_data = self.carn_line.get_ydata()
        y_data[year] = carn_count
        self.carn_line.set_ydata(y_data)

    def _update_year_count(self, year):
        """
        Updates the year counter in the graphics.

        :param year: what step in the simulation we are in, givves the x-coordinate
        :type year: int
        """
        self.txt.set_text(self.count_template.format(year))

    def _update_fitness_hist(self, animall_fitness_per_species):
        """
        Updates the fitness histogram for both species. The histogram is showing the distrubution of fitness-values.

        :param animal_fitness_per_species: Dictionary containing one list per species with animals fitness-values
        :type animal_fitness_per_species: dict
        """

        self.fitness_hist_ax.clear()
        self.fitness_hist_ax.hist(animall_fitness_per_species['Herbivore'], self.fitness_bins,
                                  histtype=u'step', color='blue')
        self.fitness_hist_ax.hist(animall_fitness_per_species['Carnivore'], self.fitness_bins,
                                  histtype=u'step', color='red')

    def _update_age_hist(self, animal_age_per_species):
        """
        Updates the age histogram for both species. The histogram is showing the distrubution of age-values.

        :param animal_age_per_species: Dictionary containing one list per species with animals age-values
        :type animal_age_per_species: dict
        """
        self.age_hist_ax.clear()
        self.age_hist_ax.hist(animal_age_per_species['Herbivore'], self.age_bins,
                              histtype=u'step', color='blue')
        self.age_hist_ax.hist(animal_age_per_species['Carnivore'], self.age_bins,
                              histtype=u'step', color='red')

    def _update_weight_hist(self, animal_weight_per_species):
        """
        Updates the weight histogram for both species. The histogram is showing the distrubution of weight-values.

        :param animal_age_per_species: Dictionary containing one list per species with animals weight-values
        :type animal_age_per_species: dict
        """
        self.weight_hist_ax.clear()
        self.weight_hist_ax.hist(animal_weight_per_species['Herbivore'], self.weight_bins,
                                 histtype=u'step', color='blue')
        self.weight_hist_ax.hist(animal_weight_per_species['Carnivore'], self.weight_bins,
                                 histtype=u'step', color='red')

    def _save_graphics(self, step):
        """Saves graphics to file if file name given."""

        if self._img_base is None or step % self._img_step != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
