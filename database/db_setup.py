import mysql.connector
from database.db_config import conectar_bd

def ejecutar_script_sql():

    conn = None
    cursor = None
    try:
        # onectar sin especificar la base de datos, para poder crearla
        temp_config = conectar_bd().copy()
        temp_config.pop("database", None)  # Quitar 'database' para conectarnos solo al servidor
        conn = mysql.connector.connect(**temp_config)
        cursor = conn.cursor()

        # Crear la base de datos si no existe, y usarla
        cursor.execute("CREATE DATABASE IF NOT EXISTS game;")
        cursor.execute("USE game;")

        # Crear tablas principales

        # Tabla users
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Tabla characters
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            life INT DEFAULT 100,
            energy INT DEFAULT 100,
            ability VARCHAR(255),
            ability_effect TEXT,
            weakness VARCHAR(255),
            weakness_effect TEXT
        );
        """)

        # Tabla enemies
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS enemies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            life INT DEFAULT 100,
            energy INT DEFAULT 100,
            ability VARCHAR(255),
            ability_effect TEXT
        );
        """)

        # Tabla events
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INT AUTO_INCREMENT PRIMARY KEY,
            type ENUM('positivo','negativo','neutro') NOT NULL,
            description TEXT NOT NULL,
            effect TEXT NOT NULL
        );
        """)

        # Tabla horoscope
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS horoscope (
            id INT AUTO_INCREMENT PRIMARY KEY,
            type ENUM('positivo','negativo','neutro') NOT NULL,
            message TEXT NOT NULL,
            effect TEXT NOT NULL
        );
        """)

        # Tabla progress
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            level INT DEFAULT 1,
            enemies_defeated INT DEFAULT 0,
            items_acquired INT DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # (Opcional) Relaciones extras: character_enemies, character_events, character_horoscope, etc.
        # Ejemplos:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS character_enemies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            character_id INT,
            enemy_id INT,
            FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE,
            FOREIGN KEY (enemy_id) REFERENCES enemies(id) ON DELETE CASCADE
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS character_events (
            id INT AUTO_INCREMENT PRIMARY KEY,
            character_id INT,
            event_id INT,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS character_horoscope (
            id INT AUTO_INCREMENT PRIMARY KEY,
            character_id INT,
            horoscope_id INT,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE,
            FOREIGN KEY (horoscope_id) REFERENCES horoscope(id) ON DELETE CASCADE
        );
        """)

        # Paso 4: Poblar datos iniciales
        poblar_users(cursor)
        poblar_characters(cursor)
        poblar_enemies(cursor)
        poblar_events(cursor)
        poblar_horoscope(cursor)

        # Paso 5: Confirmar los cambios
        conn.commit()
        print("✅ Base de datos configurada y tablas creadas/pobladas correctamente.")

    except mysql.connector.Error as err:
        print(f"❌ Error en la configuración de la base de datos: {err}")
    finally:
        cursor.close()
        conn.close()

def poblar_users(cursor):
    """Insertar algunos usuarios de ejemplo."""
    users_data = [
        ("Daniela", "daniela@mail.com", "123Hash"),
        ("Ruth", "ruth@mail.com", "123Hash"),
        ("RuthD", "ruthdaniela@mail.com", "123Hash")
    ]
    query = """
        INSERT IGNORE INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
    """
    cursor.executemany(query, users_data)
    print("✅ Usuarios de ejemplo insertados (si no existían).")

def poblar_characters(cursor):
    """Insertar personajes de ejemplo."""
    characters_data = [
        ("Estudiante de Programación", 100, 90, "Depuración rápida", "Recupera 20 de energía", "Café insuficiente", "Reduce energía en 15 puntos"),
        ("Mamá de un Bebé", 120, 80, "Multitarea extrema", "Evita un evento negativo", "Falta de sueño", "Reduce energía en 10 puntos cada turno")
    ]
    query = """
        INSERT IGNORE INTO characters 
        (name, life, energy, ability, ability_effect, weakness, weakness_effect)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(query, characters_data)
    print("✅ Personajes de ejemplo insertados (si no existían).")

def poblar_enemies(cursor):
    """Insertar enemigos de ejemplo."""
    enemies_data = [
        ("Misoginia", 150, 50, "Desmoralización", "Reduce energía en 30 puntos"),
        ("Racismo", 140, 55, "Exclusión social", "Reduce vida en 25 puntos"),
        ("Ignorancia", 120, 60, "Difusión de Fake News", "Reduce la habilidad del jugador en un 50%")
    ]
    query = """
        INSERT IGNORE INTO enemies 
        (name, life, energy, ability, ability_effect)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.executemany(query, enemies_data)
    print("✅ Enemigos de ejemplo insertados (si no existían).")

def poblar_events(cursor):
    """Insertar eventos de ejemplo."""
    events_data = [
        ("positivo", "Encuentras una mentoría y ganas experiencia.", '{"energia": 20, "vida": 10}'),
        ("negativo", "Tu laptop se rompe en medio de un proyecto importante.", '{"energia": -25}')
    ]
    query = """
        INSERT IGNORE INTO events (type, description, effect)
        VALUES (%s, %s, %s)
    """
    cursor.executemany(query, events_data)
    print("✅ Eventos de ejemplo insertados (si no existían).")

def poblar_horoscope(cursor):
    """Insertar horóscopos de ejemplo."""
    horoscope_data = [
        ("positivo", "Hoy las estrellas están a tu favor, todo saldrá bien.", '{"energia": 15, "vida": 10}'),
        ("negativo", "Tiempos difíciles, pero no imposibles de superar.", '{"energia": -10}')
    ]
    query = """
        INSERT IGNORE INTO horoscope (type, message, effect)
        VALUES (%s, %s, %s)
    """
    cursor.executemany(query, horoscope_data)
    print("✅ Horóscopos de ejemplo insertados (si no existían).")

if __name__ == "__main__":
    ejecutar_script_sql()
