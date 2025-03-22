import tkinter as tk
import random
from tkinter import messagebox
from PIL import Image, ImageTk
from game_logic.combat import atacar_enemigo, atacar, actualizar_estado_enemigo
from game_logic.progress import cargar_progreso, guardar_progreso
from game_logic.horoscope import aplicar_efecto_horoscopo
from database.db_queries import obtener_enemigos, obtener_horoscopo, obtener_personaje_usuario, ejecutar_query
from game_logic.skills import aplicar_habilidad
from database.db_queries import resetear_vida_enemigos
from database.db_queries import obtener_personaje_por_id


class GameWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("LifeGame - Batalla")
        self.root.geometry("700x500")

        self.background_image = Image.open("assets/game_background.png")
        self.background_image = self.background_image.resize((700, 500))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Carga progreso del jugador
        self.jugador = cargar_progreso(user_id)
        if not self.jugador:
            messagebox.showerror("Error", "No se encontró progreso para este usuario.")
            self.root.destroy()
            return


        # Carga enemigo y horóscopo aleatorio
        resetear_vida_enemigos()
        self.enemigos = obtener_enemigos()
        self.enemigo = random.choice(self.enemigos)
        self.progreso = cargar_progreso(self.user_id)

        if self.progreso.get("last_horoscope"):
            self.horoscopo = {
                "id": self.progreso.get("last_horoscope_id"),
                "message": self.progreso.get("last_horoscope") or "🌙 Horóscopo no disponible.",
                "effect": self.parsear_efecto(self.progreso.get("horoscope_effect") or "")
            }
        else:
            nuevo_horoscopo = aplicar_efecto_horoscopo(self.jugador, None) or {}
            self.horoscopo = {
                "id": nuevo_horoscopo.get("id", None),
                "message": nuevo_horoscopo.get("message", "🌙 Que el viento guie tu destino."),
                "effect": nuevo_horoscopo.get("effect", {}),
                "image_path": nuevo_horoscopo.get("image_path", "assets/horoscope/neutro1.png")
            }

        mensaje = self.horoscopo.get("message", "🌌 Horóscopo desconocido")
        self.label_horoscopo = tk.Label(root, text=mensaje, font=("Helvetica", 16), bg="black", fg="yellow")
        self.label_horoscopo.pack(pady=5)

        # información del jugador
        self.label_jugador = tk.Label(root, text=f"{self.jugador['character_name']} - Vida: {self.jugador['life']}", font=("Helvetica", 14), bg="black", fg="white")
        self.label_jugador.pack(pady=10)

        # información del enemigo
        self.label_enemigo = tk.Label(root, text=f"{self.enemigo['name']} - Vida: {self.enemigo['life']}", font=("Helvetica", 14), bg="red", fg="white")
        self.label_enemigo.pack(pady=10)
        self.frame_vs = tk.Frame(root, bg="black")
        self.frame_vs.pack(pady=10)

        # Imagen jugador
        self.img_jugador = ImageTk.PhotoImage(Image.open(self.jugador["character_image"]))
        self.label_img_jugador = tk.Label(self.frame_vs, image=self.img_jugador)
        self.label_img_jugador.pack(side=tk.LEFT, padx=20)

        # Imagen nemigo
        self.img_enemigo = ImageTk.PhotoImage(Image.open(self.enemigo["image_path"]))
        self.label_img_enemigo = tk.Label(self.frame_vs, image=self.img_enemigo)
        self.label_img_enemigo.pack(side=tk.LEFT, padx=20)

        # Botón de ataque
        self.boton_ataque = tk.Button(root, text="⚔️ Atacar", command=self.ataque)
        self.boton_ataque.pack(pady=5)

        # Botón de habilidad
        self.boton_habilidad = tk.Button(root, text="🎭 Habilidad", command=self.usar_habilidad)
        self.boton_habilidad.pack(pady=5)

        # Botón de defender
        self.boton_defender = tk.Button(root, text="🛡️ Defender", command=self.defender)
        self.boton_defender.pack(pady=5)

        # Botón de guardar y salir
        self.boton_guardar = tk.Button(root, text="💾 Guardar y Salir", command=self.guardar_y_salir)
        self.boton_guardar.pack(pady=5)

    def actualizar_ui(self):
        # Actualizar vida y energía del jugador
        self.label_jugador.config(
            text=f"{self.jugador['character_name']} - Vida: {self.jugador['life']}, Energía: {self.jugador['energy']}")

        # Actualizar vida y energía del enemigo
        self.label_enemigo.config(
            text=f"{self.enemigo['name']} - Vida: {self.enemigo['life']}, Energía: {self.enemigo['energy']}")

        # Actualizar mensaje del horóscopo
        mensaje_horoscopo = self.horoscopo.get("message", "🌠 Tu destino es un misterio...")
        self.label_horoscopo.config(text=mensaje_horoscopo)

        # Refrescar la UI
        self.root.update()

    def manejar_turno(self):
        """Maneja el turno del jugador y luego el del enemigo."""

        # 🔹 Verificar si el enemigo ha sido derrotado
        if self.enemigo["life"] <= 0:
            messagebox.showinfo("Victoria", f"¡Has derrotado a {self.enemigo['name']}! 🎉")

            #  Asegurar que el enemigo derrotado tenga vida 0 en la BD
            actualizar_estado_enemigo({"id": self.enemigo["id"], "life": 0})

            #  Obtener un nuevo enemigo con vida positiva
            enemigos_disponibles = [e for e in obtener_enemigos() if e["life"] > 20]

            if not enemigos_disponibles:
                print("⚠️ Todos los enemigos han sido derrotados. Reiniciando lista de enemigos...")
                resetear_vida_enemigos()  # Restaurar todos los enemigos a su vida inicial
                enemigos_disponibles = obtener_enemigos()

            self.enemigo = random.choice(enemigos_disponibles)

            # Actualizar imagen y texto del enemigo
            nueva_imagen = ImageTk.PhotoImage(Image.open(self.enemigo["image_path"]))
            self.label_img_enemigo.config(image=nueva_imagen)
            self.label_img_enemigo.image = nueva_imagen  # <- evitar que se pierda la imagen
            self.label_enemigo.config(text=f"{self.enemigo['name']} - Vida: {self.enemigo['life']}")

            # Verificar si el horóscopo tiene un ID antes de guardarlo
            horoscopo_id = self.horoscopo.get("id", None)

            # 🔹 Guardar progreso con el nuevo enemigo
            guardar_progreso(
                self.user_id,
                self.jugador["character_id"],
                self.jugador["life"],
                self.jugador["energy"],
                self.enemigo["id"],  # Nuevo enemigo
                horoscopo_id
            )

            # Actualizar la UI con el nuevo enemigo
            self.actualizar_ui()
            return

        # 🔹 Turno del enemigo (si aún está vivo)
        if self.jugador["life"] > 0:
            atacar_enemigo(self.jugador, self.enemigo)

        # 🔹 Verificar si el jugador ha sido derrotado
        if self.jugador["life"] <= 0:
            messagebox.showerror("Derrota", "Has sido derrotada. Se te asignará un nuevo personaje. 😢")

            # Obtener nuevo personaje aleatorio
            query_nuevo_personaje = "SELECT id FROM characters ORDER BY RAND() LIMIT 1"
            nuevo_personaje = ejecutar_query(query_nuevo_personaje, fetch_one=True)

            if nuevo_personaje:
                # Asignar nuevo personaje al jugador
                self.jugador = obtener_personaje_por_id(nuevo_personaje["id"])
                self.jugador["life"] = 100  # Reiniciar vida
                self.jugador["energy"] = 100  # Reiniciar energía

                # Guardar el nuevo personaje en la base de datos
                guardar_progreso(
                    self.user_id,
                    self.jugador["id"],  # Nuevo personaje asignado
                    self.jugador["life"],
                    self.jugador["energy"],
                    None,  # No tiene enemigo anterior
                    None  # No tiene horóscopo aún
                )

            # Enviar al jugador a la selección de personaje en la UI
            self.root.destroy()
            return

        self.actualizar_ui()

    def ataque(self):
        """El jugador ataca al enemigo y actualiza la UI"""

        print(f"🔹 Antes del ataque: {self.enemigo['name']} - Vida: {self.enemigo['life']}")  # 🟢 Debugging

        # aplica daño al enemigo
        dano_jugador = atacar(self.jugador, self.enemigo)

        print(
            f"⚔️ {self.jugador['character_name']} hizo {dano_jugador} de daño a {self.enemigo['name']}!")  # 🟢 Debugging
        print(f"🔹 Después del ataque: {self.enemigo['name']} - Vida: {self.enemigo['life']}")  # 🟢 Debugging

        # Guardar el nuevo estado del enemigo en la BD
        actualizar_estado_enemigo(self.enemigo)

        self.actualizar_ui()

        # el turno enemigo después de atacar
        self.manejar_turno()
    def usar_habilidad(self):
        aplicar_habilidad(self.jugador, self.enemigo)
        self.manejar_turno()

    def defender(self):
        print(f"🛡️ {self.jugador['character_name']} se pone en defensa! Reducirá el daño del próximo ataque enemigo.")
        atacar(self.jugador, self.enemigo, defensa=True)
        self.manejar_turno()

    def guardar_y_salir(self):
        horoscopo_id = self.horoscopo.get("id", None)

        guardar_progreso(
            self.user_id,
            self.jugador["character_id"],
            self.jugador["life"],
            self.jugador["energy"],
            self.enemigo["id"],
            horoscopo_id
        )

        messagebox.showinfo("Progreso Guardado", "Tu progreso ha sido guardado. Cerrando el juego...")
        self.root.destroy()

    def actualizar_interfaz(self):
        """Actualiza los textos de vida y energía tras cada acción."""
        self.label_jugador.config(text=f"{self.jugador['character_name']} - Vida: {self.jugador['life']}")
        self.label_enemigo.config(text=f"{self.enemigo['name']} - Vida: {self.enemigo['life']}")

    def parsear_efecto(self, efecto_texto):
        """Convierte el texto del efecto del horóscopo en un diccionario de valores numéricos."""
        efecto = {}

        # Si el efecto es None o vacío, evitar errores y devolver un efecto neutro
        if not efecto_texto:
            return {"neutral": True}

        if "Ganas 10 de energía" in efecto_texto:
            efecto["energia"] = 10
        elif "Ganas 10 de vida" in efecto_texto:
            efecto["vida"] = 10
        elif "Tus habilidades son un 20% más efectivas" in efecto_texto:
            efecto["habilidad_boost"] = 0.2
        elif "Pierdes 10 de energía" in efecto_texto:
            efecto["energia"] = -10
        elif "Pierdes 10 de vida" in efecto_texto:
            efecto["vida"] = -10
        elif "Tus habilidades tardan un turno más en activarse" in efecto_texto:
            efecto["habilidad_delay"] = 1
        elif "Nada cambia" in efecto_texto:
            efecto["neutral"] = True

        return efecto  # Devuelve el diccionario con el efecto analizado

    def actualizar_horoscopo(self):
        """Actualiza el horóscopo en la interfaz con la nueva información obtenida de la base de datos."""

        nuevo_horoscopo = obtener_horoscopo()  # 🔥 Obtener un horóscopo nuevo de la base de datos

        if nuevo_horoscopo:
            self.horoscopo_label.config(text=nuevo_horoscopo["message"])
            nueva_imagen = ImageTk.PhotoImage(Image.open(nuevo_horoscopo["image_path"]))
            self.horoscopo_imagen_label.config(image=nueva_imagen)
            self.horoscopo_imagen_label.image = nueva_imagen

            print(f"✅ Interfaz actualizada con el nuevo horóscopo: {nuevo_horoscopo['message']}")
        else:
            print("❌ No se encontró un nuevo horóscopo.")

