import random
from game_logic.game_logic import calcular_ataque
from database.db_queries import ejecutar_query

def calcular_ataque(jugador, enemigo, accion="ataque"):
    """Calcula el daño infligido basado en la acción y la habilidad."""
    dano = 15

    return dano


def atacar(jugador, enemigo, accion="ataque", defensa=False):
    """Función para calcular el daño del ataque y aplicarlo al enemigo."""
    dano_jugador = calcular_ataque(jugador, enemigo, accion)

    if isinstance(dano_jugador, tuple):
        dano_jugador = dano_jugador[1]

    if dano_jugador <= 0:
        print(f"⚠️ {jugador['character_name']} no hizo daño a {enemigo['name']}.")
        return

    if defensa:
        dano_jugador = max(0, dano_jugador // 2)

    enemigo["life"] -= dano_jugador

    print(f"⚔️ {jugador['character_name']} hizo {dano_jugador} de daño a {enemigo['name']}!")

    if enemigo["life"] <= 0:
        print(f"💀 {enemigo['name']} ha sido derrotado!")
        enemigo["life"] = 0  # Asegurar que no haya valores negativos

    # 🔹 enemigo en la base de datos
    actualizar_estado_enemigo(enemigo)

    return dano_jugador

def actualizar_estado_enemigo(enemigo):
    """Actualiza la vida del enemigo en la base de datos."""
    query = """
        UPDATE enemies SET life = %s WHERE id = %s
    """
    ejecutar_query(query, (enemigo["life"], enemigo["id"]), commit=True)
    # Mostrar nombre solo si está disponible
    if "name" in enemigo:
        print(f"✅ Estado del enemigo actualizado en la base de datos: {enemigo['name']} (Vida {enemigo['life']})")
    else:
        print(f"✅ Estado del enemigo actualizado en la base de datos: ID {enemigo['id']} (Vida {enemigo['life']})")

def atacar_enemigo(jugador, enemigo):

    print(f"⚔️ {enemigo['id']} contraataca!")

    dano_enemigo = random.randint(10, 20)

    if enemigo.get("ability_effect") == "Reduce energía en 30 puntos":
        jugador["energy"] = max(0, jugador["energy"] - 30)
        print(f"⚡ {enemigo['id']} drena 30 de energía a {jugador['character_name']}!")

    jugador["life"] -= dano_enemigo
    print(f"💥 {enemigo['name']} hizo {dano_enemigo} de daño a {jugador['character_name']}!")

    if jugador["life"] <= 0:
        print(f"💀 {jugador['character_name']} ha sido derrotado por {enemigo['name']}!")

