import json


class Pokemon:
    """A Class the represent a pokemon"""
    def __init__(self, value, type, pos):
        self.value = value
        self.type = type
        self.pos = pos


class Pokemons:
    """A class that represent a group of pokemon"""
    def __init__(self, jsonString):
        self.pokemons = []
        pokemonss = json.loads(jsonString)
        for pok in pokemonss["Pokemons"]:
            value = pok["Pokemon"]['value']
            type = pok["Pokemon"]['type']
            x, y, z = pok['Pokemon']['pos'].split(',')
            pos = (float(x), float(y))
            pokemon = Pokemon(value, type, pos)
            self.pokemons.append(pokemon)
