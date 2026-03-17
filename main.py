# 2048 - Game in Python/Tkinter
# Author : Selle Sow | Date : 10/02/2026

import tkinter as tk
import random

# Colors (2 to 8192)
COULEURS = {
    0: "#4a5568", 2: "#e8f8f8", 4: "#a8e0f0", 8: "#5cd0e8",
    16: "#00c8e8", 32: "#00b8d8", 64: "#1a6898", 128: "#185888",
    256: "#144878", 512: "#103868", 1024: "#0c2850", 2048: "#082040",
    4096: "#061830", 8192: "#041028"
}

# Game Grid
grid = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

score = 0
game_over = False
won_message_shown = False

# Functions for Movement

def pack4(a, b, c, d):

    moves = 0
    
    # 1. Pushing non-zero values to the left
    for i in range(3):
        if a == 0 and b != 0:
            a, b = b, 0
            moves += 1
        if b == 0 and c != 0:
            b, c = c, 0
            moves += 1
        if c == 0 and d != 0:
            c, d = d, 0
            moves += 1
            
    # 2. Merging
    if a == b and a != 0:
        a = a * 2
        b, c, d = c, d, 0
        moves += 1
    if b == c and b != 0:
        b = b * 2
        c, d = d, 0
        moves += 1
    if c == d and c != 0:
        c = c * 2
        d = 0
        moves += 1
        
    return a, b, c, d, moves

def move_left():
    global grid
    changed = False
    for i in range(4):
        # Pack row values to the left
        a, b, c, d, m = pack4(grid[i][0], grid[i][1], grid[i][2], grid[i][3])
        grid[i][0], grid[i][1], grid[i][2], grid[i][3] = a, b, c, d
        if m > 0:
            changed = True
    return changed

def move_right():
    global grid
    changed = False
    for i in range(4):
        # Reverse row, pack left, then reverse back
        a, b, c, d, m = pack4(grid[i][3], grid[i][2], grid[i][1], grid[i][0])
        grid[i][3], grid[i][2], grid[i][1], grid[i][0] = a, b, c, d
        if m > 0:
            changed = True
    return changed

def move_up():
    global grid
    changed = False
    for j in range(4):
        # Pack column values upwards
        a, b, c, d, m = pack4(grid[0][j], grid[1][j], grid[2][j], grid[3][j])
        grid[0][j], grid[1][j], grid[2][j], grid[3][j] = a, b, c, d
        if m > 0:
            changed = True
    return changed

def move_down():
    global grid
    changed = False
    for j in range(4):
        # Pack column values downwards
        a, b, c, d, m = pack4(grid[3][j], grid[2][j], grid[1][j], grid[0][j])
        grid[3][j], grid[2][j], grid[1][j], grid[0][j] = a, b, c, d
        if m > 0:
            changed = True
    return changed

def add_new_tile():
    global grid
    # List all empty cells (those containing 0)
    empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
    
    if empty_cells:
        # Choose a random cell from empty ones
        i, j = random.choice(empty_cells)
        
        # Probability : 80% for a 2, 20% for a 4
        if random.random() < 0.8:
            grid[i][j] = 2
        else:
            grid[i][j] = 4

def is_game_over():
    # Check for any empty cell
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
    for i in range(4):
        for j in range(4):
            if grid[i][j] >= 2048:
                return True
    return False


# Restart Function
def restart_game():
    global grid, score, game_over, won_message_shown
    grid = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    score = 0
    game_over = False
    won_message_shown = False
    status_label.config(text="")
    add_new_tile()
    add_new_tile()
    update_ui()

# UI Creation
window = tk.Tk()
window.title("2048 - Etape 6")
window.configure(bg="black", padx=20, pady=20) # Black background with page padding
window.resizable(False, False) # Prevent window resizing

# Top Bar for Score and Restart
header_frame = tk.Frame(window, bg="black")
header_frame.pack(fill="x", pady=(0, 20))

score_label = tk.Label(header_frame, text="Score : 0", fg="white", bg="black", font=("Arial", 18, "bold"))
score_label.pack(side="left")

# Status Label (Win/Loss)
status_label = tk.Label(window, text="", fg="white", bg="black", font=("Arial", 14, "bold"))
status_label.pack(pady=(0, 10))

# Stylized Restart Button
tk.Button(header_frame, text="Restart", bg="#22c55e", fg="white",
          font=("Arial", 11, "bold"), relief="flat", padx=15, pady=5,
          activebackground="#16a34a", cursor="hand2",
          command=restart_game).pack(side="right")

# Main Game Grid Frame
frame = tk.Frame(window, bg="#3a4555", padx=10, pady=10) # Grid container with border padding
frame.pack()

labels = [
    [None, None, None, None],
    [None, None, None, None],
    [None, None, None, None],
    [None, None, None, None]
]

# Create tiles with more spacing
for i in range(4):
    for j in range(4):
        labels[i][j] = tk.Label(frame, text="", width=4, height=2,
                                bg=COULEURS[0], font=("Arial", 22, "bold"),
                                fg="white")
        labels[i][j].grid(row=i, column=j, padx=6, pady=6) # Tile spacing

def update_ui():
    score_label.config(text="Score : " + str(score))
    for i in range(4):
        for j in range(4):
            value = grid[i][j]
            
            # Simple text and background color logic
            if value == 0:
                txt = ""
                bg_color = COULEURS[0]
            else:
                txt = str(value)
                bg_color = COULEURS[value]
                
            # Text color logic
            if value <= 2:
                text_color = "black"
            else:
                text_color = "white"
                
            labels[i][j].config(
                text=txt,
                bg=bg_color,
                fg=text_color
            )

def key_pressed(event):
    global game_over, won_message_shown
    if game_over:
        return
        
    key = event.keysym
    moved = False
    
    # Check if 2048 exists before the move
    had_2048_before = has_2048()

    if key in ["Up", "w", "W"]:
        moved = move_up()
    elif key in ["Down", "s", "S"]:
        moved = move_down()
    elif key in ["Left", "a", "A", "q", "Q"]:
        moved = move_left()
    elif key in ["Right", "d", "D"]:
        moved = move_right()
        
    if moved:
        add_new_tile()
        update_ui()
        
        # Check Win Condition
        if not won_message_shown and not had_2048_before and has_2048():
            status_label.config(text="Félicitations ! Vous avez atteint 2048 !", fg="#22c55e")
            won_message_shown = True
            
        # Check Loss Condition
        if is_game_over():
            game_over = True
            status_label.config(text="Game Over ! Le tableau est plein.", fg="#ef4444")

# Binding keyboard event
window.bind('<Key>', key_pressed)

# Initial Display with 2 tiles
add_new_tile()
add_new_tile()
update_ui()
window.mainloop()
