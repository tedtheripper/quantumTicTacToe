from vertex import Vertex


class Graph:  # Graph
    '''
    Class Graph. Represents relations which are costructed on the gameboard
    Contains attributes:
    :param vertexes: container for keeping all nodes
    :type vertexes: dictionary
    '''

    def __init__(self):
        # Constructs graph with empty vertex dictionary
        self.vertexes = {}

    def add_vertex(self, inc_id: int, square_index: int) -> None:
        # Adding new node to the graph
        self.vertexes[inc_id] = Vertex(inc_id, square_index)

    def remove_vertex(self, inc_id: int) -> None:
        # Removing existing node from the graph
        for n in self.vertexes[inc_id].get_neighbours():
            self.vertexes[n].remove_neighbour(inc_id)
        self.vertexes[inc_id].clean_neighbours()
        del self.vertexes[inc_id]

    def add_edge(self, id1: int, id2: int) -> None:
        # Adding edges to nodes in the graph
        self.vertexes[id1].add_neighbour(id2)
        self.vertexes[id2].add_neighbour(id1)

    def vertex_exist(self, id: int) -> bool:
        # Checks if node exists
        return id in self.vertexes.keys()

    def get_neighbours(self, id: int) -> list:
        # Returns all neighbours of given node
        return self.vertexes[id].get_neighbours()

    def get_square_index(self, id: int) -> int:
        # Returns index of square containing given node
        return self.vertexes[id].get_index()

    def get_board(self) -> list:
        # Returns whole gameboard in very convinient form
        board = [[], [], [], [], [], [], [], [], []]
        for v in self.vertexes.keys():
            board[self.get_square_index(v)].append(v)
        return board

    def get_all_vertexes_in_given_square(self, square_ix: int) -> list:
        # Returns every node in given square on the board
        result = []
        for v in self.vertexes.keys():
            if self.vertexes[v].get_index() == square_ix:
                result.append(v)
        return result

    def show_graph(self) -> None:
        # Displays graph relations
        for v in self.vertexes.keys():
            print(f"{v} : {self.vertexes[v].get_neighbours()}")
        print("\n")

    def is_cyclic_utility(self, v: int, visited: list, parent: int, cycle_elements: list, last: list) -> bool:
        # Tool for correct cycle discovering
        visited[v] = True
        for n in self.vertexes[v].get_neighbours():
            if not visited[n]:
                if self.is_cyclic_utility(n, visited, v, cycle_elements, last):
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

    def is_cyclic(self) -> bool:
        # Checks if current craph contains any cycle (DFS algorithm)
        visited = {}
        cycle_elements = []
        last = []
        # rec_stack = {}
        for v in self.vertexes.keys():
            visited[v] = False
            # rec_stack[v] = False
        for v in self.vertexes.keys():
            if not visited[v]:
                if self.is_cyclic_utility(v, visited, -1, cycle_elements, last):
                    for square in self.get_board():  # checks if cycle isn't inside one square
                        res = all(elem in square for elem in cycle_elements)
                        if res:
                            print('Cycle is inside one square')
                            return False, None
                    return True, cycle_elements
        return False, None

    def is_untouchable(self, sq: int) -> bool:
        # Checks square's mutability
        vs = self.get_all_vertexes_in_given_square(sq)
        if len(vs) > 0 and self.vertexes[vs[0]].get_is_untouchable():
            return True
        return False

    def show_colored_graph(self) -> None:
        # Displays colors of the graph's nodes
        for v in self.vertexes.keys():
            print(f"{v}: {self.vertexes[v].get_color()}")

    def all_colored_in_graph(self, cycle: list) -> bool:
        # Checks if every node in the cycle has been colored
        for v in cycle:
            if not self.vertexes[v].get_color():
                return False
        return True

    def get_correct_square_to_choose(self, cycle: list, id: int) -> list:
        # Returns list of correct squares to choose from when collapse is happening
        vert = self.get_correct_cycle(cycle)
        square = self.get_all_vertexes_in_given_square(id)
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
        for vertex_id in self.vertexes.keys():
            if self.vertexes[vertex_id].get_color() == 'Red':
                to_be_removed.append(vertex_id)
            if self.vertexes[vertex_id].get_color() == 'Blue':
                self.vertexes[vertex_id].set_is_untouchable()
        for v in to_be_removed:
            self.remove_vertex(v)

    def handle_collapse(self, cycle: list, choice: int) -> None:
        # Responsible for correct graph coloring (Blue, Red)
        self.vertexes[choice].set_color('Blue')
        if choice % 2 == 0:
            self.vertexes[choice-1].set_color('Red')
        else:
            self.vertexes[choice+1].set_color('Red')
        while not self.all_colored_in_graph(cycle):
            for v in cycle:
                if self.vertexes[v].get_color() == 'Blue':
                    for n in self.vertexes[v].get_neighbours():
                        if not self.vertexes[n].get_color():
                            self.vertexes[n].set_color('Red')
                            if n % 2 == 0:
                                if not self.vertexes[n-1].get_color():
                                    self.vertexes[n-1].set_color('Blue')
                            else:
                                if not self.vertexes[n+1].get_color():
                                    self.vertexes[n+1].set_color('Blue')
        board = self.get_board()
        for sq in board:
            vs = self.get_all_vertexes_in_given_square(board.index(sq))
            for v in vs:
                if self.vertexes[v].get_color() == 'Blue':
                    for v in vs:
                        if not self.vertexes[v].get_color():
                            self.vertexes[v].set_color('Red')
        for v in self.vertexes.keys():
            if self.vertexes[v].get_color() == 'Blue':
                if v % 2 == 0:
                    if v-1 in self.vertexes.keys():
                        self.vertexes[v-1].set_color('Red')
                else:
                    if v+1 in self.vertexes.keys():
                        self.vertexes[v+1].set_color('Red')
            if self.vertexes[v].get_color() == 'Red':
                if v % 2 == 0:
                    if v-1 in self.vertexes.keys():
                        self.vertexes[v-1].set_color('Blue')
                else:
                    if v+1 in self.vertexes.keys():
                        self.vertexes[v+1].set_color('Blue')
        self.handle_collapse_delete()
        self.show_colored_graph()
