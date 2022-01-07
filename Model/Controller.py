from types import SimpleNamespace

import GUI
from Model.DiGraph import DiGraph
from Model.GraphAlgo import GraphAlgo
from client_python.client import Client
from classes.agents import *
from classes.pokemons import *
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
        self.agents = Agents(self.client.get_agents())  # declare variables
        self.pokemons = Pokemons(self.client.get_pokemons())
        self.ttl = float(self.client.time_to_end())
        # what is mc
        self.grade = 0

    def find_next_route(self):
        # implement algorithm here
        pass

    def close(self):
        self.client.stop_connection()
    #
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

        self.client.add_agent("{\"id\":0}")
        # self.client.add_agent("{\"id\":14}")
        # self.client.add_agent("{\"id\":10}")
        # self.client.add_agent("{\"id\":5}")

    def determine_next_edges(self):
        edges = []
        for agent in self.agents.agents:
            nextnode = (agent.src + 1) % self.graph.v_size()
            tup = (agent.id, nextnode)
            edges.append(tup)
        return edges
        # insert algorithm here

    def insert_edges_to_client(self, list_tup_id_edge):
        for tup in list_tup_id_edge:
            #                            '{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}'
            self.client.choose_next_edge('{"agent_id":' + str(tup[0]) + ',"next_node_id":' + str(tup[1]) + '}')



cntrl = controller()

while cntrl.client.is_running():



    cntrl.update_Agents()
    cntrl.update_Pokemons()
    list_tup = cntrl.determine_next_edges()  # list of (agent id, next node)
    cntrl.insert_edges_to_client(list_tup)
    cntrl.ttl = float(cntrl.client.time_to_end())
    # cntrl.update_GUI()  # does it matter if move called after update gui
    print(cntrl.ttl, cntrl.client.get_info())
    cntrl.client.move()


def close():
    cntrl.close()
