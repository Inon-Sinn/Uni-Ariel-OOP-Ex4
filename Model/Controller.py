from types import SimpleNamespace

from Model.DiGraph import DiGraph
from client_python.client import Client
import json

ip = '127.0.0.1'
port = 6666

# start connection
client = Client()
client.start_connection(ip,port)

# get the graph
graph_json = client.get_graph()
graph = DiGraph()


pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))



def find_next_route():
    # implement algorithm here
    pass


def update_GUI():
    # get parameters here and pass them to gui
    pass


def get_pokemons():
    # get the pokemons from the server
    pass