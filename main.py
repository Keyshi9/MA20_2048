# 2048 - Jeu en Python/Tkinter
# Auteur : Selle Sow | Date : 10/02/2026

import tkinter as tk

# Colors (2 to 8192)
COULEURS = {
    0: "#4a5568", 2: "#e8f8f8", 4: "#a8e0f0", 8: "#5cd0e8",
    16: "#00c8e8", 32: "#00b8d8", 64: "#1a6898", 128: "#185888",
    256: "#144878", 512: "#103868", 1024: "#0c2850", 2048: "#082040",
    4096: "#061830", 8192: "#041028"
}

# Test Grid
grid = [
    [0, 0, 0, 2],
    [0, 0, 2, 2],
    [2, 0, 2, 2],
    [2, 2, 2, 2]
]

score = 0

# Functions for Movement

def pack4(a, b, c, d):

    moves = 0
    
    # 1. Pushing non-zero values to the left (3 passes to be sure)
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

# UI Creation

window = tk.Tk()
window.title("2048 - Step 4 Draft")
window.configure(bg="black")

score_label = tk.Label(window, text="Score : 0", fg="white", bg="black", font=("Arial", 14))
score_label.pack(side="top", anchor="w", padx=30, pady=10)

frame = tk.Frame(window, bg="#3a4555", padx=8, pady=8)
frame.pack(padx=20, pady=10)

labels = [
    [None, None, None, None],
    [None, None, None, None],
    [None, None, None, None],
    [None, None, None, None]
]

for i in range(4):
    for j in range(4):
        labels[i][j] = tk.Label(frame, text="", width=4, height=2,
                                bg=COULEURS[0], font=("Arial", 16, "bold"))
        labels[i][j].grid(row=i, column=j, padx=4, pady=4)

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
    key = event.keysym
    moved = False
    
    if key in ["Up", "w", "W"]:
        moved = move_up()
    elif key in ["Down", "s", "S"]:
        moved = move_down()
    elif key in ["Left", "a", "A", "q", "Q"]:
        moved = move_left()
    elif key in ["Right", "d", "D"]:
        moved = move_right()
        
    if moved:
        update_ui()

# Binding keyboard event
window.bind('<Key>', key_pressed)

# Initial Display
update_ui()
window.mainloop()
