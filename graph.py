import sys

class Vertex:
    def __init__(self, id):
        self.id = id
        self.adjacent = {}  # key : vertex, value : [linkID, linkCost]
        self.links = {}  # key : linkID, value : linkCost
        self.distance = sys.maxsize
        self.visited = False
        self.next = None

    def add_neighbor(self, neighbor, linkID, linkCost):
        self.adjacent[neighbor] = [linkID]

    def add_link(self, linkID, linkCost):
        self.links[linkID] = linkCost

    def get_all_links(self):
        return self.links.keys()

    def get_all_neighbors(self):
        return self.adjacent.keys()

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_visted(self):
        self.visited = True

    def set_next(self, next):
        self,next = next

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

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

    def add_edge(self, start, end, linkID, linkCost):
        self.add_vertex(start)
        self.add_vertex(end)
        self.vertex[start].add_neighbor(self.vertex[end],linkID, linkCost)
        self.vertex[end].add_neighbor(self.vertex[start], linkID, linkCost)

    def get_all_vertex(self):
        return self.vertex.keys()

