import random


class Bacteria:
    """Bacteria which die and multiply with fixed probabilities."""

    # These parameters are defined at the class level
    p_death = 0.1   #: probability of death per cycle
    p_divide = 0.2  #: probability of cell division per cycle

    default_params = {'p_death': p_death,
                      'p_divide': p_divide}

    @classmethod
    def set_params(cls, new_params):
        """
        Set class parameters.

        Parameters
        ----------
        new_params : dict
            Legal keys: 'p_death', 'p_divide'

        Raises
        ------
        ValueError, KeyError
        """

        for key in new_params:
            if key not in ('p_death', 'p_divide'):
                raise KeyError('Invalid parameter name: ' + key)

        if 'p_death' in new_params:
            if not 0 <= new_params['p_death'] <= 1:
                raise ValueError('p_death must be in [0, 1].')
            cls.p_death = new_params['p_death']

        if 'p_divide' in new_params:
            if not 0 <= new_params['p_divide'] <= 1:
                raise ValueError('p_divide must be in [0, 1].')
            cls.p_divide = new_params['p_divide']

    @classmethod
    def get_params(cls, default_params):
        """
        Get class parameters.

        Returns
        -------
        dict
            Dictionary with class parameters.
        """

        return {'p_death': cls.p_death, 'p_divide': cls.p_divide}

    def __init__(self):
        """Create bacterium with age 0."""
        self.age = 0

    def ages(self):
        """Bacterium ages by one cycle."""
        self.age += 1

    def dies(self):
        """
        Decide whether bacterium dies.

        Returns
        -------
        bool
            True if bacterium dies.
        """

        return random.random() < self.p_death

    def divides(self):
        """
        Decide whether bacterium divides.

        Returns
        -------
        bool
            True if bacterium divides.
        """

        return random.random() < self.p_divide


# These parameters are defined at the class level
p_death = 0.1   #: probability of death per cycle
p_divide = 0.2  #: probability of cell division per cycle

default_params = {'p_death': p_death,
                      'p_divide': p_divide}

print(default_params)

parametres = {'w_birth': 8.0, 'sigma_birth': 1.5,
                    'beta': 0.9, 'eta': 0.05,
                    'a_half ': 40.0, 'phi_age': 0.6,
                    'w_half': 10.0, 'phi_weight': 0.1,
                    'mu': 0.25, 'gamma': 0.2,
                    'zeta': 3.5, 'xi': 1.2,
                    'omega': 0.4, 'F': 10.0,
                    'DeltaPhiMax': None}

a = {}
for i in parametres:
    a[i] = (parametres[i] + 1)

print(a)