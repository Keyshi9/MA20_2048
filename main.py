import tkinter as tk

COLORS = {0:"#4a5568", 2:"#e8f8f8", 4:"#a8e0f0", 8:"#5cd0e8", 16:"#00c8e8", 32:"#00b8d8",
          64:"#1a6898", 128:"#185888", 256:"#144878", 512:"#103868", 1024:"#0c2850", 2048:"#082040", 4096:"#061830", 9192:"#041028"}

GRID = [[0,0,0,2], [4,8,16,32], [64,128,256,512], [1024,2048,4096,9192]]

root = tk.Tk()
root.title("2048")
root.configure(bg="black")

tk.Label(root, text="Score : 152", fg="white", bg="black", font=("Arial",14)).pack(side="top", anchor="w", padx=30, pady=10)
tk.Button(root, text="Restart", bg="#22c55e", fg="white", font=("Arial",11,"bold"), relief="flat").place(x=280, y=10)

f = tk.Frame(root, bg="#3a4555", padx=8, pady=8)
f.pack(padx=20, pady=10)

for i,row in enumerate(GRID):
    for j,v in enumerate(row):
        tk.Label(f, text=str(v) if v else "", width=4, height=2, bg=COLORS[v], 
                 fg="black" if v<=2 else "white", font=("Arial",16,"bold")).grid(row=i,column=j,padx=4,pady=4)

root.mainloop()
