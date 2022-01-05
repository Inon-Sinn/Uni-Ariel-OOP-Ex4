import json


class Agent:
    def __init__(self, jsonString):
        self.id
        self.value
        self.src
        self.dest
        self.speed
        self.pos


class Agents:

    def __init__(self,jsonString):
        agents = json.loads(jsonString)
        for agent in agents:
            self.id = agents['Agent']['id']
            self.value = agents['Agent']['value']
            self.src = agents['Agent']['src']
            self.dest = agents['Agent']['dest']
            self.speed = agents['Agent']['speed']
            self.pos = agents['Agent']['pos']
