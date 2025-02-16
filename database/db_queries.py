from database.db_config import conectar_bd

def obtener_enemigos():
    """Obtiene la lista de enemigos de la base de datos."""
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM enemies")
        enemigos = cursor.fetchall()
        cursor.close()
        conn.close()
        return enemigos
    return []

def obtener_eventos():
    """Obtiene eventos del juego."""
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM events ORDER BY RAND() LIMIT 1")
        evento = cursor.fetchone()
        cursor.close()
        conn.close()
        return evento
    return None

def obtener_horoscopo():
    """Obtiene un horóscopo aleatorio."""
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM horoscope ORDER BY RAND() LIMIT 1")
        horoscopo = cursor.fetchone()
        cursor.close()
        conn.close()
        return horoscopo
    return None

def guardar_progreso(jugador_id, nivel, enemigos_derrotados, objetos_comprados):
    """Guarda el progreso del jugador en la base de datos."""
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO progress (user_id, nivel, enemigos_derrotados, objetos_comprados)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            nivel = VALUES(nivel), 
            enemigos_derrotados = VALUES(enemigos_derrotados), 
            objetos_comprados = VALUES(objetos_comprados)
        """
        try:
            cursor.execute(query, (jugador_id, nivel, enemigos_derrotados, objetos_comprados))
            conn.commit()
            print(f"✅ Progreso guardado para el jugador {jugador_id}.")
        except Exception as e:
            print(f"❌ Error al guardar el progreso: {e}")
        finally:
            cursor.close()
            conn.close()
