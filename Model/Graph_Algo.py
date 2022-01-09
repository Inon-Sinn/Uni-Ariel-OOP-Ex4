import json
import math
from typing import List
import numpy as np
from Model import GraphAlgoInterface
from Model.DiGraph import DiGraph
from Model.GraphInterface import GraphInterface
from queue import Queue
from Model.Minheap import MinHeap

norm = np.linalg.norm


class GraphAlgo(GraphInterface):
    """This Class Represents the Algorithms we can Run on the Graph we implemented,
    This class implements the GraphAlgo Interface given in the Assignment"""

    def __init__(self, graph: DiGraph = None):
        self.graph = graph

    def get_graph(self) -> GraphInterface:
        """Returns the Graph on which the Algorithms run"""
        return self.graph

    def closestEdges(self, pos) -> list:
        """Return a sorted list of the edges closest to the pokemon"""
        edges = []
        for src in self.graph.get_all_v().values():
            for dest in src.all_out_edges.items():
                dest_pos = self.graph.getNode(dest[0]).pos
                p1 = np.array([src.pos[0], src.pos[1]])
                p2 = np.array([dest_pos[0], dest_pos[1]])
                p3 = np.array([pos[0], pos[1]])
                distance = np.abs(norm(np.cross(p2 - p1, p1 - p3))) / norm(p2 - p1)
                edges.append((src.Id, dest[0], distance))
        return edges

    @staticmethod
    def edgeByType(type, distances) -> tuple:
        """Return the edge closest that adhere to its type -> (src,dest,dist)
        where dist is the distance from the edge"""
        distances = sorted(distances, key=lambda x: x[2])
        edge = 0, 0, math.inf  # in case that there is no edge
        while len(distances) > 0:
            curEdge = distances.pop(0)
            if curEdge[0] < curEdge[1] and type == 1:
                edge = curEdge
                break
            if curEdge[1] < curEdge[0] and type == -1:
                edge = curEdge
                break
        return edge

    def distanceOnEdge(self, edge, pos) -> float:
        """Given the edge and the pokemon position it calculate its distance
        by to the weight of the edge in the Graph """
        # Build the points
        src_pos = self.graph.getNode(edge[0]).pos
        pt_src = np.array([src_pos[0], src_pos[1]])
        dest_pos = self.graph.getNode(edge[1]).pos
        pt_dest = np.array([dest_pos[0], dest_pos[1]])
        pt_pok = np.array([pos[0], pos[1]])

        dist_src_pos = np.abs(norm(pt_src - pt_pok))
        dist_src_dest = np.abs(norm(pt_src - pt_dest))
        if edge[2] == 0:
            part = (dist_src_pos / dist_src_dest)
        else:
            dist = math.sqrt((dist_src_pos * dist_src_pos) - (edge[2] * edge[2]))
            part = (dist / dist_src_dest)
        res = self.graph.getNode(edge[0]).all_out_edges.get(edge[1])
        return res * part

    def PokemonPlacement(self, type, pos) -> tuple:
        """Given a pokemon's position and type it returns the edges it on and the distance on the edge itself"""
        edgeDistances = self.closestEdges(pos)
        edge = self.edgeByType(type, edgeDistances)
        return edge[0], edge[1], self.distanceOnEdge(edge, pos)

    def best_Path_foreach_agent(self, agents: list, pokemons: list) -> dict:
        """ receiving agents [] and pokemons [] and agent_to_pokemon{agent.id,(path[], pok(x,y)}
         and returns {agent.id,(path[], pok(x,y)}
        """
        d = {}
        paths = []  # (weight, path, agent.id, pok.pos)

        for agent in agents.agents:
            tta = 0
            if agent.dest != -1:
                tta = self.distanceOnEdge((agent.dest, agent.src, 0), agent.pos)
            for pokemon in pokemons.pokemons:
                pok_root, pok_dest, dist = self.PokemonPlacement(pokemon.type, pokemon.pos)
                if agent.dest == -1:
                    weight, path = self.shortest_path(agent.src, pok_root)
                elif agent.src != pok_root:
                    weight, path = self.shortest_path(agent.dest, pok_root)
                else:
                    weight, path = self.shortest_path(agent.src, pok_root)
                path.pop(0)
                path.append(pok_dest)
                paths.append(((weight + dist + tta)/agent.speed, path, agent.id, pokemon.pos))

        # note that sorting might improve run time

        paths = sorted(paths, key=lambda x: x[0])
        pokemon_invalid = {}
        # sorted algorithm improve runtime
        for agent in agents.agents:
            for i in range(len(paths)):
                if (pokemon_invalid.get(paths[i][3]) == agent.id or pokemon_invalid.get(paths[i][3]) is None) \
                         and paths[i][2] == agent.id:
                    d[agent.id] = (paths[i][1], paths[i][3], paths[i][0])
                    break
            pokemon_invalid[d[agent.id][1]] = agent.id
        return d
        # working algo not best
        # for agent in agents.agents:
        #     weight = math.inf
        #     for i in range(paths.__len__()):
        #         if paths[i][2] == agent.id and paths[i][0] < weight and\
        #                 (pokemon_invalid.get(paths[i][3]) == agent.id or pokemon_invalid.get(paths[i][3]) is None):
        #             d[agent.id] = (paths[i][1], paths[i][3], paths[i][0])
        #             weight = paths[i][0]
        #     pokemon_invalid[d[agent.id][1]] = agent.id
        # return d  # {agent.id : (path, pokemon pos, weight of path) }

    def load_from_json_string(self, jsonString: str) -> bool:
        graph = DiGraph()
        # add try catch statement for jsonDecodeError
        fromJson = json.loads(jsonString)
        for n in fromJson['Nodes']:
            try:  # In case we are not given a position
                x, y, z = n['pos'].split(',')
                pos = (float(x), float(y))
                graph.add_node(n['id'], pos)
            except KeyError:
                graph.add_node(n['id'])
        for e in fromJson['Edges']:
            graph.add_edge(e['src'], e['dest'], e['w'])

        self.graph = graph

        return True

    def load_from_json(self, file_name: str) -> bool:
        """Given the name of a json file of a graph this algorithm will load the Graph"""
        graph = DiGraph()
        try:  # Checks if the file even Exists
            with open(file_name, "r+") as f:
                fromJson = json.load(f)
                for n in fromJson['Nodes']:
                    try:  # In case we are not given a position
                        pos = tuple(float(s) for s in n['pos'].split(','))
                        graph.add_node(n['id'], pos)
                    except KeyError:
                        graph.add_node(n['id'])
                for e in fromJson['Edges']:
                    graph.add_edge(e['src'], e['dest'], e['w'])
        except IOError as err:
            print(err)
            return False

        self.graph = graph
        return True

    def save_to_json(self, file_name: str) -> bool:
        """This Algorithms Saves the Graph of this class into a json file with the given File Name"""
        # Checks the Input
        if file_name is None:
            return False
        ToJson = {'Edges': [], 'Nodes': []}
        for src in self.graph.get_all_v().values():
            for dest in src.all_out_edges.items():
                ToJson['Edges'].append({
                    'src': src.Id,
                    'w': dest[1],
                    'dest': dest[0]
                })
        for n in self.graph.nodes.values():
            if n.noPos is True:
                ToJson['Nodes'].append({
                    'id': n.Id
                })
            else:
                ToJson['Nodes'].append({
                    'pos': ','.join(map(str, n.pos)),
                    'id': n.Id
                })
        try:
            with open(file_name, 'w') as outfile:
                json.dump(ToJson, outfile, indent=4)
                return True
        except TypeError:  # Should not happen but in case the Graph itself has a problem
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        shortestPath - O(|E|log|V|)
        we are given two nodes id's of the source and the destination,
        we then run Dijstra using those two id's and then return the path to get from the source to the destination.
        :param id1: Id of the source/start node
        :param id2: Id of the destination/end
        :return: a Tuple(the distance of the shortest path, the path as list of node id's)
        """
        dijkstra = Dijkstra(self.graph)
        # define distances From src as distance Of Shortest Paths
        distancesFromsrc = dijkstra.DijkstraAlgo(id1)
        if distancesFromsrc.get(id2) is math.inf:
            return float('inf'), []
        return distancesFromsrc.get(id2), dijkstra.ShortestPath(id1, id2)

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        tsp - O(n^2*|E|log|V|)
        traveling salesman problem(almost), we get a list of cities(id's of nodes)
        and have to return a path that passes through all cities(not the shortest just a path).
        We do this using a greedy algorithem, we start from the first city,
        the next city is the closest unvisited city to it, which we find with Dijkstra,
        and we contuine like this until we went over all city's. After which we return the path we went.
        :param node_lst: list of node id's representing the cities
        :return: a Tuple(the path as list of node id's,the distance of the Path)
        """
        if node_lst is None:
            return None, math.inf
        if node_lst.__len__() == 1:
            return node_lst
        completePath = []
        currentPath = []
        currentCity = node_lst.pop(0)
        found = False
        total_dist = 0
        while node_lst.__len__() != 0:
            next_city = 0
            removeIndex = 0
            minPathWeight = math.inf
            # getting the minimal path
            for i in range(node_lst.__len__()):
                # define ShortPathWeight as the distance from the start node to node at index i
                (shortPathWeight, ShortPathList) = self.shortest_path(currentCity, node_lst[i])
                # if there is a path shortPathWeight is real number, else it is infinity
                if shortPathWeight < minPathWeight:
                    next_city = node_lst[i]
                    removeIndex = i
                    currentPath = ShortPathList
                    minPathWeight = shortPathWeight
                    found = True
            if not found:
                return None, math.inf
            found = False
            currentCity = next_city
            node_lst.pop(removeIndex)
            completePath.extend(currentPath.copy())
            total_dist += minPathWeight

        # remove dublicates lol
        i = 0
        while i < len(completePath) - 1:
            if completePath[i] == completePath[(i + 1)]:
                completePath.pop(i)
            i += 1
        return completePath, total_dist

    def centerPoint(self) -> (int, float):
        """
        center - O(|V||E|log|V|)
        The center is the node which minimizes the max distance to all the other nodes.
        First we check if the graph is even connected else there won't be a center at all. If the graph is connected
        we run Dijkstra from every node we return the node minimizes the max distance to all the other nodes.
        :return: Tuple(center node id, min-maximum distance)
        """
        if self.isConnected() is False:
            return None, math.inf
        center_id = 0
        center_max_dis = math.inf
        for node in self.graph.get_all_v().values():
            dijk = Dijkstra(self.graph)
            dijk.DijkstraAlgo(node.Id)
            current_maxDis = dijk.MaxWeight()
            if current_maxDis < center_max_dis and current_maxDis != -1:
                center_max_dis = current_maxDis
                center_id = node.Id
        return center_id, center_max_dis

    def isConnected(self) -> bool:
        """An auxiliary function for center Point, Checks if the given Graph is Connected"""
        if len(self.graph.get_all_v()) != 0:
            firstRun = BFS(self.graph)
            if firstRun.Connected() is False:
                return False
            SecondRun = BFS(self.reversedGraph())
            if SecondRun.Connected() is False:
                return False
        return True

    def reversedGraph(self) -> DiGraph:
        """Return the Reverse Graph of the algorithms Graph"""
        Reversed = DiGraph()
        # Add all the node to the Reverse Graph
        for node in self.graph.get_all_v().values():
            Reversed.add_node(node.Id, node.pos)
        # Add all the edges to the Reverse Graph
        for node_id in self.graph.get_all_v().keys():
            for edge in self.graph.all_out_edges_of_node(node_id).items():
                Reversed.add_edge(edge[0], node_id, edge[1])
        return Reversed


class BFS:
    """This Class implements the BFS Algorithm,"""

    def __init__(self, graph):
        """
        Run the BFS Algorithm
        :param graph: a Graph that implements the GraphInterface
        """
        self.graph = graph
        self.Q = Queue(self.graph.v_size())
        self.d = {}
        self.prev = {}  # TODO could be deleted if there is no use for it
        # constants
        self.white = 0
        self.gray = 1
        self.black = 2
        self.BFSAlgo()

    def BFSAlgo(self):
        """The BFS algorithm, the input is the id of a node from which the Algorithm will start"""
        if self.graph.v_size() != 0:
            self.d = {}
            self.prev = {}
            node_id = next(iter(self.graph.get_all_v().keys()))
            for node in self.graph.get_all_v().values():
                node.tag = self.white
                self.prev[node.Id] = None
            self.graph.getNode(node_id).tag = self.gray
            self.d[node_id] = 0
            self.Q.put(node_id)
            while self.Q.empty() is False:
                self.BFS_VISIT(self.Q.get_nowait())

    def BFS_VISIT(self, node_id):
        """Used By the BFS Algorithm, Goes over all the siblings of the given Node and adds them to the Queue if they
        were not visited before( color white) """
        currNode = self.graph.getNode(node_id)
        for other_Node_id in currNode.get_All_out_edges():
            outNode = self.graph.getNode(other_Node_id)
            if outNode.tag == self.white:
                outNode.tag = self.gray
                self.d[other_Node_id] = self.d.get(node_id) + 1
                self.prev[other_Node_id] = node_id
                self.Q.put(other_Node_id)
        currNode.tag = self.black

    def Connected(self):
        """An Auxiliary Function used to check if the given Graph is connected"""
        for node in self.graph.get_all_v().values():
            if node.tag == self.white:
                return False
        return True


class Dijkstra:
    """This Class implements the Dijkstra Algorithm"""

    def __init__(self, graph):
        self.graph = graph
        self.MinHeap = MinHeap()
        self.distsFromSrc = {}
        self.prev = {}

    def DijkstraAlgo(self, start_id) -> dict:
        """
        The Dijkstra algorithm
        :param start_id: the id of the node on which the Dijkstra algorithm will run
        :return: dict - A dict with the weight of the shortest path for every node from the given starting node
        """
        # Iterating through all the nodes and setting their weights to infinity
        for node in self.graph.get_all_v().values():
            if node.Id == start_id:
                self.MinHeap.insert(0, start_id)
                self.distsFromSrc[start_id] = 0

            else:
                self.MinHeap.insert(math.inf, node.Id)
                self.distsFromSrc[node.Id] = math.inf

            self.prev[node.Id] = None
            # Note that the first node that is popped is the starting node since it has a weight of 0
        while not self.MinHeap.isEmpty():
            # dist is useless only defined because we receive a tuple from heappop
            next_id = self.MinHeap.removeMin()
            for edge in self.graph.all_out_edges_of_node(next_id).items():
                self.relax(next_id, edge[0], edge[1])
                # edge[0] = destId, edge[1] = weight
        return self.distsFromSrc

    def relax(self, src, dest, weight):
        """
        Relax, used be the Dijkstra algorithm,
        The Input is a Edge
        :param src: the id of the source node
        :param dest: the id of the destination node
        :param weight: the weight of the edge
        """
        newWeight = (self.distsFromSrc.get(src) + weight)

        if self.distsFromSrc.get(dest) > newWeight:
            self.MinHeap.DecreaseKey(dest, newWeight)
            self.distsFromSrc[dest] = newWeight
            self.prev[dest] = src

    def ShortestPath(self, src, dest) -> list:
        """
        An Auxiliray function that Return the shortest path between 2 given nodes in a form of a list
        :param src: the id of the starting node
        :param dest: the id of the end node
        :return: list - the shotest path between the two nodes (them included)
        """
        shortestPath = []
        current = dest
        if self.distsFromSrc[dest] is math.inf:
            return None
        while current != src and current is not None:
            shortestPath.insert(0, current)
            try:
                current = self.prev[current]
            except KeyError:
                current = None
        shortestPath.insert(0, src)
        return shortestPath

    def MaxWeight(self) -> float:
        """ An Auxiliary function that returns the max weight found in this Dijkstra run"""
        Max = 0
        for weight in self.distsFromSrc.values():
            if weight == math.inf:
                return -1
            if weight > Max:
                Max = weight
        return Max
