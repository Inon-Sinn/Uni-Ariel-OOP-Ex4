from types import SimpleNamespace

from Model.DiGraph import DiGraph
from Model.GraphAlgo import GraphAlgo
from client_python.client import Client
from classes.agents import *
from classes.pokemons import *
import json


class controller:

    def __init__(self):
        ip = '127.0.0.1'
        port = 6666
        # start connection
        self.client = Client()
        self.client.start_connection(ip, port)

        self.graph  # declare variables
        self.graphAlgo
        self.set_graph_and_algo()

        self.agents  # declare variables
        self.pokemons
        self.update_Pokemons()
        self.update_Agents()

    def find_next_route(self):
        # implement algorithm here
        pass

    def close(self):
        self.client.stop_connection()

    def update_GUI(self):
        # get parameters here and pass them to gui
        pass

    def set_graph_and_algo(self):
        graph_json = self.client.get_graph()  # geting json of graph
        self.graphAlgo = GraphAlgo()  # seting new graphalgo
        info = json.loads(self.client.get_info())  # geting info json
        graph_filename = "../" + info["GameServer"]["graph"]  # geting filename from info
        self.graphAlgo.load_from_json(graph_filename)  # loading the graph into algo
        self.graph = self.graphAlgo.get_graph()  # seting graph
        if self.graphAlgo.get_graph() is None:  # sanity check
            print('no graph found')

    def update_Agents(self):
        agents_json = self.client.get_agents()
        self.agents = Agents(agents_json)

    def update_Pokemons(self):
        pokemons_json = self.client.get_pokemons()  # setting pokemons and agents
        self.pokemons = Pokemons(pokemons_json)

    def add_agents(self, list_of_starting_nodes):
        if len(list_of_starting_nodes) > 4:
            print("cant insert more than 4 agents")
        for starting_node in list_of_starting_nodes:
            self.client.add_agent("{\"id\":" + starting_node + "}")
        # self.client.add_agent("{\"id\":0}")
        # self.client.add_agent("{\"id\":14}")
        # self.client.add_agent("{\"id\":10}")
        # self.client.add_agent("{\"id\":5}")

    def set_next_edge(self, dict_id_to_edge):
        for id in dict_id_to_edge.keys():
            # insert algorithm here
            pass


        self.client.move()


# *********** main loop ************#
# declare static controller that can be turned off if user presses stop
cntrl = controller()


def close():
    cntrl.close()


while cntrl.client.is_running():
    cntrl.update_Agents()
    cntrl.update_Pokemons()

    # insert algorithm here

    cntrl.set_next_edge()  # insert edges here


