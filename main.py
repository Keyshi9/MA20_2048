# 2048 - Puzzle Game in Python/Tkinter
# Author: Selle Sow | Date: 10/02/2026

import tkinter as tk
import random

# Color Palette for tiles (from 0 to 8192)
COLORS = {
    0: "#4a5568", 2: "#e8f8f8", 4: "#a8e0f0", 8: "#5cd0e8",
    16: "#00c8e8", 32: "#00b8d8", 64: "#1a6898", 128: "#185888",
    256: "#144878", 512: "#103868", 1024: "#0c2850", 2048: "#082040",
    4096: "#061830", 8192: "#041028"
}

# Core Game State
grid = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

score = 0
best_score = 0
prev_grid = None
prev_score = 0
game_over = False
won_message_shown = False

# --- Movement Logic ---

def pack4(a, b, c, d):
    """
    Shifts and merges 4 numbers in a single row/column.
    Returns the new values, the number of successful moves, 
    and the points earned from merges.
    """
    moves = 0
    points = 0
    
    # 1. Shift non-zero values to the left
    # This ensures tiles move as far as possible before merging
    for _ in range(2):
        if c == 0 and d != 0:
            c, d = d, 0
            moves += 1
        if b == 0 and c != 0:
            b, c = c, 0
            moves += 1
        if a == 0 and b != 0:
            a, b = b, 0
            moves += 1
            
    # 2. Merge identical adjacent tiles
    if a == b and a != 0:
        a = a * 2
        points += a
        b, c, d = c, d, 0
        moves += 1
    if b == c and b != 0:
        b = b * 2
        points += b
        c, d = d, 0
        moves += 1
    if c == d and c != 0:
        c = c * 2
        points += c
        d = 0
        moves += 1
        
    return a, b, c, d, moves, points

def move_left():
    """Moves all tiles to the left and returns True if anything changed."""
    global grid, score
    changed = False
    for i in range(4):
        a, b, c, d, m, p = pack4(grid[i][0], grid[i][1], grid[i][2], grid[i][3])
        grid[i][0], grid[i][1], grid[i][2], grid[i][3] = a, b, c, d
        score += p
        if m > 0:
            changed = True
    return changed

def move_right():
    """Moves all tiles to the right and returns True if anything changed."""
    global grid, score
    changed = False
    for i in range(4):
        a, b, c, d, m, p = pack4(grid[i][3], grid[i][2], grid[i][1], grid[i][0])
        grid[i][3], grid[i][2], grid[i][1], grid[i][0] = a, b, c, d
        score += p
        if m > 0:
            changed = True
    return changed

def move_up():
    """Moves all tiles upwards and returns True if anything changed."""
    global grid, score
    changed = False
    for j in range(4):
        a, b, c, d, m, p = pack4(grid[0][j], grid[1][j], grid[2][j], grid[3][j])
        grid[0][j], grid[1][j], grid[2][j], grid[3][j] = a, b, c, d
        score += p
        if m > 0:
            changed = True
    return changed

def move_down():
    """Moves all tiles downwards and returns True if anything changed."""
    global grid, score
    changed = False
    for j in range(4):
        a, b, c, d, m, p = pack4(grid[3][j], grid[2][j], grid[1][j], grid[0][j])
        grid[3][j], grid[2][j], grid[1][j], grid[0][j] = a, b, c, d
        score += p
        if m > 0:
            changed = True
    return changed

def add_new_tile():
    """Spawns a new tile (2 or 4) in a random empty cell."""
    global grid
    empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
    
    if empty_cells:
        i, j = random.choice(empty_cells)
        # Probability: 80% for a '2', 20% for a '4'
        grid[i][j] = 2 if random.random() < 0.8 else 4

def is_game_over():
    """Checks if the player is unable to make any more moves."""
    # Check for empty cells
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                return False
    
    # Check for horizontal matches
    for i in range(4):
        for j in range(3):
            if grid[i][j] == grid[i][j+1]:
                return False
                
    # Check for vertical matches
    for j in range(4):
        for i in range(3):
            if grid[i][j] == grid[i+1][j]:
                return False
                
    return True

def has_2048():
    """Checks if the winning 2048 tile has been reached."""
    for row in grid:
        if any(val >= 2048 for val in row):
            return True
    return False

# --- UI Controls ---

def restart_game():
    """Resets the game state to its initial parameters."""
    global grid, score, game_over, won_message_shown, prev_grid, prev_score
    grid = [[0]*4 for _ in range(4)]
    score = 0
    prev_grid = None
    prev_score = 0
    game_over = False
    won_message_shown = False
    status_label.config(text="")
    add_new_tile()
    add_new_tile()
    update_ui()

def undo():
    """Reverts the game state to the previous move."""
    global grid, score, prev_grid, prev_score, game_over
    if prev_grid is not None:
        grid = [row[:] for row in prev_grid]
        score = prev_score
        prev_grid = None # Allow only one step of undo for simplicity
        game_over = False
        status_label.config(text="")
        update_ui()

# --- UI Creation ---

root = tk.Tk()
root.title("2048 Puzzle Game")
root.configure(bg="#1a202c", padx=20, pady=20)
root.resizable(False, False)

# Header Section (Score and High Score)
header = tk.Frame(root, bg="#1a202c")
header.pack(fill="x", pady=(0, 20))

score_label = tk.Label(header, text="Score: 0", fg="white", bg="#1a202c", font=("Arial", 16, "bold"))
score_label.pack(side="left", padx=10)

best_label = tk.Label(header, text="Best: 0", fg="#fbbf24", bg="#1a202c", font=("Arial", 16, "bold"))
best_label.pack(side="left", padx=10)

# Status Label (Win/Loss feedback)
status_label = tk.Label(root, text="", fg="white", bg="#1a202c", font=("Arial", 14, "bold"))
status_label.pack(pady=(0, 10))

# Control Buttons (Undo and Restart)
btn_frame = tk.Frame(header, bg="#1a202c")
btn_frame.pack(side="right")

tk.Button(btn_frame, text="Undo", bg="#6366f1", fg="white",
          font=("Arial", 11, "bold"), relief="flat", padx=15, pady=5,
          activebackground="#4f46e5", cursor="hand2",
          command=undo).pack(side="left", padx=5)

tk.Button(btn_frame, text="Restart", bg="#22c55e", fg="white",
          font=("Arial", 11, "bold"), relief="flat", padx=15, pady=5,
          activebackground="#16a34a", cursor="hand2",
          command=restart_game).pack(side="left", padx=5)

# Game Grid Frame
game_frame = tk.Frame(root, bg="#2d3748", padx=10, pady=10)
game_frame.pack()

labels = [[None]*4 for _ in range(4)]

# Initialize Tile Labels
for i in range(4):
    for j in range(4):
        labels[i][j] = tk.Label(game_frame, text="", width=4, height=2,
                                bg=COLORS[0], font=("Arial", 22, "bold"),
                                fg="white")
        labels[i][j].grid(row=i, column=j, padx=6, pady=6)

def update_ui():
    """Updates the labels on the grid and current score counts."""
    global best_score
    if score > best_score:
        best_score = score
        
    score_label.config(text="Score: " + str(score))
    best_label.config(text="Best: " + str(best_score))
    
    for i in range(4):
        for j in range(4):
            value = grid[i][j]
            if value == 0:
                labels[i][j].config(text="", bg=COLORS[0])
            else:
                text_color = "black" if value <= 4 else "white"
                labels[i][j].config(text=str(value), bg=COLORS[value], fg=text_color)

def handle_keypress(event):
    """Event handler for keyboard input (arrows and WASD)."""
    global game_over, won_message_shown, prev_grid, prev_score
    
    if game_over:
        return
        
    key = event.keysym
    moved = False
    
    # Pre-move snapshot for Undo
    temp_grid = [row[:] for row in grid]
    temp_score = score
    
    had_win_before = has_2048()

    if key in ["Up", "w", "W"]:
        moved = move_up()
    elif key in ["Down", "s", "S"]:
        moved = move_down()
    elif key in ["Left", "a", "A", "q", "Q"]:
        moved = move_left()
    elif key in ["Right", "d", "D"]:
        moved = move_right()
        
    if moved:
        # Commit snapshot for Undo
        prev_grid = temp_grid
        prev_score = temp_score
        
        add_new_tile()
        update_ui()
        
        # Check Win state
        if not won_message_shown and not had_win_before and has_2048():
            status_label.config(text="Congratulations! You've reached 2048!", fg="#22c55e")
            won_message_shown = True
            
        # Check Game Over state
        if is_game_over():
            game_over = True
            status_label.config(text="Game Over! No more moves possible.", fg="#ef4444")

# Keyboard binding
root.bind('<Key>', handle_keypress)

# Initial setup
add_new_tile()
add_new_tile()
update_ui()

root.mainloop()
