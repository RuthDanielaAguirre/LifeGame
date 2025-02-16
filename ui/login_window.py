import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import iniciar_sesion
from ui.game_window import GameWindow
from ui.signup_window import SignUpWindow

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("LifeGame - Login")

        tk.Label(root, text="Usuario:").pack()
        self.entry_usuario = tk.Entry(root)
        self.entry_usuario.pack()

        tk.Label(root, text="Contraseña:").pack()
        self.entry_contraseña = tk.Entry(root, show="*")
        self.entry_contraseña.pack()

        tk.Button(root, text="Iniciar sesión", command=self.login).pack()
        tk.Button(root, text="Registrarse", command=self.abrir_registro).pack()

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
