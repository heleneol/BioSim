
geogr = textwrap.dedent(geogr)

i = Island(geogr)

ini_herbs = [{'loc': (2, 2),
              'pop': [{ 'species': 'Herbivore',
                        'age': 5,
                        'weight': 20}
                        for _ in range(2)]}]

i.place_population(ini_pop=ini_herbs)
print(i.map[(2, 2)].herb_pop)

@pytest.mark.parametrize('geogr, n_b', [(10, 20), (30, 40)])
class test_island:
