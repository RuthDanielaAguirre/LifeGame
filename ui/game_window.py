import tkinter as tk
from tkinter import messagebox

class GameWindow:
    def __init__(self, root, username):
        self.root = root
        self.root.title("LifeGame - Juego")
        self.root.geometry("700x500")

        self.label = tk.Label(root, text=f"Bienvenido al juego {username}!", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.quit_button = tk.Button(root, text="Salir", command=self.salir)
        self.quit_button.pack()

    def salir(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameWindow(root, username="jane")  # Puedes cambiar el ID por prueba
    root.mainloop()