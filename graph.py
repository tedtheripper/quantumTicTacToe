from vertex import Vertex


class Graph:  # Graph
    '''
    Class Graph. Represents relations which are costructed on the gameboard
    Contains attributes:
    :param vertices: container for keeping all nodes
    :type vertices: dictionary
    '''

    def __init__(self):
        # Constructs graph with empty vertex dictionary
        self.vertices = {}

    def add_vertex(self, inc_id: int, square_index: int) -> None:
        # Adding new node to the graph
        self.vertices[inc_id] = Vertex(inc_id, square_index)

    def remove_vertex(self, inc_id: int) -> None:
        # Removing existing node from the graph
        for n in self.vertices[inc_id].get_neighbours():
            self.vertices[n].remove_neighbour(inc_id)
        self.vertices[inc_id].clean_neighbours()
        del self.vertices[inc_id]

    def add_edge(self, id1: int, id2: int) -> None:
        # Adding edges to nodes in the graph
        self.vertices[id1].add_neighbour(id2)
        self.vertices[id2].add_neighbour(id1)

    def vertex_exist(self, id: int) -> bool:
        # Checks if node exists
        return id in self.vertices.keys()

    def get_neighbours(self, id: int) -> list:
        # Returns all neighbours of given node
        return self.vertices[id].get_neighbours()

    def get_square_index(self, id: int) -> int:
        # Returns index of square containing given node
        return self.vertices[id].get_index()

    def get_board(self) -> list:
        # Returns whole gameboard in very convinient form
        board = [[], [], [], [], [], [], [], [], []]
        for v in self.vertices.keys():
            board[self.get_square_index(v)].append(v)
        return board

    def get_all_vertices_in_given_square(self, square_ix: int) -> list:
        # Returns every node in given square on the board
        result = []
        for v in self.vertices.keys():
            if self.vertices[v].get_index() == square_ix:
                result.append(v)
        return result

    def show_graph(self) -> None:
        # Displays graph relations
        for v in self.vertices.keys():
            print(f"{v} : {self.vertices[v].get_neighbours()}")
        print("\n")

    '''def has_cycle(self, v: int, parent: int, visited: set) -> bool:
        if v in visited:
            return True
        visited.add(v)
        for u in self.vertices[v].get_neighbours():
            if u != parent and self.has_cycle(u, v, visited):
                return True
        return False'''

    def is_cyclic_utility(self, v: int, visited: list, parent: int, cycle_elements: list, last: list) -> bool:
        # Tool for correct cycle discovering
        visited[v] = True
        for n in self.vertices[v].get_neighbours():
            if not visited[n]:
                if self.is_cyclic_utility(n, visited, v, cycle_elements, last):
                    cycle_elements.append(n)
                    if len(last) > 0:
                        if n == last[0]:
                            last.remove(n)
                    if len(last) > 0:
                        cycle_elements.append(v)
                    return True
            elif parent != n:
                last.append(n)
                cycle_elements.append(v)
                return True
        return False

    def all_in_one_square(self, cycled):
        for sq in self.get_board():
            global full
            full = True
            for c in cycled:
                if c not in sq:
                    full = False
            if full:
                return True
        return False

    def is_cyclic(self) -> bool:
        # Checks if current craph contains any cycle (DFS algorithm)
        visited = {}
        cycle_elements = []
        last = []
        # vis = set([])
        has_cycle = False
        # cycled = []
        # print('Jest Cykl' if self.has_cycle(1, -1, vis) else 'Nie ma cyklu')
        for v in self.vertices.keys():
            visited = {}
            for v in self.vertices.keys():
                visited[v] = False
            cycle_elements = []
            if not visited[v]:
                if self.is_cyclic_utility(v, visited, -1, cycle_elements, last):
                    print(cycle_elements)
                    if self.all_in_one_square(cycle_elements):
                        print('Cycle is inside one square')
                        has_cycle = False
                    else:
                        return True, cycle_elements
        if not has_cycle:
            return False, None

    def is_untouchable(self, sq: int) -> bool:
        # Checks square's mutability
        vs = self.get_all_vertices_in_given_square(sq)
        if len(vs) > 0 and self.vertices[vs[0]].get_is_untouchable():
            return True
        return False

    def show_colored_graph(self) -> None:
        # Displays colors of the graph's nodes
        for v in self.vertices.keys():
            print(f"{v}: {self.vertices[v].get_color()}")

    def all_colored_in_graph(self, cycle: list) -> bool:
        # Checks if every node in the cycle has been colored
        for v in cycle:
            if not self.vertices[v].get_color():
                return False
        return True

    def get_correct_square_to_choose(self, cycle: list, id: int) -> list:
        # Returns list of correct squares to choose from when collapse is happening
        vert = self.get_correct_cycle(cycle)
        square = self.get_all_vertices_in_given_square(id)
        for item in square:
            if item not in vert:
                square.remove(item)
        return square

    def get_correct_cycle(self, cycle: list) -> list:
        # Returns list of correct nodes to choose from when collapse is happening
        correct_v_to_choose = list(cycle)
        for elem in cycle:
            if elem % 2 == 0 and elem-1 not in cycle:
                correct_v_to_choose.remove(elem)
            if elem % 2 == 1 and elem+1 not in cycle:
                correct_v_to_choose.remove(elem)
        return correct_v_to_choose

    def handle_collapse_delete(self) -> None:
        # Removes unnecessary nodes after collapse and blocks rest from being edited
        to_be_removed = []
        for vertex_id in self.vertices.keys():
            if self.vertices[vertex_id].get_color() == 'Red':
                to_be_removed.append(vertex_id)
            if self.vertices[vertex_id].get_color() == 'Blue':
                self.vertices[vertex_id].set_is_untouchable()
        for v in to_be_removed:
            self.remove_vertex(v)

    def handle_collapse(self, cycle: list, choice: int) -> None:
        # Responsible for correct graph coloring (Blue, Red)
        self.vertices[choice].set_color('Blue')
        if choice % 2 == 0:
            self.vertices[choice-1].set_color('Red')
        else:
            self.vertices[choice+1].set_color('Red')
        while not self.all_colored_in_graph(cycle):
            for v in cycle:
                if self.vertices[v].get_color() == 'Blue':
                    for n in self.vertices[v].get_neighbours():
                        if not self.vertices[n].get_color():
                            self.vertices[n].set_color('Red')
                            if n % 2 == 0:
                                if not self.vertices[n-1].get_color():
                                    self.vertices[n-1].set_color('Blue')
                            else:
                                if not self.vertices[n+1].get_color():
                                    self.vertices[n+1].set_color('Blue')
        board = self.get_board()
        for sq in board:
            vs = self.get_all_vertices_in_given_square(board.index(sq))
            for v in vs:
                if self.vertices[v].get_color() == 'Blue':
                    for v in vs:
                        if not self.vertices[v].get_color():
                            self.vertices[v].set_color('Red')
        for v in self.vertices.keys():
            if self.vertices[v].get_color() == 'Blue':
                if v % 2 == 0:
                    if v-1 in self.vertices.keys():
                        self.vertices[v-1].set_color('Red')
                else:
                    if v+1 in self.vertices.keys():
                        self.vertices[v+1].set_color('Red')
            if self.vertices[v].get_color() == 'Red':
                if v % 2 == 0:
                    if v-1 in self.vertices.keys():
                        self.vertices[v-1].set_color('Blue')
                else:
                    if v+1 in self.vertices.keys():
                        self.vertices[v+1].set_color('Blue')
        self.handle_collapse_delete()
        self.show_colored_graph()
