import tkinter as tk
from tkinter import messagebox
import copy
import random

# Global variables
size = 4  # Default starting size
board = []
scores = [0, 0]
turn = 0
player_mode = ""
text = None
entry = None
entry_boxes = None
game_window = None
player_mode_window = None
size_window = None

# Function to create the board structure
def create_board(size):
    return [[[False, False] for _ in range(size)] for _ in range(size)]

def print_board(board, size):
    board_str = ""
    for y in range(size):
        for x in range(size):
            board_str += "•"
            if x < size - 1:
                if board[y][x][0]:
                    board_str += "---"
                else:
                    board_str += "   "
        board_str += "\n"


        if y < size - 1:
            for x in range(size):
                if board[y][x][1]:
                    board_str += "|   "
                else:
                    board_str += "    "
            board_str += "\n"
    current_turn_str = "Player " + str(turn + 1) + "'s turn"
    board_str = current_turn_str + "\n\n" + board_str
    return board_str

    return board_str


def check_move(board, move, size):
    x, y, d = move
    if d not in ['h', 'v']:
        return False
    if d == 'h' and (x < 0 or x >= size - 1 or y < 0 or y >= size):
        return False
    if d == 'v' and (x < 0 or x >= size or y < 0 or y >= size - 1):
        return False
    if (d == 'h' and board[y][x][0]) or (d == 'v' and board[y][x][1]):
        return False
    return True


def add_line(board, move, size):
    directions = {'h': (0, 1), 'v': (1, 0)}
    x, y, d = move
    dx, dy = directions[d]
    if d == 'h':
        board[y][x][0] = True
    elif d == 'v':
        board[y][x][1] = True


def player_turn():
    global turn, scores
    try:
        input_str = entry.get()
        x, y, d = input_str.split(',')
        d = d.strip().lower()
        if d in ['h', 'v']:
            x, y = int(x.strip()), int(y.strip())
            move = (x, y, d)
            if check_move(board, move, size):
                add_line(board, move, size)
                score, boxes_made = evaluate_move(board, move, size)  # اینجا تغییر کرده است
                scores[turn] += boxes_made
                update_gui()
                if score == 0:  # اگر هیچ امتیازی کسب نشده باشد
                    turn = 1 - turn
                if player_mode == "computer" and turn == 1:
                    computer_turn()
                else:
                    entry.delete(0, tk.END)
    except (ValueError, IndexError):
        messagebox.showinfo("Invalid Move", "Invalid input. Format your move as 'x,y,direction' with no spaces and submit again.")
    entry.delete(0, tk.END)


def computer_turn():
    global turn, scores
    move = computer_move(board, size)
    if move:
        add_line(board, move, size)
        # تجزیه move به x, y و direction
        x, y, direction = move
        # فراخوانی تابع evaluate_move با تمام آرگومان‌های لازم
        score, boxes_made = evaluate_move(board, x, y, direction, size)  # تغییر داده شده است
        scores[turn] += boxes_made
        update_gui()
        if boxes_made == 0:
            turn = 1 - turn
            if player_mode == "computer" and turn == 1:
                game_window.after(500, computer_turn)



def update_gui():
    board_str = print_board(board, size)
    scores_str = f"Player 1 Score: {scores[0]}\nPlayer 2 Score: {scores[1]}"
    text.delete(1.0, tk.END)
    text.insert(tk.END, board_str + scores_str)


    if sum(scores) == ((size - 1) * (size - 1)):
        game_over()

# Function to initialize player mode and start size selection
def set_player_mode(mode):
    global player_mode, player_mode_window, size_window
    player_mode = mode
    player_mode_window.destroy()
    # Create the size selection window
    size_window = tk.Toplevel()  # Using Toplevel for secondary window
    size_window.title("Select Board Size")
    size_window.geometry("300x100")
    tk.Label(size_window, text="Select Board Size", font=("Helvetica", 14)).pack(pady=10)
    size_4_button = tk.Button(size_window, text="4x4", command=lambda: set_board_size(4))
    size_4_button.pack(side="left", padx=10)
    size_6_button = tk.Button(size_window, text="6x6", command=lambda: set_board_size(6))
    size_6_button.pack(side="right", padx=10)

# Function to set the board size and start the game
def set_board_size(selected_size):
    global size, board, scores, turn, game_window, size_window
    size = selected_size
    board = create_board(size)
    scores = [0, 0]
    turn = 0
    size_window.destroy()
    game_window.deiconify()
    update_gui()

# Function to update the GUI
def update_gui():
    board_str = print_board(board, size)
    scores_str = f"Player 1 Score: {scores[0]}\nPlayer 2 Score: {scores[1]}"
    text.delete(1.0, tk.END)
    text.insert(tk.END, board_str + scores_str)


    if sum(scores) == ((size - 1) * (size - 1)):
        game_over()


# Player turn handling
def player_turn():
    global turn, scores
    try:
        input_str = entry.get()
        x, y, direction = input_str.split(',')
        direction = direction.strip().lower()
        if direction in ['h', 'v']:
            x, y = int(x.strip()), int(y.strip())
            move = (x, y, direction)
            if check_move(board, move, size):
                add_line(board, move, size)
                # استفاده از x, y, direction بدست آمده از move
                score, boxes_made = evaluate_move(board, x, y, direction, size)
                scores[turn] += boxes_made
                update_gui()
                if boxes_made == 0:
                    turn = 1 - turn
                    
                if player_mode == "computer" and turn == 1:
                    computer_turn()

                entry.delete(0, tk.END)
    except (ValueError, IndexError):
        messagebox.showinfo("Invalid Move", "Invalid input. Format your move as 'x,y,direction' with no spaces and submit again.")
    entry.delete(0, tk.END)

# Functions for computer moves, game evaluation, and game over
def computer_move(board, size):
    # Simple AI for computer turn: Prioritize completing a box, else choose random valid move
    for y in range(size):
        for x in range(size):
            if y < size - 1:
                if not board[y][x][0]:  # Check horizontal lines
                    potential_move = (x, y, 'h')
                    test_board = copy.deepcopy(board)
                    add_line(test_board, potential_move, size)
                    if evaluate_move(test_board, x, y, 'h', size)[0] > 0:  # if it completes a box, return this move
                        return potential_move
            if x < size - 1:
                if not board[y][x][1]:  # Check vertical lines
                    potential_move = (x, y, 'v')
                    test_board = copy.deepcopy(board)
                    add_line(test_board, potential_move, size)
                    if evaluate_move(test_board, x, y, 'v', size)[0] > 0:  # if it completes a box, return this move
                        return potential_move
    # If no immediate scoring move is found, choose a random valid move
    valid_moves = []
    for y in range(size):
        for x in range(size):
            if y < size - 1 and not board[y][x][0]:  # Horizontal lines
                valid_moves.append((x, y, 'h'))
            if x < size - 1 and not board[y][x][1]:  # Vertical lines
                valid_moves.append((x, y, 'v'))
    return random.choice(valid_moves) if valid_moves else None

def game_over():
    winner = "Player 1" if scores[0] > scores[1] else "Player 2" if scores[1] > scores[0] else "It's a tie!"
    messagebox.showinfo("Game Over", f"Game over! Final scores:\nPlayer 1: {scores[0]}\nPlayer 2: {scores[1]}\n{winner}")    

def evaluate_move(board, x, y, direction, size):
    score = 0
    boxes_made = 0


    dx, dy = (0, 1) if direction == 'h' else (1, 0)


    if x - dx >= 0 and x - dx < size - 1 and y - dy >= 0 and y - dy < size - 1:
        if direction == 'h':
            if board[y][x-1][1] and board[y+dy][x-1][1] and board[y][x-1][0]:
                score += 1
                boxes_made += 1
        else:
            if board[y-1][x][0] and board[y-1][x+dx][0] and board[y-1][x][1]:
                score += 1
                boxes_made += 1


    if x >= 0 and x < size - 1 and y >= 0 and y < size - 1:
        if direction == 'h':
            if board[y-dy][x][1] and board[y][x+1][1] and board[y-dy][x][0]:
                score += 1
                boxes_made += 1
        else:
            if board[y][x-dx][0] and board[y+1][x-dx][0] and board[y][x-dx][1]:
                score += 1
                boxes_made += 1


    return score, boxes_made

# Function to create the initial player mode window
def create_player_mode_window():
    window = tk.Toplevel()
    window.title("Select Player Mode")
    window.geometry("300x100")
    tk.Label(window, text="Select Player Mode", font=("Helvetica", 14)).pack(pady=10)
    human_button = tk.Button(window, text="Human", command=lambda: set_player_mode("human"))
    human_button.pack(side="left", padx=10)
    computer_button = tk.Button(window, text="Computer", command=lambda: set_player_mode("computer"))
    computer_button.pack(side="right", padx=10)
    return window

# Function to create the game window
def create_game_window():
    window = tk.Toplevel()
    window.title("Dots and Boxes")
    window.geometry("500x800")
    global text, entry, entry_boxes
    tk.Label(window, text="Dots and Boxes", font=("Helvetica", 16)).pack(pady=10)
    
    # تنظیمات بهتر برای نمایش داشبورد بازی
    text = tk.Text(window, height=20, width=50, bg='lemon chiffon', font=('Helvetica', 14))
    text.pack(padx=10, pady=10)

    tk.Label(window, text="Enter your move (x,y,direction[h/v]):").pack()
    entry = tk.Entry(window, font=('Helvetica', 12), width=10)
    entry.pack(pady=(0, 20))

    # حذف قسمت تعداد جعبه‌ها به دست آمده توسط حرکت - این بخش در منطق بازی خودکار است
    # submit_button با استفاده از event handler عوض شده تا با فشار دادن Enter فعال شود
    entry.bind("<Return>", lambda event: player_turn())
    submit_button = tk.Button(window, text="Submit Move", command=player_turn)
    submit_button.pack(pady=(0, 20))

    return window

# Starting point of the application
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Main Tk instance is hidden
    player_mode_window = create_player_mode_window()  # Create player mode select window
    game_window = create_game_window()  # Create the main game window
    game_window.withdraw()  # Initially hide the game window until board size is selected
    root.mainloop()  # Start the Tkinter event loop