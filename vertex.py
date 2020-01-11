class Vertex: # Wierzchołek
    def __init__(self, id: int, square_index: int):
        # identyfikacja po id, 1 i 2 to X a 3 i 4 to Y itd
        self.__id = id
        self.__neighbours = []
        self.__color = None # Once set, cannot be changed
        # Blue is for correct vertexes and red is for bad ones
        # None if the vertexes has not yet been in any cycle
        self.__square_index = square_index
        self.__is_untouchable = False

    def get_neighbours(self):
        return self.__neighbours

    def add_neighbour(self, id):
        if id not in self.__neighbours:
            self.__neighbours.append(id)

    def remove_neighbour(self, id):
        if id in self.__neighbours:
            self.__neighbours.remove(id)

    def clean_neighbours(self):
        self.__neighbours = []

    def get_color(self):
        return self.__color
    
    def set_color(self, color):
        if self.__color is None:
            self.__color = color

    def get_index(self):
        return self.__square_index

    def set_index(self, index):
        self.__square_index = index

    def set_is_untouchable(self, touch=True):
        self.__is_untouchable = touch
    
    def get_is_untouchable(self):
        return self.__is_untouchable