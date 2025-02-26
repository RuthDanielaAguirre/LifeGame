import random
from game_logic.progress import guardar_estado_jugador

def calcular_ataque(jugador, enemigo, accion):
    """Lógica de batalla basada en la acción del jugador."""
    mensaje = ""

    if accion == "ataque":
        daño = 10
        enemigo["life"] -= daño
        mensaje = f"{jugador['character_name']} atacó a {enemigo['name']} causando {daño} de daño."

    elif accion == "habilidad":
        if jugador["ability_effect"] == "Puede hacer dos acciones en un turno":
            daño = 15
            enemigo["life"] -= daño * 2
            mensaje = f"{jugador['character_name']} usó {jugador['ability']} y atacó dos veces ({daño * 2} de daño)!"
        else:
            daño = 15
            enemigo["life"] -= daño
            mensaje = f"{jugador['character_name']} usó {jugador['ability']} causando {daño} de daño."

    elif accion == "defender":
        mensaje = f"{jugador['character_name']} se defiende, reduciendo el daño recibido este turno."

    # Turno del enemigo
    daño_enemigo = random.randint(10, 20)
    if accion == "defender":
        daño_enemigo = max(5, daño_enemigo // 2)

    jugador["life"] -= daño_enemigo
    mensaje += f"\n{enemigo['name']} atacó a {jugador['character_name']} causando {daño_enemigo} de daño."

    return mensaje, jugador, enemigo

def guardar_y_salir(user_id, jugador, enemigo):
    """Guarda el estado actual del jugador y cierra el juego."""
    guardar_estado_jugador(user_id, jugador["id"], jugador["life"], jugador["energy"], enemigo["id"], None)
