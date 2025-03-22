import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database.db_queries import guardar_progreso, obtener_personaje_usuario, obtener_personajes_disponibles
import os


try:
    from ui.game_window import GameWindow
except ModuleNotFoundError as e:
    print(f"⚠️ Error al importar GameWindow: {e}")

# autenticación
try:
    from controllers.auth_controller import iniciar_sesion
except ModuleNotFoundError as e:
    print(f"⚠️ Error al importar iniciar_sesion: {e}")


class LoginWindow:
    def __init__(self, root):
        print("🟣 Constructor LoginWindow activo")
        self.root = root
        self.root.title("LifeGame - Login")
        self.root.geometry("700x500")

        # Fondo con imagen
        ruta_base = os.path.dirname(os.path.abspath(__file__))  # Carpeta ui/
        ruta_imagen = os.path.join(ruta_base, '..', 'assets', 'login1.png')
        ruta_imagen = os.path.abspath(ruta_imagen)

        self.background_image = Image.open("assets/login1.png")
        self.background_image = self.background_image.resize((700, 500))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Área de login
        frameLog = tk.Frame(self.root, bg="black")
        frameLog.pack(side="left", padx=20, pady=20)

        tk.Label(frameLog, text="Usuario:", font=("Helvetica", 12), fg="white", bg="black").pack()
        self.entry_usuario = tk.Entry(frameLog)
        self.entry_usuario.pack()

        tk.Label(frameLog, text="Contraseña:", font=("Helvetica", 12), fg="white", bg="black").pack()
        self.entry_contraseña = tk.Entry(frameLog, show="*")
        self.entry_contraseña.pack()

        tk.Button(frameLog, text="Iniciar sesión", command=self.login).pack()
        tk.Button(frameLog, text="Registrarse", command=self.abrir_registro).pack()

    def login(self):
        """Verifica el usuario y carga su progreso o lo envía a la selección de personaje."""
        username = self.entry_usuario.get()
        password = self.entry_contraseña.get()

        user = iniciar_sesion(username, password)
        if user:
            messagebox.showinfo("Bienvenida", f"¡Bienvenida {user['username']}!")
            self.root.destroy()  # Cierra la ventana de login

            # obtener el personaje del usuario
            personaje = obtener_personaje_usuario(user["id"])

            if personaje:
                root_juego = tk.Tk()
                GameWindow(root_juego, user["id"])
                root_juego.mainloop()
            else:
                root_seleccion = tk.Tk()
                SeleccionPersonajeWindow(root_seleccion, user["id"])
                root_seleccion.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def abrir_registro(self):
        from ui.SignUpWindow import SignUpWindow
        self.root.destroy()
        root_signup = tk.Tk()
        SignUpWindow(root_signup)
        root_signup.mainloop()

class SeleccionPersonajeWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Selecciona tu Personaje")
        self.root.geometry("800x600")

        self.personajes = obtener_personajes_disponibles()

        if not self.personajes:
            messagebox.showerror("Error", "No hay personajes disponibles.")
            self.root.destroy()
            return

        tk.Label(root, text="Elige tu personaje:", font=("Helvetica", 14)).pack()

        self.frame_personajes = tk.Frame(root)
        self.frame_personajes.pack()

        self.imagenes = []  # Almacena imágenes para evitar garbage collection

        for personaje in self.personajes:
            img = Image.open(personaje["image_path"])
            img = img.resize((150, 150))
            img = ImageTk.PhotoImage(img)

            self.imagenes.append(img)

            btn = tk.Button(self.frame_personajes, image=img, command=lambda p=personaje: self.seleccionar_personaje(p))
            btn.pack(side=tk.LEFT, padx=10, pady=10)

    def seleccionar_personaje(self, personaje):
        """Permite seleccionar un personaje y guarda el progreso del usuario."""
        guardar_progreso(self.user_id, personaje["id"], 100, 100, None, None)

        messagebox.showinfo("Seleccionado", f"Has elegido a {personaje['name']}.")
        self.root.destroy()

        # ersonaje elegido
        root_juego = tk.Tk()
        GameWindow(root_juego, self.user_id)
        root_juego.mainloop()



if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
