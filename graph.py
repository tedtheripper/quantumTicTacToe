class Vertex: # Wierzchołek
    def __init__(self, id):
        # identyfikacja po id, 1 i 2 to X a 3 i 4 to Y
        self._id = id
        self.neighbours = []
    
    def get_edges(self):
        return self.neighbours

class Edge: # Krawędź       MAY NOT BE USED
    def __init__(self, first_node, second_node):
        self._f_node = first_node
        self._s_node = second_node

class Graph: # Graf
    # TODO: implement the graph class that defines and checks internal loops
    def __init__(self):
        self.vertexes = {}

    def add_vertex(self, inc_id):
        self.vertexes[inc_id] = Vertex(inc_id)

    def add_edge(self, id1, id2):
        self.vertexes[id1].neighbours.append(id2)
        self.vertexes[id2].neighbours.append(id1)

    def vertex_exist(self, id):
        return id in self.vertexes.keys()

    def show_graph(self):
        for v in self.vertexes.keys():
            print(f"{v} : {self.vertexes[v].neighbours}")

    def is_cyclic_utility(self, v, visited, parent, cycle_elements):
        visited[v] = True
        for n in self.vertexes[v].neighbours:
            if visited[n] == False:
                if self.is_cyclic_utility(n, visited, v, cycle_elements) == True:
                    cycle_elements.append(v)
                    return True
            elif parent != n:
                cycle_elements.append(v)
                return True
        return False

    def is_cyclic(self):
        visited = {}
        cycle_elements = []
        # rec_stack = {}
        for v in self.vertexes.keys():
            visited[v] = False
            # rec_stack[v] = False
        for v in self.vertexes.keys():
            if visited[v] == False:
                if self.is_cyclic_utility(v, visited, -1, cycle_elements) == True:
                    return True, cycle_elements
        return False, None
