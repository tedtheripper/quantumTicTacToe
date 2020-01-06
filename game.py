from graph import Vertex, Graph

# REWRITE THIS AS CLASSES WITH METHODS for further use

def if_not_first_move(move_id):
    return False if move_id==1 else True

def show_board():
    for square in game_array:
        # print(f"{game_array.index(square) + 1}: ", end=' ')
        print(square)

def handle_cycle(cycle, move_id_temp):
    cycled_squares = set([])
    for square in game_array:
        for c in cycle:
            if c in square:
                cycled_squares.add(game_array.index(square)+1)
    print(f"Choose one square from the cycle: {cycled_squares}")
    choice = int(input())
    print(f"Which one of the element would you like to keep in here? {game_array[choice-1]}")
    # add showing (X1, O4, etc) and chosing only those which are in the cycle
    choice_upper = int(input())
    to_remove = []
    for item in game_array[choice-1]:
        if item != choice_upper:
            to_remove.append(item)
    if choice_upper%2 == 0 :
        g.remove_vertex(choice_upper-1)
    else:
        g.remove_vertex(choice_upper+1)
    removing(to_remove)

def removing_util(to_remove_t, start):
    temp = []
    for tbr in to_remove_t:
        for n in g.get_neighbours(tbr):
            temp.append(n)
    if len(temp) > 0:
        g.remove_vertex(to_remove_t[0])
    

def removing(to_remove_t):
    while len(to_remove_t) > 0:
        pass
        # removing_util()


g = Graph()

game_array = [[], [], [], [], [], [], [], [], []]
game_final_array = []
game_end = False
move_id = 1 # number of the player's movement
which_player = False # False -> X, True -> O

for i in range(0, 10):
    game_final_array.append(-1)

while not game_end:
    print(f"Now plays: {str('X' if not which_player else 'O')}")
    print("input the index of the block <1, 9>: ")
    user_move = int(input()) - 1    # indexing starts at 0
    game_array[user_move].append(move_id)
    if move_id%2 == 0 and (move_id-1 not in game_array[user_move]):
        pass   # add an option for user's error
    g.add_vertex(move_id)
    if if_not_first_move(move_id) and move_id%2 == 0:
        g.add_edge(move_id, move_id-1)
    for vertex in game_array[user_move]:
        if vertex != move_id:
            g.add_edge(move_id, vertex)
    show_board()
    print("-----------------------")
    g.show_graph()
    if move_id%2 == 0 and g.is_cyclic()[0]:
        game_end = True
        cycle = g.is_cyclic()[1]
        for elem in cycle:
            if elem%2==0 and elem-1 not in cycle:
                cycle.remove(elem)
            if elem%2==1 and elem+1 not in cycle:
                cycle.remove(elem)
        print("Graph has a cycle" + f"{cycle}")
        handle_cycle(cycle, move_id)
    if move_id%2 == 0:
        which_player = not which_player
    move_id += 1
    