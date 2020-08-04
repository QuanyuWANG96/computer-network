import sys

class Vertex:
    def __init__(self, id):
        self.id = id
        self.adjacent = {}  # key : vertex, value : linkID
        self.links = {}  # key : linkID, value : linkCost
        self.visited = False

    def add_neighbor(self, neighbor, linkID):
        self.adjacent[neighbor] = linkID

    def add_link(self, linkID, linkCost):
        self.links[linkID] = linkCost

    def get_all_links(self):
        return self.links.keys()

    def set_visted(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x for x in self.adjacent.keys()])


class Graph:
    def __init__(self):
        self.vertex = {} # key : index i, value : vertex i
        self.num_vertex = 0

    def add_vertex(self, id):
        if id not in self.vertex:
            self.num_vertex += 1
            new_vtx = Vertex(id)
            self.vertex[id] = new_vtx
        return self.vertex[id]

    def get_vertex(self, n):
        if n in self.vertex:
            return self.vertex[n]
        return None

    def add_vertex_link(self, n, linkID, linkCost):
        self.add_vertex(n)
        self.vertex[n].add_link(linkID, linkCost)

    def add_edge(self, start, end, linkID):
        self.add_vertex(start)
        self.add_vertex(end)
        self.vertex[start].add_neighbor(end,linkID)
        self.vertex[end].add_neighbor(start, linkID)
        # print("add edge from " + str(start) + " to " + str(end) + " through link " + str(linkID))
        # print("add edge from " + str(end) + " to " + str(start) + " through link " + str(linkID))

    def get_all_vertex(self):
        return self.vertex.keys()

    def __str__(self):
        for vtx in self.get_all_vertex():
            print("vertex:" + str(vtx))
            print(self.get_vertex(vtx))
        return str([self.vertex[x] for x in self.vertex.keys()])


