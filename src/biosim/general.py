

animal_const = {'herbivore': {'w_birth': 8.0,
                              'sigma_birth': 1.5,
                              'beta': 0.9,
                              'eta': 0.05,
                              'a_half ': 40.0,
                              'phi_age': 0.6,
                              'w_half': 10.0,
                              'phi_weight': 0.1,
                              'mu': 0.25,
                              'gamma': 0.2,
                              'zeta': 3.5,
                              'xi': 1.2,
                              'omega': 0.4,
                              'F': 10.0,
                              'DeltaPhiMax': None},
                'carnivore': {'w_birth': 6.0,
                              'sigma_birth': 1.0,
                              'beta': 0.75,
                              'eta': 0.125,
                              'a_half ': 40.0,
                              'phi_age': 0.3,
                              'w_half': 4.0,
                              'phi_weight': 00.4,
                              'mu': 0.4,
                              'gamma': 0.8,
                              'zeta': 3.5,
                              'xi': 1.1,
                              'omega': 0.8,
                              'F': 50.0,
                              'DeltaPhiMax': 10.0}}

landscape_const = {'lowland': {'f_max': 800},
                   'highland': {'f_max': 300},
                   'water': {'f_max': 0},
                   'desert': {'f_max': 0}}


def getnestdict(dict, key1, key2):
    try:
        return dict.get(key1, {}).get(key2)
    except KeyError:
        print('Keyvalue does not exist')
        return None
