from graph import Graph
from tkinter import *
import tkinter.messagebox
import random


class GameState:
    '''
    Class carrying bool that tells if game has ended
    '''
    state = False


def computer_player(mode: int, buttons: list, g: Graph, cycle: list = None) -> None:
    # Operates the simple computer player
    # modes of the player:
    # 0 - normal move
    # 1 - choosing the square to collapse
    # 2 - choosing the item to collapse
    if mode == 0 and not GameState.state:
        move1 = -1
        for i in range(0, 2):
            rand = random.randint(0, 8)
            if g.is_untouchable(rand) or rand == move1:
                while g.is_untouchable(rand) or rand == move1:
                    rand = random.randint(0, 8)
                btn_pressed(buttons[rand], buttons)
                move1 = rand
            else:
                btn_pressed(buttons[rand], buttons)
                move1 = rand
    elif mode == 1 and not GameState.state:
        rand = random.randint(0, len(all_buttons[0])-1)
        square_choice_btn_pressed(all_buttons[0][rand], g, cycle, buttons)
    elif mode == 2 and not GameState.state:
        index = random.randint(0, len(all_buttons[2])-1)
        rand = all_buttons[2][index]
        element_choice_btn_pressed(g, cycle, rand, buttons)

# Basic functions
def if_not_first_move(move_id: int) -> bool:
    # checks if it is the first move of the game
    return False if move_id==1 else True

def show_board(graph: Graph) -> None:
    # Displays the gameboard in the console
    for v in graph.get_board():
        print(v)

def who(number: int) -> str:
    # Returns the character which will be placed in the board instead of nodes' id
    if number%4==1 or number%4==2:
        return 'X'
    return 'O'

def get_symbol(number: int) -> str:
    # returns human-friendly node ID
    if number%4==1 or number%4==2:
        if number%2==0:
            res = f"X{int(number/2)}"
        else:
            res = f"X{int((number+1)/2)}"
    else:
        if number%2==0:
            res = f"O{int(number/2)}"
        else:
            res = f"O{int((number+1)/2)}"
    return res

def update_board(gph: Graph, buttons: list) -> None:
    # Updates the GUI board
    board = gph.get_board()
    enable_all_buttons(buttons)
    for i in range(0, 9):
        # change background and enable buttons
        if gph.is_untouchable(i):
            buttons[i].configure(bg='#cccccc')
            buttons[i].configure(state=DISABLED)
            res = get_symbol(board[i][0])
            buttons[i]['text'] = str(res)

# Button functions
def disable_all_buttons(buttons: list) -> None:
    # Disables all board-buttons
    for b in buttons:
        b.configure(state=DISABLED)

def enable_all_buttons(buttons: list) -> None:
    # Enables all board-buttons
    for b in buttons:
        b.configure(state=NORMAL)

def destroy_all_choice_buttons() -> None:
    # Removes side buttons for slim and pretty look
    # print('Buttons destroyed')
    for i in range(0, 2):
        for button in all_buttons[i]:
            button.destroy()
    while len(all_buttons) > 0:
        del all_buttons[0]

def handle_win(result: set, gph: Graph) -> None:
    # Displays who won the game
    if result is None:
        tkinter.messagebox.showinfo('Results', f"DRAW")
    else:
        if len(result) > 1:
            if move_id%4==0:
                tkinter.messagebox.showinfo('Results', f"Winner: O: 1pt\nX: 0.5pt")   
            else:
                tkinter.messagebox.showinfo('Results', f"Winner: X: 1pt\nO: 0.5pt") 
        else:
            tkinter.messagebox.showinfo('Results', f"Winner: {check_results(gph)[1].pop()}")

def element_choice_btn_pressed(gph: Graph, cycle: list, c_choice: int, buttons: list) -> None:
    # Operates on the player's node choice and handles the win 
    choice_upper = c_choice 
    gph.handle_collapse(cycle, choice_upper)
    update_board(gph, buttons)
    label_choice1['text'] = ""
    destroy_all_choice_buttons()
    if check_results(gph)[0]:
        GameState.state = True
        for b in buttons:
            b.configure(state=DISABLED)
        handle_win(check_results(gph)[1], gph)

def square_choice_btn_pressed(button: Button, gph: Graph, cycle: list, buttons: list) -> None:
    # Operates on the player's square choice
    choice = int(button['text']) - 1 
    correct_v_choice = gph.get_correct_square_to_choose(cycle, choice)
    choice2_buttons = []
    i = 5
    # Creating new buttons for choosing the node to collapse
    for c_choice in correct_v_choice:
        result = get_symbol(c_choice)
        button = Button(tk, text=result, bg='white', height=1, width=2)
        button.configure(command=lambda gph=gph, cycle=cycle, c_choice=c_choice, buttons=buttons : element_choice_btn_pressed(gph, cycle, c_choice, buttons))
        button.grid(row=2, column=i)
        i += 1
        choice2_buttons.append(button)
    all_buttons.append(choice2_buttons)
    all_buttons.append(correct_v_choice)
    if move_id%4 == 2:
        computer_player(2, buttons, gph, cycle)

def btn_pressed(button: Button, buttons: list) -> bool:
    # Handles player's normal moves
    global move_id, which_player, g
    index = buttons.index(button)
    if g.is_untouchable(index):
        tkinter.messagebox.showinfo('Error', 'You can\'t use this button')
        return False
    if move_id%2 == 0 and (move_id-1 in g.get_all_vertexes_in_given_square(index)):
        tkinter.messagebox.showinfo('Error', 'You already put something in here')
        return False
    g.add_vertex(move_id, index)
    res = get_symbol(move_id)
    button['text'] += f" {res}"
    if if_not_first_move(move_id) and move_id%2 == 0:
        g.add_edge(move_id, move_id-1)
    for vertex in g.get_all_vertexes_in_given_square(index):
        if vertex != move_id:
            g.add_edge(move_id, vertex)
    show_board(g)
    print("-----------------------")
    g.show_graph()
    if move_id%2 == 0 and g.is_cyclic()[0]:
        cycle = g.is_cyclic()[1]
        # print("Graph has a cycle" + f"{cycle}")
        handle_cycle(cycle, move_id, g, buttons)
        if GameState.state:
            return False
        # show_board(g)
        # print(f"The end | Winner: {check_results(g)[1]}")
    if move_id%2 == 0:
        which_player = not which_player
    move_id += 1
    label['text'] = f"{str('X' if not which_player else 'O')}'s turn"
    if move_id%4 == 3 and not GameState.state:
        computer_player(0, buttons, g)
    return True

# Handlers
def handle_cycle(cycle: list, move_id_temp: int, gph: Graph, buttons: list) -> None:
    # Handles situation when the cycle is discovered and further actions are needed
    cycled_squares = set([])
    for c in cycle:
        cycled_squares.add(g.get_square_index(c))
    for c in cycled_squares:
        buttons[c].configure(bg='#03bafc')
    disable_all_buttons(buttons)
    tkinter.messagebox.showinfo('Cycle', f'The cycle has been found\n{who(move_id_temp+1)} is choosing')
    label_choice1.configure(width=12)
    label_choice1['text'] = "Squares available"
    i = 5
    # Creates new buttons for choosing the square
    choice1_buttons = []
    for c in cycled_squares:
        button = Button(tk, text=c+1, bg='white', height=1, width=1)
        button.configure(command=lambda button=button, gph=gph, cycle=cycle, buttons=buttons: square_choice_btn_pressed(button, gph, cycle, buttons))
        button.grid(row=1, column=i)
        i += 1
        choice1_buttons.append(button)
    all_buttons.append(choice1_buttons)
    if move_id%4 == 2:
        computer_player(1, buttons, gph, cycle=cycle)

# Checking functions
def check_row(graph: Graph, row_number: int) -> (bool, str):
    # checks all rows to find the winning situation
    row_number *= 3
    if len(graph.get_board()[row_number]) == 0:
        return False, None
    pos = who(graph.get_board()[row_number][0])
    for i in range(row_number, row_number+3):
        if len(graph.get_board()[i]) == 0:
            return False, None
        if not graph.is_untouchable(i) or who(graph.get_board()[i][0]) != pos:
            return False, None
    return True, who(graph.get_board()[row_number][0])

def check_column(graph: Graph, column_number: int) -> (bool, str):
    # Checks all columns to find the winning situation
    if len(graph.get_board()[column_number]) == 0:
        return False, None
    pos = who(graph.get_board()[column_number][0])
    for i in range(column_number, 9, 3):
        if len(graph.get_board()[i]) == 0:
            return False, None
        if not graph.is_untouchable(i) or who(graph.get_board()[i][0]) != pos:
            return False, None
    return True, who(graph.get_board()[column_number][0])

def check_X_pattern_left_high(graph: Graph) -> (bool, str):
    # Checks if one part of X pattern occurs
    if len(graph.get_board()[0]) == 0:
        return False, None
    pos = who(graph.get_board()[0][0])
    for i in range(0, 9, 4):
        if len(graph.get_board()[i]) == 0:
            return False, None
        if not graph.is_untouchable(i) or who(graph.get_board()[i][0]) != pos:
            return False, None
    return True, who(graph.get_board()[0][0])

def check_X_pattern_left_low(graph: Graph) -> (bool, str):
    # Checks if one part of X pattern occurs
    if len(graph.get_board()[2]) == 0:
        return False, None
    pos = who(graph.get_board()[2][0])
    for i in range(2, 8, 2):
        if len(graph.get_board()[i]) == 0:
            return False, None
        if not graph.is_untouchable(i) or who(graph.get_board()[i][0]) != pos:
            return False, None
    return True, who(graph.get_board()[2][0])

def check_results(graph: Graph) -> (bool, set):
    # Returns tuple (True, who) if game ends
    # Possibilities:
    # X wins
    # O wins
    # both win
    # draw
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
    else:
        res = 0
        for i in range(0, len(graph.get_board())):
            if graph.is_untouchable(i):
                res += 1
        if res == 9:
            return True, None
    return False, None



tk = Tk()
tk.title("Quantum Tic Tac Toe")
g = Graph() # initializing a new graph
GameState.state = False
move_id = 1 # movement counter
which_player = False # False -> X, True -> O
all_buttons = []

label = Label(tk, text="X's turn", height=1, width=12)
label.grid(row=1, column=0)
buttons = []
# Constructing board from buttons
for row in range(2, 5):
    for column in range(0, 3):
        button = Button(tk, text=" ", bg='white', height=5, width=12)
        button.configure(command=lambda button=button, buttons=buttons: btn_pressed(button, buttons))
        button.grid(row=row, column=column)
        buttons.append(button)

label_choice1 = Label(tk, text="", height=1, width=0)
label_choice1.grid(row=0, column=4)

tk.mainloop()
