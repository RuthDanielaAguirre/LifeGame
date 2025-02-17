#import sys
#import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'controllers')))
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Agrega la carpeta raíz

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from controllers.auth_controller import iniciar_sesion
from ui.game_window import GameWindow
#from ui.SignUpWindow import SignUpWindow

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("LifeGame - Login")
        self.root.geometry("700x500")

        self.background_image = Image.open("assets/login1.png")
        self.background_image = self.background_image.resize((700, 500))  # Redimensionamos la imagen al tamaño de la ventana
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        framet = tk.Frame(self.root, bg="black", bd=4)
        framet.pack(side="top", fill="x")

        labelt = tk.Label(framet, text="Bienvenido a LifeGame", font=("Helvetica", 16), fg="white", bg="black")
        labelt.pack(side="top", anchor="w",  pady = 5)

        frameLog = tk.Frame(self.root, bg="black")
        frameLog.pack(side="left")

        tk.Label(frameLog, text="Usuario:",font=("Helvetica", 12), fg="white", bg="black").pack()
        self.entry_usuario = tk.Entry(frameLog)
        self.entry_usuario.pack()

        tk.Label(frameLog, text="Contraseña:",font=("Helvetica", 12), fg="white", bg="black").pack()
        self.entry_contraseña = tk.Entry(frameLog, show="*")
        self.entry_contraseña.pack()

        tk.Button(frameLog, text="Iniciar sesión", command=self.login).pack()
        tk.Button(frameLog, text="Registrarse", command=self.abrir_registro).pack()

    def login(self):
        username = self.entry_usuario.get()
        password = self.entry_contraseña.get()

        user = iniciar_sesion(username, password)
        if user:
            messagebox.showinfo("Bienvenida", f"¡Bienvenida {user['username']}!")
            self.root.destroy()  # Cierra la ventana de login
            root_juego = tk.Tk()
            GameWindow(root_juego, user['id'])  # Abre la ventana del juego
            root_juego.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def abrir_registro(self):
        self.root.destroy()
        root_signup = tk.Tk()
        SignUpWindow(root_signup)
        root_signup.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
