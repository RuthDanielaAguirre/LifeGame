import json
import random
from database.db_queries import obtener_horoscopo, guardar_progreso


def aplicar_efecto_horoscopo(jugador, horoscopo):
    """Aplica los efectos del horóscopo en el jugador y lo guarda en la base de datos."""

    if not horoscopo or not horoscopo.get("message"):
        print("⚠️ No hay horóscopo en progreso. Seleccionando uno nuevo...")
        horoscopo = obtener_horoscopo()

        if not horoscopo:
            print("❌ No hay horóscopos disponibles en la base de datos.")
            return jugador

        # 🔹 Guardar el nuevo horóscopo en el progreso del jugador
        guardar_progreso(jugador["user_id"], jugador["character_id"], jugador["life"], jugador["energy"], None,
                         horoscopo["id"])

    print(f"🔮 Horóscopo recibido: {horoscopo.get('message', 'Sin mensaje')}")

    # Valida si `effect` ya es un JSON o es un texto simple
    efecto_texto = horoscopo.get("effect", "{}")
    efectos = {}

    if isinstance(efecto_texto, dict):  # Si ya es un diccionario, úsalo directamente
        efectos = efecto_texto
    else:
        try:
            # Convertir el efecto en diccionario JSON válido
            if "Ganas" in efecto_texto:
                efectos["vida"] = 10 if "vida" in efecto_texto else 0
                efectos["energia"] = 10 if "energía" in efecto_texto else 0
            elif "Pierdes" in efecto_texto:
                efectos["vida"] = -10 if "vida" in efecto_texto else 0
                efectos["energia"] = -10 if "energía" in efecto_texto else 0
            elif "habilidades tardan" in efecto_texto:
                efectos["habilidad_retrasada"] = True
        except Exception:
            print(f"❌ Error al interpretar el efecto del horóscopo: {efecto_texto}")

    # Aplicar efectos al jugador
    jugador["life"] += efectos.get("vida", 0)
    jugador["energy"] += efectos.get("energia", 0)

    print(f"🎭 Estado del jugador después del horóscopo: Vida {jugador['life']}, Energía {jugador['energy']}")

    return jugador
