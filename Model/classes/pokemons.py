import json


class Pokemon:
    def __init__(self, value, type, pos):
        self.value = value
        self.type = type
        self.pos = pos


class Pokemons:
    def __init__(self, jsonString):
        self.pokemons = []
        pokemonss = json.loads(jsonString)
        print(pokemonss)
        for pok in pokemonss["Pokemons"]:
            value = pok["Pokemon"]['value']
            type = pok["Pokemon"]['type']
            pos = tuple(float(s) for s in pok["Pokemon"]['pos'].split(','))
            pokemon = Pokemon(value, type, pos)
            self.pokemons.append(pokemon)
