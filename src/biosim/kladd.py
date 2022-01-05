class Nisse:

    parameters = {  'w_birth': 8.0, 'sigma_birth': 1.5,
                    'beta': 0.9, 'eta': 0.05}

    @classmethod
    def set_parameters(cls, new_params):
        for key in new_params:
            if key not in cls.parameters:
                raise KeyError('Invalid parameter name: ' + key)

        for key in cls.parameters:
            if key in new_params:
                cls.parameters.update(new_params)



    @classmethod
    def get_params(cls):
        return cls.parameters

    def __init__(self):
        w_birth = self.get_params().get('w_birth')
        self.age = w_birth


n = Nisse()
print(n.age)


