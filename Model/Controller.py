from types import SimpleNamespace

from Model.DiGraph import DiGraph
from Model.GraphAlgo import GraphAlgo
from client_python.client import Client
import json

ip = '127.0.0.1'
port = 6666

# start connection
client = Client()
client.start_connection(ip,port)

# get the graph
graph_json = client.get_graph()
graphAlgo = GraphAlgo()
info = json.loads(client.get_info())
graph_filename = "../" + info["GameServer"]["graph"]

graphAlgo.load_from_json(graph_filename)
if graphAlgo.get_graph() is None:
    print('no graph found')
else:
    for node in graphAlgo.get_graph().get_all_v().values():
        print(node)
# pokemons
pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))
print(pokemons_obj)

agents = json.loads(client.get_agents(),
                    object_hook=lambda d: SimpleNamespace(**d))

# print(pokemons_obj)
print(agents)


# print (agents_obj)

def find_next_route():
    # implement algorithm here
    pass


def update_GUI():
    # get parameters here and pass them to gui
    pass


def get_pokemons():
    # get the pokemons from the server
    pass


while client.is_running():
    for agent in agents:
        if (agent.dest != -1):
            # insert algorithm here
            # choose next edge here
            pass

    client.move()
