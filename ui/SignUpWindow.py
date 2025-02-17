import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Agrega la carpeta raíz

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from controllers.auth_controller import registrar_usuario
from ui.login_window import LoginWindow

class SignUpWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("LifeGame - Registro")
        self.root.geometry("700x500")

        self.background_image = Image.open("assets/login1.png")  # Cambia la imagen si es necesario
        self.background_image = self.background_image.resize((700, 500))  # Ajusta al tamaño de la ventana
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        tk.Label(root, text="Usuario:").pack()
        self.entry_usuario = tk.Entry(root)
        self.entry_usuario.pack()

        tk.Label(root, text="Email:").pack()
        self.entry_email = tk.Entry(root)
        self.entry_email.pack()

        tk.Label(root, text="Contraseña:").pack()
        self.entry_contraseña = tk.Entry(root, show="*")
        self.entry_contraseña.pack()

        tk.Button(root, text="Registrarse", command=self.registrarse).pack()
        tk.Button(root, text="Volver al Login", command=self.volver_al_login).pack()

    def registrarse(self):
        username = self.entry_usuario.get()
        email = self.entry_email.get()
        password = self.entry_contraseña.get()

        if username and email and password:
            registrar_usuario(username, email, password)
            messagebox.showinfo("Registro Exitoso", "¡Usuario registrado correctamente!")
            self.volver_al_login()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    def volver_al_login(self):
        self.root.destroy()
        root_login = tk.Tk()
        LoginWindow(root_login)
        root_login.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignUpWindow(root)
    root.mainloop()
