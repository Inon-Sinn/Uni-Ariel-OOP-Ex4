from types import SimpleNamespace

from Model.DiGraph import DiGraph
from Model.Graph_Algo import GraphAlgo
from client_python.client import Client
from Model.classes.agents import *
from Model.classes.pokemons import *
import threading
import json


class controller:

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

        self.add_agents([1, 2, 3, 4])
        self.agents = Agents(self.client.get_agents())  # initialize agents and pokemons
        self.pokemons = Pokemons(self.client.get_pokemons())

        self.pokemon_for_agent = {}  # dict of {agent.id : ( path to pokemon,pokemon.pos)}

        self.ttl = float(self.client.time_to_end())
        self.grade = 0

    def find_next_route(self):
        # implement algorithm here
        pass

    def close(self):
        self.client.stop_connection()

    # def update_GUI(self):
    #     # if gui returns false then close the controler
    #     if not self.gui.update(self.pokemons.pokemons, self.agents.agents, self.grade, self.gui.mc, self.ttl):
    #         close()

    def update_Agents(self):
        agents_json = self.client.get_agents()
        self.agents = Agents(agents_json)

    def update_Pokemons(self):
        pokemons_json = self.client.get_pokemons()  # setting pokemons and agents
        self.pokemons = Pokemons(pokemons_json)

    def add_agents(self, list_of_starting_nodes):
        # insert closest node to pokemon algorithm here
        # if len(list_of_starting_nodes) > 4:
        #     print("cant insert more than 4 agents")
        # for starting_node in list_of_starting_nodes:
        #     #                      "{\"id\":0}"
        #     self.client.add_agent('{\"id\":' + starting_node + '}')

        if not self.client.add_agent("{\"id\":0}"):
            print("agent adding failed")
        # self.client.add_agent("{\"id\":14}")
        # self.client.add_agent("{\"id\":10}")
        # self.client.add_agent("{\"id\":5}")

    def determine_next_edges(self):
        edges = []
        for agent in self.agents.agents:
            if agent.dest == -1:
                nextnode = (self.pokemon_for_agent[agent.id][0]).pop(0)
                tup = (agent.id, nextnode)
                edges.append(tup)
        return edges
        # insert algorithm here

    def insert_edges_to_client(self, list_tup_id_edge):
        for tup in list_tup_id_edge:
            #                            '{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}'
            self.client.choose_next_edge('{"agent_id":' + str(tup[0]) + ', "next_node_id":' + str(tup[1]) + '}')
            # self.client.choose_next_edge(
            #     '{\"agent_id\":' + str(tup[0]) + ', \"next_node_id\":' + str(tup[1]) + '}')

    def move_agents(self):
        self.client.move()

    def add_paths_to_agents(self):
        self.pokemon_for_agent = self.graphAlgo.best_Path_foreach_agent(self.agents, self.pokemons)
