import random
from database.db_queries import guardar_progreso, obtener_horoscopo


def aplicar_efecto_horoscopo(jugador, horoscopo):
    """Aplica el efecto del horóscopo al jugador."""
    print(f"🔮 Horóscopo del día: {horoscopo['message']}")
    print(f"✨ Efecto: {horoscopo['effect']}")

    if "Ganas 10 de energía" in horoscopo["effect"]:
        jugador["energy"] += 10
    elif "Ganas 10 de vida" in horoscopo["effect"]:
        jugador["life"] += 10
    elif "Pierdes 10 de energía" in horoscopo["effect"]:
        jugador["energy"] -= 10
    elif "Pierdes 10 de vida" in horoscopo["effect"]:
        jugador["life"] -= 10
    elif "Tus habilidades son un 20% más efectivas" in horoscopo["effect"]:
        jugador["habilidad_boost"] = 1.2
    elif "Tus habilidades tardan un turno más en activarse" in horoscopo["effect"]:
        jugador["habilidad_retraso"] = True


def iniciar_batalla(jugador, enemigo):
    """Sistema de combate mejorado con habilidades y horóscopo."""
    print(f"\n⚔️ ¡{jugador['name']} vs {enemigo['name']}! ⚔️")

    defensa = False
    horoscopo = obtener_horoscopo()
    aplicar_efecto_horoscopo(jugador, horoscopo)

    while jugador["life"] > 0 and enemigo["life"] > 0:
        print(f"\n{jugador['name']} ❤️{jugador['life']} | ⚡{jugador['energy']}")
        print(f"{enemigo['name']} ❤️{enemigo['life']} | ⚡{enemigo['energy']}")

        print("\n🔥 ¿Qué quieres hacer?")
        print("1️⃣ Ataque normal (10 de daño)")
        print("2️⃣ Usar habilidad especial")
        print("3️⃣ Defender (reduce daño recibido)")
        print("4️⃣ Esquivar (puede evitar todo el daño)")
        opcion = input("Elige una opción (1-4): ").strip()

        if opcion == "1":
            print(f"⚔️ {jugador['name']} ataca a {enemigo['name']}!")
            enemigo["life"] -= 10

        elif opcion == "2":
            print(f"🌟 {jugador['name']} usa su habilidad especial: {jugador['ability']}!")
            if jugador["ability_effect"] == "Puede hacer dos acciones en un turno":
                print("⚡ ¡Ataque doble!")
                enemigo["life"] -= 15
                enemigo["life"] -= 15
            elif jugador["ability_effect"] == "Duplica el daño por un turno":
                print("💥 ¡Golpe crítico!")
                enemigo["life"] -= 30
            elif jugador["ability_effect"] == "Recupera 20 de energía":
                print("☕ ¡Recuperas energía!")
                jugador["energy"] += 20
            else:
                print("❌ La habilidad no tiene efecto especial en esta versión.")
                enemigo["life"] -= 15

        elif opcion == "3":
            print(f"🛡️ {jugador['name']} se defiende! Recibe menos daño este turno.")
            defensa = True

        elif opcion == "4":
            if random.random() < 0.5:
                print(f"💨 {jugador['name']} esquivó el ataque con éxito!")
                continue
            else:
                print(f"⚠️ {jugador['name']} intentó esquivar, pero falló.")

        else:
            print("❌ Opción no válida, intenta de nuevo.")
            continue

        if enemigo["life"] <= 0:
            print(f"💀 {enemigo['name']} ha sido derrotado!")
            break

        print(f"⚔️ {enemigo['name']} contraataca!")
        dano_enemigo = random.randint(10, 20)

        if enemigo["ability_effect"] == "Reduce la energía del jugador en 30":
            jugador["energy"] -= 30
        elif enemigo["ability_effect"] == "Reduce la vida del jugador en 25":
            jugador["life"] -= 25
        elif enemigo["ability_effect"] == "Reduce la precisión de los ataques del jugador un 50%":
            if random.random() < 0.5:
                print(f"💨 {jugador['name']} falló su ataque debido a {enemigo['name']}!")
                continue
        elif enemigo["ability_effect"] == "Reduce energía en 20 por turno":
            jugador["energy"] -= 20

        if defensa:
            print("🛡️ Daño reducido gracias a la defensa!")
            dano_enemigo = max(5, dano_enemigo // 2)
            defensa = False

        jugador["life"] -= dano_enemigo
        print(f"💥 {enemigo['name']} hizo {dano_enemigo} de daño a {jugador['name']}!")

        if jugador["life"] <= 0:
            print(f"💀 {jugador['name']} ha sido derrotado por {enemigo['name']}!")
            break

    print("⚔️ Batalla finalizada.")
    guardar_progreso(jugador["user_id"], jugador["character_id"], jugador["life"], jugador["energy"], enemigo["id"],
                     horoscopo["id"])


# **🔹 Prueba Rápida**
if __name__ == "__main__":
    jugador_prueba = {
        "user_id": 1,
        "character_id": 1,
        "name": "Estudiante de Programación",
        "life": 100,
        "energy": 90,
        "ability": "Resolución de bugs",
        "ability_effect": "Recupera 20 de energía"
    }

    enemigo_prueba = {
        "id": 3,
        "name": "Ignorancia",
        "life": 120,
        "energy": 60,
        "ability": "Difusión de Fake News",
        "ability_effect": "Reduce la precisión de los ataques del jugador un 50%"
    }

    iniciar_batalla(jugador_prueba, enemigo_prueba)
