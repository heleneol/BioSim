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

plt.rc('font', size=8)


# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('../..', 'data')
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
        else:
            self._img_base = None

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self._img_ctr = 0
        self._img_step = 1

        # the following will be initialized by _setup_graphics
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
        self.img_axis = None
        self.herb_line = None
        self.carn_line = None

    def update(self, year, species_count, animal_matrix, animal_fitness_per_species, animal_age_per_species, animal_weight_per_species):
        """
        Updates graphics with current data and save to file if necessary.

        :param step: current time step
        :param sys_map: current system status (2d array)
        :param sys_mean: current mean value of system
        """
        self._update_year_count(year)
        self._update_count_graph(year, species_count['Herbivore'], species_count['Carnivore'])
        self._update_herb_heat_map(animal_matrix['Herbivore'])
        self._update_carn_heat_map(animal_matrix['Carnivore'])
        self._update_fitness_hist(animal_fitness_per_species)
        self._update_age_hist(animal_age_per_species)
        self._update_weight_hist(animal_weight_per_species)
        self.fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-5)  # pause required to pass control to GUI

        # self._save_graphics(step)

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

    def setup(self, final_step, img_step, island_geographie):
        """
        Prepare graphics.

        Call this before calling :meth:`update()` for the first time after
        the final time step has changed.

        :param final_step: last time step to be visualised (upper limit of x-axis)
        :param img_step: interval between saving image to file
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
        self.map_legend = self.fig.add_axes([0.37, 0.7, 0.1, 0.2])
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
            self.count_template = 'Count: {:5d}'
            self.txt = self.year_ax.text(0.5, 0.5, self.count_template.format(0),
                                         horizontalalignment='center',
                                         verticalalignment='center',
                                         transform=self.year_ax.transAxes)

        # Add subplot for animal count per species
        if self.animal_count_ax is None:
            self.animal_count_ax = self.fig.add_subplot(3, 3, 3)
            self.animal_count_ax.set_ylim(0, 20000)

        self.animal_count_ax.set_xlim(0, final_step + 1)

        if self.herb_heat_map_ax is None:
            self.herb_heat_map_ax = self.fig.add_subplot(3, 3, 4)
            self.herb_heat_map_ax.set_title('Herbivore heat map')

        if self.carn_heat_map_ax is None:
            self.carn_heat_map_ax = self.fig.add_subplot(3, 3, 6)
            self.carn_heat_map_ax.set_title('Carnivore heat map')

        if self.fitness_hist_ax is None:
            self.fitness_hist_ax = self.fig.add_subplot(3, 3, 7)
            self.fitness_hist_ax.set_title('Fitness hist.')
            self.fitness_hist_ax.set_ylim(0, 2000)
            self.fitness_bins = np.linspace(0, 1, 30)

        if self.age_hist_ax is None:
            self.age_hist_ax = self.fig.add_subplot(3, 3, 8)
            self.age_hist_ax.set_title('Age hist.')
            self.age_hist_ax.set_ylim(0, 2000)
            self.age_bins = np.linspace(0, 60, 30)

        if self.weight_hist_ax is None:
            self.weight_hist_ax = self.fig.add_subplot(3, 3, 9)
            self.weight_hist_ax.set_title('Weight hist.')
            self.weight_hist_ax.set_ylim(0, 2000)
            self.weight_bins = np.linspace(0, 60, 30)

        if self.herb_line is None:
            herb_plot = self.animal_count_ax.plot(np.arange(0, final_step+1),
                                                  np.full(final_step+1, np.nan), color='blue')
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
                                                  np.full(final_step+1, np.nan), color='red')
            self.carn_line = carn_plot[0]
        else:
            x_data, y_data = self.carn_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step+1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self.carn_line.set_data(np.hstack((x_data, x_new)),
                                        np.hstack((y_data, y_new)))

    def _update_herb_heat_map(self, herb_map):
        """Update the 2D-view of the system."""

        if self.herb_heat_map_plot is not None:
            self.herb_heat_map_plot.set_data(herb_map)
        else:
            self.herb_heat_map_plot = self.herb_heat_map_ax.imshow(herb_map,
                                                                   interpolation='nearest',
                                                                   vmin=0, vmax=200)
            plt.colorbar(self.herb_heat_map_plot, ax=self.herb_heat_map_ax,
                         orientation='vertical', shrink=0.75)

    def _update_carn_heat_map(self, carn_map):
        if self.carn_heat_map_plot is not None:
            self.carn_heat_map_plot.set_data(carn_map)
        else:
            self.carn_heat_map_plot = self.carn_heat_map_ax.imshow(carn_map,
                                                                   interpolation='nearest',
                                                                   vmin=0, vmax=200)
            plt.colorbar(self.carn_heat_map_plot, ax=self.carn_heat_map_ax,
                         orientation='vertical', shrink=0.75)

    def _update_count_graph(self, year, herb_count, carn_count):
        y_data = self.herb_line.get_ydata()
        y_data[year] = herb_count
        self.herb_line.set_ydata(y_data)

        y_data = self.carn_line.get_ydata()
        y_data[year] = carn_count
        self.carn_line.set_ydata(y_data)

    def _update_year_count(self, year):
        self.txt.set_text(self.count_template.format(year))

    def _update_fitness_hist(self, animall_fitness_per_species):
        self.fitness_hist_ax.clear()
        self.fitness_hist_ax.hist(animall_fitness_per_species['Herbivore'], self.fitness_bins,
                                  histtype=u'step', color='blue')
        self.fitness_hist_ax.hist(animall_fitness_per_species['Carnivore'], self.fitness_bins,
                                  histtype=u'step', color='red')

    def _update_age_hist(self, animal_age_per_species):
        self.age_hist_ax.clear()
        self.age_hist_ax.hist(animal_age_per_species['Herbivore'], self.age_bins,
                              histtype=u'step', color='blue')
        self.age_hist_ax.hist(animal_age_per_species['Carnivore'], self.age_bins,
                              histtype=u'step', color='red')

    def _update_weight_hist(self, animal_weight_per_species):
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
