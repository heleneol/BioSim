ini_carns = [{'loc': (2, 7),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
#animal for animal in ini_carns print()
print(ini_carns[0].get('pop')[0].get('species'))
