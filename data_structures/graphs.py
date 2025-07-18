class Graph:

    class Vertex:
        __slots__ = '_item'

        def __init__(self, item):
            self._item = item

        def item(self):
            return self._item

        def __hash__(self):
            return hash(id(self))
        
        def __str__(self):
            return str(self._item)

    class Edge:
        __slots__ = '_origin', '_destination', '_item'

        def __init__(self, origin, destination, item):
            self._origin = origin
            self._destination = destination
            self._item = item

        def item(self):
            return self._item

        def __hash__(self):
            return hash((self._origin, self._destination))
        
        def __str__(self):
            return f"({self._origin}, {self._destination}, {self._item})"
        
        def endpoints(self):
            return self._origin, self._destination

        def opposite(self, vertex):
            return self._destination if vertex is self._origin else self._origin

    def __init__(self, directed=False):
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing

    def is_directed(self):
        return self._incoming is not self._outgoing

    def vertex_count(self):
        return len(self._outgoing)

    def vertices(self):
        return self._outgoing.keys()

    def edge_count(self):
        total = sum(len(self._outgoing[vertex]) for vertex in self._outgoing)

        return total if self.is_directed() else total // 2

    def edges(self):
        result = set()

        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())

        return result

    def get_edge(self, origin, destination):
        self._validate_vertex(origin)
        self._validate_vertex(destination)

        return self._outgoing[origin].get(destination)

    def degree(self, vertex, outgoing=True):
        self._validate_vertex(vertex)

        adjacent = self._outgoing if outgoing else self._incoming

        return len(adjacent[vertex])

    def incident_edges(self, vertex, outgoing=True):
        self._validate_vertex(vertex)

        adjacent = self._outgoing if outgoing else self._incoming

        for edge in adjacent[vertex].values():
            yield edge

    def insert_vertex(self, item=None):
        vertex = self.Vertex(item)
        self._outgoing[vertex] = {}

        if self.is_directed():
            self._incoming[vertex] = {}

        return vertex

    def insert_edge(self, origin, destination, item=None):
        if self.get_edge(origin, destination) is not None:
            raise ValueError("Vertices are already adjacent.")

        edge = self.Edge(origin, destination, item)
        self._outgoing[origin][destination] = edge
        self._incoming[destination][origin] = edge

    def _validate_vertex(self, vertex):
        if not isinstance(vertex, self.Vertex):
            raise TypeError("Object is not a vertex.")

        if vertex not in self._outgoing:
            raise ValueError("Vertex does not belong to graph.")