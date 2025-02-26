from database.db_queries import guardar_progreso, cargar_progreso

def guardar_estado_jugador(user_id, character_id, life, energy, last_enemy_id, last_horoscope_id):
    """Guarda el estado actual del jugador en la base de datos."""
    guardar_progreso(user_id, character_id, life, energy, last_enemy_id, last_horoscope_id)

def cargar_estado_jugador(user_id):
    """Carga el estado del jugador desde la base de datos."""
    return cargar_progreso(user_id)
