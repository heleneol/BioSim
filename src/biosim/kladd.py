import textwrap

ini_herbs = [{'loc': (10, 10),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 20}
                              for _ in range(2)]}]

for indx, population in enumerate(ini_herbs):
    if ini_herbs[indx].get('loc') == (10, 10):
        print(ini_herbs[indx].get('pop'))
