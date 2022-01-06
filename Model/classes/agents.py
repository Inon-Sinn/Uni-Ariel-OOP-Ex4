import json


class Agent:
    def __init__(self, id, value, src, dest, speed, pos):
        self.id
        self.value
        self.src
        self.dest
        self.speed
        self.pos


class Agents:

    def __init__(self, jsonString):
        self.agents = []
        agents_dict = json.loads(jsonString)
        for agent in agents_dict['Agents']:
            id = agent['Agent']['id']
            value = agent['Agent']['value']
            src = agent['Agent']['src']
            dest = agent['Agent']['dest']
            speed = agent['Agent']['speed']
            pos = tuple(float(s) for s in agent['Agent']['pos'].split(','))
            a = agent(id, value, src, dest, speed, pos)
            self.agents.append(a)
