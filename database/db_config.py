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
    "database": os.getenv("AIVEN_DATABASE", "defaultdb"),
}

def conectar_bd():
    """Establece la conexión con la base de datos MySQL (Aiven) usando las variables de entorno."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Conexión exitosa a la base de datos")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Error de conexión: {err}")
        return None

