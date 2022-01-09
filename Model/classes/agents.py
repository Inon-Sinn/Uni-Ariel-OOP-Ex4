import json


class Agent:
    def __init__(self, id, value, src, dest, speed, pos):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos


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
            x,y,z = agent['Agent']['pos'].split(',')
            pos = (float(x),float(y))
            a = Agent(id, value, src, dest, speed, pos)
            self.agents.append(a)

    def update(self, jsonString):
        agents_dict = json.loads(jsonString)
        for agent in agents_dict['Agents']:
            for old_agents in agent

    def getSpeedById(self, Id):
        for i in range(len(self.agents)):
            if self.agents[i].id == Id:
                return self.agents[i].speed
