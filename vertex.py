class Vertex: # Node class
    '''
    Class Vertex. Represents a single node in the graph as an object
    :param __id: vertex's id
    :type __id: int
    :param __neighbours: list of node's neighbours
    :type __neighbours: list
    :param __color: color of the node used to indicate its usefulness
    :type __color: str
    :param __square_index: index of the square in which node is located
    :type __square_index: int
    :param __is_untouchable: represents node's mutability
    :type __is_untouchable: bool
    '''
    def __init__(self, id: int, square_index: int):
        # identification by id, 1 & 2 is X and 3 & 4 is Y etc
        self.__id = id
        self.__neighbours = []
        self.__color = None # Once set, cannot be changed
        # Blue is for correct vertexes and red is for nto necessary ones
        # None if the vertexes has not yet been in any cycle
        self.__square_index = square_index
        self.__is_untouchable = False

    def get_neighbours(self) -> list:
        return self.__neighbours

    def add_neighbour(self, id: int) -> None:
        if id not in self.__neighbours:
            self.__neighbours.append(id)

    def remove_neighbour(self, id: int) -> None:
        if id in self.__neighbours:
            self.__neighbours.remove(id)

    def clean_neighbours(self) -> None:
        self.__neighbours = []

    def get_color(self) -> str:
        return self.__color
    
    def set_color(self, color: str) -> None:
        if self.__color is None:
            self.__color = color

    def get_index(self) -> int:
        return self.__square_index

    def set_index(self, index: int) -> None:
        self.__square_index = index

    def set_is_untouchable(self, touch: bool = True) -> None:
        # sets the vertex immutability
        self.__is_untouchable = touch
    
    def get_is_untouchable(self) -> bool:
        return self.__is_untouchable