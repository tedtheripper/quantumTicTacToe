from graph import Graph

# REWRITE THIS AS CLASSES WITH METHODS for further use

def if_not_first_move(move_id):
    return False if move_id==1 else True

def show_board(graph):
    for v in graph.get_board():
        print(v)

def handle_cycle(cycle, move_id_temp, gph):
    cycled_squares = set([])
    for c in cycle:
        cycled_squares.add(g.get_square_index(c)+1)
    print(f"Choose one square from the cycle: {cycled_squares}")
    choice = int(input())
    correct_v_choice = gph.get_correct_square_to_choose(cycle, choice-1)
    print(f"Which one of the element would you like to keep in here? {correct_v_choice}")
    # add showing (X1, O4, etc) and chosing only those which are in the cycle
    choice_upper = int(input())
    gph.handle_collapse(cycle, choice_upper)


g = Graph()
# game_array = [[], [], [], [], [], [], [], [], []]
game_end = False
move_id = 1 # movement counter
which_player = False # False -> X, True -> O

while not game_end:
    print(f"Now plays: {str('X' if not which_player else 'O')}")
    print("input the index of the block <1, 9>: ")
    user_move = int(input()) - 1    # indexing starts at 0
    # game_array[user_move].append(move_id)
    if move_id%2 == 0 and (move_id-1 not in g.get_all_vertexes_in_given_square(user_move)):
        pass   # add an option for user's error
    g.add_vertex(move_id, user_move)
    if if_not_first_move(move_id) and move_id%2 == 0:
        g.add_edge(move_id, move_id-1)
    for vertex in g.get_all_vertexes_in_given_square(user_move):
        if vertex != move_id:
            g.add_edge(move_id, vertex)
    show_board(g)
    print("-----------------------")
    g.show_graph()
    if move_id%2 == 0 and g.is_cyclic()[0]:
        game_end = True
        cycle = g.is_cyclic()[1]
        print("Graph has a cycle" + f"{cycle}")
        handle_cycle(cycle, move_id, g)
    if move_id%2 == 0:
        which_player = not which_player
    move_id += 1
    