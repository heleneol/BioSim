default_parametres = {'f_max': 800}

def set_parameters(default_parametres, new_params):
    """
    set class parameters.

    Parameters
    ________
    new_params: dict

    Raises
    ________
    KeyError
    ValueError
    """

    for key in new_params:
        if key not in default_parametres:
            raise KeyError('Invalid parameter name: ' + key)

        elif new_params[key] < 0:
            raise ValueError('The fodder parameter must be a non-negative number')

    default_parametres.update(new_params)


set_parameters(default_parametres, {'f_max': 300})
print(default_parametres)



