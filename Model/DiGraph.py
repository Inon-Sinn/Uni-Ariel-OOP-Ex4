import random

from Model.GraphInterface import GraphInterface


class DiGraph(GraphInterface):
    """This Class Represent the Directed weighted Graph,
    it implements the Graph Interface given for the Assignment"""

    def __init__(self):
        self.mc = 0
        self.EdgeSize = 0
        self.nodes = {}  # dictionary with all the Nodes

    def v_size(self) -> int:
        """Returns the amount of Nodes in the Graph"""
        return len(self.nodes)

    def e_size(self) -> int:
        """Returns the amount of Edges in the Graph"""
        return self.EdgeSize

    def get_all_v(self) -> dict:
        """
        Returns a dictionary of all the nodes in the Graph
        :return: dict(Nodes) - a dictionary containing objects of Type Node
        """
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        Return a dictionary of all the edges going into the node with the given Id
        :return: dict('int - src_node_id':int - weight of the edge)
        """
        return self.nodes.get(id1).get_All_in_edges()

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        Return a dictionary of all the edges going out of the node with the given Id
        :return: dict('int - dest_node_id':int - weight of the edge)
        """
        return self.nodes.get(id1).get_All_out_edges()

    def get_mc(self) -> int:
        """Returns a counter which counts the amounts of changes that happened in the Graph"""
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Add a new edge with the a given weight to the Graph by the id of the source node and the id of destination
        :param id1: id of the source node
        :param id2: id of the destination node
        :param weight: the weight of the new edge
        """
        if id1 == id2:
            return False
        if self.nodes.get(id1) is None or self.nodes.get(id2) is None:
            return False
        src = self.nodes.get(id1)
        dest = self.nodes.get(id2)
        if src.all_out_edges.get(id2) is None and dest.all_in_edges.get(id1) is None:
            src.add_Out_edge(id2, weight)
            dest.add_In_edge(id1, weight)
            self.mc += 1
            self.EdgeSize += 1
            return True
        return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a new Node to the Graph given a id for the new Node
        :param node_id: the id of the node the user want's to add
        :param pos: tuple - that represent a 2 point on a 2 dimensional map
        :return: bool: True in Case the node was added successfully, False if it already exists
        """
        if self.nodes.get(node_id) is None:
            newNode = Node(node_id, pos)
            self.nodes[node_id] = newNode
            self.mc += 1
            return True
        return False

    def remove_node(self, node_id: int) -> bool:
        """
        Removes A node from the Graph given the id of the Node
        :param node_id: the id of the Node
        :return: bool - True if it was Removed Successfully else returns False
        """
        nodeToRemove = self.nodes.get(node_id)
        if nodeToRemove is None:
            return False
        for dest in nodeToRemove.get_All_out_edges():
            self.getNode(dest).remove_In_edge(node_id)
            self.EdgeSize -= 1
        for src in nodeToRemove.get_All_in_edges():
            self.getNode(src).remove_Out_edge(node_id)
            self.EdgeSize -= 1
        self.mc += 1
        self.nodes.pop(node_id)
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes a edge from the graph given it's source and destination id's
        :param node_id1: Id of the soucre Node
        :param node_id2: Id of the Destination Node
        :return: bool - True if it was Removed Successfully else returns False
        """
        if node_id1 == node_id2:
            return False
        if self.nodes.get(node_id1) is None or self.nodes.get(node_id2) is None:
            return False
        src = self.nodes.get(node_id1)
        dest = self.nodes.get(node_id2)
        try:
            src.remove_Out_edge(node_id2)
            dest.remove_In_edge(node_id1)
        except:
            return False
        self.mc += 1
        self.EdgeSize -= 1
        return True

    def __repr__(self):
        return "Graph: |V|={} , |E|={}".format(self.v_size(), self.e_size())

    def getNode(self, Id):
        """An Auxiliray function, Return the node from the Graph given it's Id"""
        return self.nodes.get(Id)


class Node:
    """This Class Implements the Node of the Graph"""

    def __init__(self, Id, pos):
        self.Id = Id
        self.tag = 0  # Used by the BFS algoirthm to color the node
        self.noPos = False  # Used to check if there even is a pos
        if pos is None:
            # In case the Node doesn't have a position we give it a random one
            self.pos = (random.randint(3, 9), random.randint(3, 9), 0)
            self.noPos = True
        else:
            self.pos = pos
        # The edges which destination is this node, key: source node id, value: weight of the edge
        self.all_in_edges = {}
        # The edges which source is this node, key: destination node id, value: weight of the edge
        self.all_out_edges = {}

    def get_All_in_edges(self):
        """Return a dict of all the incoming edges of this node"""
        return self.all_in_edges

    def get_All_out_edges(self):
        """Return a dict of all the outgoing edges of this node"""
        return self.all_out_edges

    def add_In_edge(self, otherId, weight):
        """Adds a new incoming edge to this node to the dict of incoming edges"""
        self.all_in_edges[otherId] = weight

    def add_Out_edge(self, otherId, weight):
        """Adds a new outgoing edge to this node to the dict of outgoing edges"""
        self.all_out_edges[otherId] = weight

    def remove_In_edge(self, otherId):
        """Remove a edge from the dict of all incoming edges"""
        return self.all_in_edges.pop(otherId)

    def remove_Out_edge(self, otherId):
        """Remove a edge from the dict of all outgoing edges"""
        return self.all_out_edges.pop(otherId)

    def __repr__(self):
        return "{}: |edges out| {} |edges in| {}".format(self.Id, len(self.all_out_edges), len(self.all_in_edges))

    def __str__(self):
        return "Id: {}\nTag: {}\npos: {}\nIncoming Edges: {}\nOutgoing Edges: {}\n".format(self.Id, self.tag, self.pos,
                                                                                           self.all_in_edges,
                                                                                           self.all_out_edges)
