from collections import defaultdict

from produce_graph_data import G
from singleton import Singleton


class Graph(object):
    __metaclass__ = Singleton

    def __init__(self, edge_lst_graph):
        self.edge_lst_graph = edge_lst_graph

    def add_edge(self, u, v):
        self.graph.append([u, v])

    def extend_edges(self, edgeList):
        self.graph = self.edge_lst_graph + edgeList


class AdjacencyLstGraph(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def adjacency_lst_to_edge_lst(self, adjacency_lst_graph):
        edgeListGraph = EdgeLstGraph()

        for vertex in adjacency_lst_graph.graph.keys():
            for child in adjacency_lst_graph.graph[vertex]:
                edgeListGraph.add_edge(vertex, child)

        return edgeListGraph


class EdgeLstGraph(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.graph = []

    def add_edge(self, u, v):
        self.graph.append([u, v])

    def add_all_edges_at_once(self, edge_lst):
        self.graph = edge_lst

    def edge_lst_to_adjacency_lst(self, edge_lst_graph):
        adjacencyListGraph = AdjacencyLstGraph()

        for edge in edge_lst_graph.graph:
            adjacencyListGraph.add_edge(edge[0], edge[1])

        return adjacencyListGraph


class DetectCycleInDirectedGraph(Graph):
    __metaclass__ = Singleton

    def __init__(self, edge_lst_graph):
        Graph.__init__(self, edge_lst_graph)
        self.vertex_size = len(set([n for e in edge_lst_graph for n in e]))

    @staticmethod
    def relieve_type_binding(edge_lst_graph):
        visited = set()
        vertex_int_dict = {}
        vertex_size = len(set([n for e in edge_lst_graph for n in e]))

        def tuple_to_list(lst):
            for i in xrange(
                    len(lst)):  # Convert the tuple element in the list to a list, readable and writable
                if isinstance(lst[i], tuple):
                    lst[i] = list(lst[i])
                else:
                    raise ValueError('element should be a tuple')
            return lst

        for edge in edge_lst_graph:
            for vertex in edge:
                if vertex not in visited:
                    visited.add(vertex)

        for (num, vertex) in zip(xrange(vertex_size), visited):
            vertex_int_dict[vertex] = num

        edge_lst_graph = tuple_to_list(edge_lst_graph)

        for vertex in edge_lst_graph:
            for index in xrange(len(vertex)):
                if vertex[index] in vertex_int_dict.keys():
                    vertex[index] = vertex_int_dict[vertex[index]]

        return filter(lambda x: x[0] != x[1], edge_lst_graph)

    def is_cyclic(self):
        self.edge_lst_graph = self.relieve_type_binding(self.edge_lst_graph)
        clen = len(self.edge_lst_graph)
        if clen == 0:  # Return False if the graph is empty
            print "Graph has no cycle because it is empty"
            return False

        in_degrees = [0 for _ in range(self.vertex_size)]
        adjacency = [set() for _ in range(self.vertex_size)]

        for second, first in self.edge_lst_graph:
            in_degrees[second] += 1
            adjacency[first].add(second)

        queue = []
        for i in range(self.vertex_size):
            if in_degrees[i] == 0:
                queue.append(i)
        counter = 0
        while queue:
            top = queue.pop(0)
            counter += 1

            # In the case of a ring, the effect of the same element in it is
            # eliminated
            for successor in adjacency[top]:
                in_degrees[successor] -= 1
                if in_degrees[successor] == 0:
                    queue.append(successor)

        if counter == self.vertex_size:
            print "Graph has no cycle"
            return False
        else:
            print "Graph has cycle"
            return True


if __name__ == '__main__':
    DetectCycleInDirectedGraph(G).is_cyclic()
