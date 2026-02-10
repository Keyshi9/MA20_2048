
# 2048 - Jeu en Python/Tkinter
# Auteur : Selle Sow | Date : 10/02/2026

import tkinter as tk

# -- Couleurs des tuiles (2 à 8192) --
COULEURS = {
    0: "#4a5568", 2: "#e8f8f8", 4: "#a8e0f0", 8: "#5cd0e8",
    16: "#00c8e8", 32: "#00b8d8", 64: "#1a6898", 128: "#185888",
    256: "#144878", 512: "#103868", 1024: "#0c2850", 2048: "#082040",
    4096: "#061830", 8192: "#041028"
}

# -- Jeu complet (toutes les valeurs de 2 à 8192) --
grille = [
    [0, 0, 0, 2], [4, 8, 16, 32],
    [64, 128, 256, 512], [1024, 2048, 4096, 8192]
]

score = 152

# -- Création de la fenêtre --
fen = tk.Tk()
fen.title("2048")
fen.configure(bg="black")

lbl_score = tk.Label(fen, text="", fg="white", bg="black", font=("Arial", 14))
lbl_score.pack(side="top", anchor="w", padx=30, pady=10)

tk.Button(fen, text="Restart", bg="#22c55e", fg="white",
          font=("Arial", 11, "bold"), relief="flat").place(x=230, y=10)

cadre = tk.Frame(fen, bg="#3a4555", padx=8, pady=8)
cadre.pack(padx=20, pady=10)

# -- Création des labels (une seule fois) --
labels = [[None]*4 for _ in range(4)]
for i in range(4):
    for j in range(4):
        labels[i][j] = tk.Label(cadre, text="", width=4, height=2,
                                bg=COULEURS[0], font=("Arial", 16, "bold"))
        labels[i][j].grid(row=i, column=j, padx=4, pady=4)

# -- Fonction d'affichage (met à jour sans recréer) --
def afficher():
    lbl_score.config(text=f"Score : {score}")
    for i in range(4):
        for j in range(4):
            v = grille[i][j]
            labels[i][j].config(
                text=str(v) if v else "",
                bg=COULEURS.get(v, "#041028"),
                fg="black" if v <= 2 else "white"
            )

afficher()
fen.mainloop()
