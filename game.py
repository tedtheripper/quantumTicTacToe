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

def who(number):
    if number%4==1 or number%4==2:
        return 'X'
    return 'O'

def check_row(graph: Graph, row_number: int):
    row_number *= 3
    if len(graph.get_board()[row_number]) == 0:
        return False, None
    pos = who(graph.get_board()[row_number][0])
    for i in range(row_number, row_number+3):
        if len(graph.get_board()[i]) == 0:
            return False, None
        if not graph.is_untouchable(i) and who(graph.get_board()[i][0]) != pos:
            return False, None
    return True, who(graph.get_board()[row_number][0])

def check_column(graph: Graph, column_number: int):
    if len(graph.get_board()[column_number]) == 0:
        return False, None
    pos = who(graph.get_board()[column_number][0])
    for i in range(column_number, 9, 3):
        if len(graph.get_board()[i]) == 0:
            return False, None
        if not graph.is_untouchable(i) and who(graph.get_board()[i][0]) != pos:
            return False, None
    return True, who(graph.get_board()[column_number][0])

def check_X_pattern_left_high(graph):
    if len(graph.get_board()[0]) == 0:
        return False, None
    pos = who(graph.get_board()[0][0])
    for i in range(0, 9, 4):
        if len(graph.get_board()[i]) == 0:
            return False, None
        if not graph.is_untouchable(i) and who(graph.get_board()[i][0]) != pos:
            return False, None
    return True, who(graph.get_board()[0][0])

def check_X_pattern_left_low(graph):
    if len(graph.get_board()[2]) == 0:
        return False, None
    pos = who(graph.get_board()[2][0])
    for i in range(2, 8, 2):
        if len(graph.get_board()[i]) == 0:
            return False, None
        if not graph.is_untouchable(i) and who(graph.get_board()[i][0]) != pos:
            return False, None
    return True, who(graph.get_board()[2][0])

def check_results(graph):
    # returns tuple (True, who) if game ends
    # possibilities:
    # X wins
    # O wins
    # both win
    wins = set([])
    for row in range(0, 3):
        if check_row(graph, row)[0]:
            wins.add(check_row(graph, row)[1])
    for column in range(0, 3):
        if check_column(graph, column)[0]:
            wins.add(check_column(graph, column)[1])
    if check_X_pattern_left_high(graph)[0]:
        wins.add(check_X_pattern_left_high(graph)[1])
    if check_X_pattern_left_low(graph)[0]:
        wins.add(check_X_pattern_left_low(graph)[1])
    if len(wins) > 0:
        return True, wins
    return False, None

g = Graph() # initializing a new graph
game_end = False
move_id = 1 # movement counter
which_player = False # False -> X, True -> O

while not game_end:
    print(f"Now plays: {str('X' if not which_player else 'O')}")
    print("input the index of the block <1, 9>: ")
    user_move = int(input()) - 1    # indexing starts at 0
    while g.is_untouchable(user_move):
        print('You cant choose this square1')
        user_move = int(input()) - 1
    while move_id%2 == 0 and (move_id-1 in g.get_all_vertexes_in_given_square(user_move)):
        print('You cant choose this square2')
        user_move = int(input()) - 1  # add an option for user's error
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
        # game_end = True
        cycle = g.is_cyclic()[1]
        print("Graph has a cycle" + f"{cycle}")
        handle_cycle(cycle, move_id, g)
        show_board(g)
        if check_results(g)[0]:
            game_end = True
            print(f"The end | Winner: {check_results(g)[1]}")
    if move_id%2 == 0:
        which_player = not which_player
    move_id += 1
    