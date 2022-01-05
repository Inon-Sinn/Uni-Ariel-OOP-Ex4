from Model.DiGraph import Node


class MinHeap:

    def __init__(self):
        # heap containing tuple (weight, nodeId)
        self.heap = []
        # the first value in the heap at index 0 is None
        self.heap.append(None)
        # dictionary maps id(a.k.a key) to index (a.k.a value) inside the heap
        self.keyToIndex = {int: int}

    def size(self) -> int:
        return len(self.heap)

    def swim(self, IdNode):
        indexOfNode = self.keyToIndex[IdNode]
        if indexOfNode == 1:
            return
        parentIndex = int(indexOfNode / 2)
        if self.heap[parentIndex][0] > self.heap[indexOfNode][0]:
            self.swap(self.heap[parentIndex][1], IdNode)
            self.swim(self.heap[parentIndex][1])

    def sink(self, parentId):
        parentIndex = self.keyToIndex.get(parentId)
        if parentIndex >= self.size():
            return
        parentIndex = parentId
        leftChildIndex = parentIndex * 2
        rightChildIndex = parentIndex * 2 + 1
        if leftChildIndex >= self.size():
            return
        # parent bigger than left child and right not exist, swap and call sink
        elif rightChildIndex >= self.size():
            if self.heap[leftChildIndex][0] < self.heap[parentIndex][0]:
                self.swap(self.heap[leftChildIndex][1], self.heap[parentIndex][1])
                self.sink(leftChildIndex)
        # parent bigger than the minimal of right and left, swap them and call recursivly
        else:
            # take child with minimal weight
            minimumChild = leftChildIndex if self.heap[leftChildIndex][0] < self.heap[rightChildIndex][0] else rightChildIndex
            if self.heap[minimumChild][0] < self.heap[parentIndex][0]:
                self.swap(self.heap[minimumChild][1], self.heap[parentIndex][1])
                self.sink(minimumChild)

    def insert(self, weight, nodeId):
        if weight is None or nodeId is None:
            raise RuntimeWarning("Cant add null to heap")
        self.heap.append((weight, nodeId))
        self.keyToIndex[nodeId] = self.size() - 1
        self.swim(nodeId)

    def removeMin(self) -> int:
        self.swap(self.heap[1][1], self.heap[(self.size() - 1)][1])
        minimalNode = self.heap.pop(self.size() - 1)
        self.sink(1)
        return minimalNode[1]

    def remove(self, nodeId) -> Node:
        index = self.keyToIndex[nodeId]
        self.swap(self.heap[index][1], self.heap[(len(self.heap) - 1)][1])
        resNodeId = self.heap.pop(self.size() - 1)[1]
        self.sink(resNodeId)
        return resNodeId

    def isEmpty(self):
        return self.size() == 1

    def DecreaseKey(self, NodeId, weight):

        try:
            nodeIndex = self.keyToIndex.get(NodeId)
            if weight < self.heap[nodeIndex][0]:
                self.heap.pop(nodeIndex)
                self.heap.insert(nodeIndex, (weight, NodeId));
                self.swim(NodeId)
        except KeyError:
            print("Node Id inserted at DecreaseKey Does not exist!")

    def swap(self, iId, jId):
        # swaps the indexes respectively to their location
        iIndex = self.keyToIndex[iId]
        jIndex = self.keyToIndex[jId]
        self.heap[iIndex], self.heap[jIndex] = self.heap[jIndex], self.heap[iIndex]
        self.keyToIndex[iId] = jIndex
        self.keyToIndex[jId] = iIndex
