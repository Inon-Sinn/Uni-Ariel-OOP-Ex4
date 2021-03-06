import math
from time import time
from types import SimpleNamespace
import logging

logging.basicConfig(filename = "data/log", level=logging.DEBUG, filemode='w')
logger = logging.getLogger()

logger.info("our First Message")

from Model.DiGraph import DiGraph
from Model.Graph_Algo import GraphAlgo
from client_python.client import Client
from Model.classes.agents import *
from Model.classes.pokemons import *
import threading
import json
import random


class controller:

    """The Controller Class is the one that decide what to do at situation and is the only one with a connection to
    the client """

    def __init__(self):

        ip = '127.0.0.1'
        port = 6666

        # start connection
        self.client = Client()
        self.client.start_connection(ip, port)

        # declare variables
        self.graphAlgo = GraphAlgo()
        self.graphAlgo.load_from_json_string(self.client.get_graph())
        self.graph = self.graphAlgo.graph

        self.pokemons = Pokemons(self.client.get_pokemons())
        self.add_agents()
        self.agents = Agents(self.client.get_agents())  # initialize agents and pokemons

        self.pokemon_for_agent = {}  # dict of {agent.id : ( path to pokemon,pokemon.pos, pokemon_time)}
        for agent in self.agents.agents:
            self.pokemon_for_agent[agent.id] = ([], -1, math.inf)

        self.last_node_for_agent = {}  # dict of {agent.id : node.id}
        for agent in self.agents.agents:
            self.last_node_for_agent[agent.id] = -1

        self.times_to_move = []

        self.ttl = float(self.client.time_to_end())
        self.grade = 0

    def find_next_route(self):
        # implement algorithm here
        pass

    def close(self):
        self.client.stop_connection()

    def update_Agents(self):
        agents_json = self.client.get_agents()
        self.agents = Agents(agents_json)

    def update_Pokemons(self):
        pokemons_json = self.client.get_pokemons()  # setting pokemons and agents
        self.pokemons = Pokemons(pokemons_json)

    def add_agents(self):
        """Adds the agents at the best place at the beginning of the game"""
        # get the amount of agents in this game - n
        info = json.loads(self.client.get_info())
        n = info['GameServer']['agents']
        # find the n pokemon with the highest value if they exist
        pokList = []
        copyList = self.pokemons.pokemons.copy()
        for i in range(n):
            if len(copyList) is not 0:
                bestPokemon = copyList[0]
                for pok in copyList:
                    if pok.value > bestPokemon.value:
                        bestPokemon = pok
                pokList.append(bestPokemon)
                copyList.remove(bestPokemon)
        # use the pokemon finder for each pokemon
        for j in range(len(pokList)):
            pokList[j] = self.graphAlgo.PokemonPlacement(pokList[j].type, pokList[j].pos)
        if len(pokList) is not n:
            for i in range(n - len(pokList)):
                pokList.append((random.randint(0, self.graph.v_size()), 0, 0))
        # add the agents to the node next to the pokemon
        for l in range(len(pokList)):
            if self.client.add_agent("{\"id\"" + f":{pokList[l][0]}" + "}") is False:
                print("Agent wasn't added, you fucked up")

    def determine_next_edges(self):
        edges = []
        for agent in self.agents.agents:
            if agent.dest == -1:
                if len(self.pokemon_for_agent[agent.id][0]) != 0:
                    nextnode = (self.pokemon_for_agent[agent.id][0]).pop(0)
                    self.last_node_for_agent[agent.id] = agent.src
                    tup = (agent.id, nextnode)
                    edges.append(tup)
                else:
                    return None
        return edges
        # insert algorithm here

    def insert_edges_to_client(self, list_tup_id_edge):
        if list_tup_id_edge is not None:
            for tup in list_tup_id_edge:
                #                            '{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}'
                self.client.choose_next_edge('{"agent_id":' + str(tup[0]) + ', "next_node_id":' + str(tup[1]) + '}')
                # self.client.choose_next_edge(
                #     '{\"agent_id\":' + str(tup[0]) + ', \"next_node_id\":' + str(tup[1]) + '}')

    def move_agents(self):
        """Tells the server to move"""
        self.client.move()

    def add_paths_to_agents(self):
        """Adds the path to the agent in the correct way"""
        d = self.graphAlgo.best_Path_foreach_agent(self.agents, self.pokemons)
        for member in d.keys():
            for agent in self.agents.agents:
                if agent.id == member and agent.dest == -1:
                    self.pokemon_for_agent[agent.id] = d[agent.id]


    def test_algorithm(self):
        """Calculates the paths each agents should take"""
        self.update_Agents()
        self.update_Pokemons()
        for agent in self.agents.agents:
            if self.pokemon_for_agent.get(agent.id) is None:
                self.add_paths_to_agents()
            elif (len(self.pokemon_for_agent[agent.id][0])) == 0:
                self.add_paths_to_agents()
        list_tup = self.determine_next_edges()  # list of (agent id, next node)
        self.insert_edges_to_client(list_tup)
        self.ttl = float(self.client.time_to_end())

    def calculateNextStopTime(self):
        """Calculate when is the next time we should tell the server to move"""
        MinTime = math.inf
        for agent in self.pokemon_for_agent.items():
            if self.agents.getDestById(agent[0]) == -1:
                self.test_algorithm()
                self.update_Agents()
            path = agent[1][0]
            weight = 0
            # Next Node is Pokemon
            logging.debug(agent[1])
            if len(path) == 0:
                logging.info("Next One Is A Pokemon")
                sourceNodeId = self.last_node_for_agent[agent[0]]
                destNodeId = self.agents.getDestById(agent[0])
                logging.debug("source - {}, dest - {}".format(sourceNodeId, destNodeId))
                weightPok = self.graphAlgo.distanceOnEdge((sourceNodeId, destNodeId, 0), agent[1][1])
                weightAgent = self.graphAlgo.distanceOnEdge((sourceNodeId, destNodeId, 0), self.agents.getPosById(agent[0]))
                logging.debug("weight of Pokemon: {}, weigh of Agent {}".format(weightPok,weightAgent))
                if weightPok > weightAgent:
                    weight = weightPok
                else:
                    weight = self.graphAlgo.distanceOnEdge((destNodeId,sourceNodeId,0), self.agents.getPosById(agent[0]))
            else:
                logging.info("Next One Is A Node")
                sourceNodeId = self.last_node_for_agent[agent[0]]
                destNodeId = self.agents.getDestById(agent[0])
                logging.debug("source - {}, dest - {}".format(sourceNodeId, destNodeId))
                weight = self.graphAlgo.distanceOnEdgeForAgent((destNodeId, sourceNodeId, 0), self.agents.getPosById(agent[0]))
            speed = self.agents.getSpeedById(agent[0])
            Time = weight/speed
            MinTime = min(MinTime, Time)
            logging.debug("Calculation: source - {}, dest - {}, weight - {}, speed - {}, Time - {}".format(sourceNodeId,destNodeId,weight,speed,Time))
        logging.debug("The Next Stop is in {} seconds".format(MinTime))
        return time() + MinTime

