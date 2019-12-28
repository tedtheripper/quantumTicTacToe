from graph import Vertex, Graph

def if_not_first_move(move_id):
    return move_id==1 if True else False

def show_board():
    for square in game_array:
        

g = Graph()

game_array = [[], [], [], [], [], [], [], [], []]
game_end = False
move_id = 1 # number of the player's movement

while not game_end:
    print("input the index of the block <1, 9>: ")
    user_move = int(input()) - 1    # indexing starts at 0
    if move_id%2 == 0 and (move_id-1 not in game_array[user_move]):
        game_array[user_move].append(move_id)   # add an option for user's error
    g.add_vertex(move_id)
    if if_not_first_move(move_id):
        g.add_edge(move_id, move_id-1)
    for vertex in game_array[user_move]:
        if vertex != move_id:
            g.add_edge(move_id, vertex)
    
     
    move_id += 1
