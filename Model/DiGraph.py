from Model.GraphInterface import GraphInterface


class DiGraph(GraphInterface):

    def __init__(self):
        self.mc = 0
        self.EdgeSize = 0
        self.nodes = {}  # dictionary with all the Nodes

    def v_size(self) -> int:
        return len(self.nodes)

    def e_size(self) -> int:
        return self.EdgeSize

    def get_all_v(self) -> dict:
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.nodes.get(id1).get_All_in_edges()

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.nodes.get(id1).get_All_out_edges()

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
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
        """Return False in the Case the node already exists"""
        # TODO check if its right and other options for sending False
        if self.nodes.get(node_id) is None:
            newNode = Node(node_id, pos)
            self.nodes[node_id] = newNode
            self.mc += 1
            return True
        return False

    def remove_node(self, node_id: int) -> bool:
        nodeToRemove = self.nodes.get(node_id)
        if nodeToRemove is None:
            return False  # TODO check if i should return False if the id does not exist
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
        return self.nodes.get(Id)


class Node:

    def __init__(self, Id, pos):
        self.Id = Id
        self.tag = 0  # Used by the BFS algoirthm to color the node
        self.noPos = False  # Used to check if there even is a pos
        if pos is None:
            self.pos = (0, 0, 0)
            self.noPos = True
        else:
            self.pos = pos
        # The edges which destination is this node, key: source node id, value: weight of the edge
        self.all_in_edges = {}
        # The edges which source is this node, key: destination node id, value: weight of the edge
        self.all_out_edges = {}

    def get_All_in_edges(self):
        return self.all_in_edges

    def get_All_out_edges(self):
        return self.all_out_edges

    def add_In_edge(self, otherId, weight):
        self.all_in_edges[otherId] = weight

    def add_Out_edge(self, otherId, weight):
        self.all_out_edges[otherId] = weight

    def remove_In_edge(self, otherId):
        return self.all_in_edges.pop(otherId)

    def remove_Out_edge(self, otherId):
        return self.all_out_edges.pop(otherId)

    def __repr__(self):
        return "{}: |edges out| {} |edges in| {}".format(self.Id, len(self.all_out_edges), len(self.all_in_edges))

    def __str__(self):
        return "Id: {}\nTag: {}\npos: {}\nIncoming Edges: {}\nOutgoing Edges: {}\n".format(self.Id, self.tag, self.pos,
                                                                                           self.all_in_edges,
                                                                                           self.all_out_edges)
