from database.db_config import conectar_bd


def ejecutar_query(query, params=None, fetch_one=False, commit=False):
    """Ejecuta una consulta SQL con manejo de errores. Puede hacer SELECT, UPDATE, INSERT o DELETE."""
    conn = conectar_bd()
    resultado = None  # Inicializar el resultado para evitar errores

    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())

            if commit:
                conn.commit()  # 🔥 Guardar cambios en la BD (para INSERT, UPDATE, DELETE)
            else:
                resultado = cursor.fetchone() if fetch_one else cursor.fetchall()

                # 🔥 Consumir cualquier resultado no leído para evitar "Unread result found"
                while cursor.nextset():
                    pass

            print(f"🛠 Debug: Query ejecutada -> {query}")
            print(f"🛠 Debug: Resultado de la query -> {resultado}")

            cursor.close()
            conn.close()
            return resultado
        except Exception as e:
            print(f"❌ Error en la query: {e}")
            cursor.close()
            conn.close()
    return None


def obtener_personajes_disponibles():
    """Obtiene todos los personajes disponibles para la selección."""
    query = """
    SELECT id, name, life, energy, ability, ability_effect, 
           weakness, weakness_effect, goal, image_path
    FROM characters
    """
    return ejecutar_query(query)

# 🔹 Obtener personaje asociado al usuario
def obtener_personaje_usuario(user_id):
    """Obtiene el personaje asignado al usuario en la tabla progress, si tiene uno."""
    query = """
    SELECT c.id, c.name, c.life, c.energy, c.ability, c.ability_effect, 
           c.weakness, c.weakness_effect, c.goal, c.image_path
    FROM characters c
    JOIN progress p ON c.id = p.character_id
    WHERE p.user_id = %s
    """
    return ejecutar_query(query, (user_id,), fetch_one=True)


# 🔹 Obtener lista de enemigos
def obtener_enemigos():
    """Obtiene la lista de enemigos con sus imágenes y habilidades."""
    query = """
    SELECT id, name, life, energy, ability, ability_effect, 
           weakness, weakness_effect, image_path 
    FROM enemies
    """
    return ejecutar_query(query)

# 🔹 Obtener un horóscopo aleatorio
def obtener_horoscopo():
    from database.db_queries import ejecutar_query

    query = """
    SELECT id, type, message, effect, image_path FROM horoscope
    ORDER BY RAND() LIMIT 1
    """
    resultado = ejecutar_query(query, fetch_one=True)

    print(f"🛠 Debug: Horóscopos obtenidos -> {resultado}")

    return resultado

# actualiza el estado del enemigo cada vez
def actualizar_estado_enemigo(enemigo):
    """Actualiza la vida del enemigo en la base de datos."""
    query = """
        UPDATE enemies SET life = %s WHERE id = %s
    """
    print(f"📡 Guardando en BD - {enemigo['name']} Vida: {enemigo['life']}")  # 🟢 Debugging

    ejecutar_query(query, (enemigo["life"], enemigo["id"]), commit=True)  # 🔥 Se agrega `commit=True`

    print(f"✅ Estado del enemigo actualizado correctamente en la base de datos.")

def resetear_vida_enemigos():
    """Restaura la vida de todos los enemigos a su valor original desde otra tabla o configuración inicial."""
    query = """
        UPDATE enemies 
        SET life = (SELECT MAX(original_life) FROM (SELECT id, life AS original_life FROM enemies) AS original WHERE original.id = enemies.id)
    """
    ejecutar_query(query, commit=True)
    print("Vida de enemigos restablecida a valores originales.")


# 🔹 Guardar progreso del usuario
def guardar_progreso(user_id, character_id, life, energy, last_enemy_id, last_horoscope_id):
    """Guarda el progreso del jugador en la base de datos. Si el jugador muere, asigna un nuevo personaje."""
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()

        # 🔹 Si el jugador ha muerto, asignar un nuevo personaje aleatorio
        if life <= 0:
            print("💀 El jugador ha sido derrotado. Asignando un nuevo personaje aleatorio...")

            query_nuevo_personaje = "SELECT id FROM characters ORDER BY RAND() LIMIT 1"
            nuevo_personaje = ejecutar_query(query_nuevo_personaje, fetch_one=True)

            if nuevo_personaje:
                character_id = nuevo_personaje["id"]
                life = 100
                energy = 100
                last_enemy_id = None
                last_horoscope_id = None
                print(f"🎭 Nuevo personaje asignado: {character_id}")
            else:
                print("❌ No se encontró un nuevo personaje. Manteniendo el anterior.")

        # 🔹 Guardar progreso
        query = """
            INSERT INTO progress (user_id, character_id, life, energy, last_enemy_id, last_horoscope_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            character_id = VALUES(character_id),
            life = VALUES(life),
            energy = VALUES(energy),
            last_enemy_id = VALUES(last_enemy_id),
            last_horoscope_id = VALUES(last_horoscope_id)
        """
        try:
            cursor.execute(query, (user_id, character_id, life, energy, last_enemy_id, last_horoscope_id))
            conn.commit()
            print(f"✅ Progreso actualizado: User {user_id}, Personaje {character_id}, Vida {life}, Energía {energy}")
        except Exception as e:
            print(f"❌ Error al guardar el progreso: {e}")
        finally:
            cursor.close()
            conn.close()




# Cargar progreso
def cargar_progreso(user_id):
    """Carga el progreso del jugador con la última información registrada. Si el personaje tiene 0 de vida, asigna uno nuevo."""
    query = """
        SELECT p.user_id, p.character_id, p.life, p.energy, 
               c.name AS character_name, c.image_path AS character_image,
               c.ability, c.ability_effect,  
               e.name AS last_enemy, e.image_path AS enemy_image,
               h.message AS last_horoscope, h.effect AS horoscope_effect, h.image_path AS horoscope_image
        FROM progress p
        JOIN characters c ON p.character_id = c.id
        LEFT JOIN enemies e ON p.last_enemy_id = e.id
        LEFT JOIN horoscope h ON p.last_horoscope_id = h.id
        WHERE p.user_id = %s
    """

    progreso = ejecutar_query(query, (user_id,), fetch_one=True)

    # Si no hay progreso registrado, asignar un personaje nuevo
    if not progreso or progreso["life"] <= 0:
        print("⚠️ No hay progreso válido o el personaje tiene 0 de vida. Asignando nuevo personaje...")
        query_nuevo_personaje = "SELECT id FROM characters ORDER BY RAND() LIMIT 1"
        nuevo_personaje = ejecutar_query(query_nuevo_personaje, fetch_one=True)

        if nuevo_personaje:
            progreso = {
                "user_id": user_id,
                "character_id": nuevo_personaje["id"],
                "life": 100,
                "energy": 100,
                "character_name": nuevo_personaje["name"],
                "character_image": nuevo_personaje["image_path"],
                "ability": nuevo_personaje["ability"],
                "ability_effect": nuevo_personaje["ability_effect"],
                "last_enemy": None,
                "enemy_image": None,
                "last_horoscope": None,
                "horoscope_effect": None,
                "horoscope_image": None
            }

            # Guardar el nuevo personaje en la base de datos
            guardar_progreso(user_id, nuevo_personaje["id"], 100, 100, None, None)

            print(f"🎭 Nuevo personaje asignado: {nuevo_personaje['name']}")

    return progreso


if __name__ == "__main__":
    print("🔍 Probando consultas de la base de datos...\n")
