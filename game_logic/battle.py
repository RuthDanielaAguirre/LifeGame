
def iniciar_batalla(jugador, enemigo, horoscopo, actualizar_ui, manejar_turno):
    """Inicia la batalla."""

    # 🔹 Convertir horóscopo en diccionario
    efecto = parsear_efecto(horoscopo["effect"])

    # 🔹 Aplicar elhoróscopo
    jugador["life"] += efecto.get("vida", 0)
    jugador["energy"] += efecto.get("energia", 0)


    if efecto.get("habilidad_boost"):
        print("🌟 Tus habilidades son más efectivas hoy!")
    if efecto.get("habilidad_delay"):
        print("⏳ Tus habilidades tardan más en activarse!")

    actualizar_ui()

    manejar_turno()

def parsear_efecto(efecto_texto):
    """Convierte el texto de efecto en un diccionario con valores numéricos."""
    efecto = {}

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

    return efecto
