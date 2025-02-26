
def aplicar_habilidad(jugador, enemigo):
    """
    Aplica la habilidad especial del personaje.
    """
    print(f"🎭 {jugador['character_name']} usa su habilidad: {jugador['ability']}!")

    if jugador["ability_effect"] == "Puede hacer dos acciones en un turno":
        print("⚡ ¡Puedes hacer otro ataque!")
        enemigo["life"] -= 15
        enemigo["life"] -= 15  # 🔹 Se ataca dos veces

    elif jugador["ability_effect"] == "Aumenta el daño un 50%":
        print("💥 Tu ataque hace más daño!")
        enemigo["life"] -= int(15 * 1.5)  # 🔹 50% más de daño

    else:
        print("❌ La habilidad no tiene efecto especial en esta versión.")
        enemigo["life"] -= 15  # 🔹 Por defecto, el ataque especial hace 15 de daño
