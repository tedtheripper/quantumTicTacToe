class Vertex: # Wierzchołek
    def __init__(self, id: int, square_index: int):
        # identyfikacja po id, 1 i 2 to X a 3 i 4 to Y itd
        self._id = id
        self._neighbours = []
        self._color = None # Once set, cannot be changed
        # Blue is for correct vertexes and red is for bad ones
        # None if the vertexes has not yet been in any cycle
        self._square_index = square_index
        self._is_untouchable = False

    def get_neighbours(self):
        return self._neighbours

    def add_neighbour(self, id):
        if id not in self._neighbours:
            self._neighbours.append(id)

    def remove_neighbour(self, id):
        if id in self._neighbours:
            self._neighbours.remove(id)

    def clean_neighbours(self):
        self._neighbours = []

    def get_color(self):
        return self._color
    
    def set_color(self, color):
        if self._color is None:
            self._color = color

    def get_index(self):
        return self._square_index

    def set_index(self, index):
        self._square_index = index

    def set_is_untouchable(self, touch=True):
        self._is_untouchable = touch
    
    def get_is_untouchable(self):
        return self._is_untouchable