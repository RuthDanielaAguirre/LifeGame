import os
import mysql.connector
from dotenv import load_dotenv

# Carga variables desde .env
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("AIVEN_HOST", "localhost"),
    "port": os.getenv("AIVEN_PORT", "3306"),
    "user": os.getenv("AIVEN_USER", "root"),
    "password": os.getenv("AIVEN_PASSWORD", ""),
    "database": os.getenv("AIVEN_DATABASE", "game"),
}

def conectar_bd():
    """Establece la conexión con la base de datos MySQL (Aiven) usando las variables de entorno."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()[0]
        print("✅ Conexión exitosa a la base de datos")
        print(f"✅ Conectado a la base de datos: {db_name}")
        print("🔍 AIVEN_DATABASE en .env:", os.getenv("AIVEN_DATABASE"))
        if db_name is None:
            print("⚠️ ADVERTENCIA: No se seleccionó ninguna base de datos.")
        cursor.close()
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Error de conexión: {err}")
        return None


if __name__ == "__main__":
    print("🔍 Probando conexión a la base de datos...\n")

    conn = conectar_bd()

    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()[0]
        print(f"✅ Conectado a la base de datos: {db_name}")
        cursor.close()
        conn.close()
    else:
        print("❌ No se pudo conectar a la base de datos.")
