from database.db_config import conectar_bd

def probar_conexion():
    """Verifica si la conexión a la base de datos funciona y muestra las tablas existentes."""
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tablas = cursor.fetchall()
        print("✅ Conexión exitosa a la base de datos")
        print("📂 Tablas en la base de datos:")
        for tabla in tablas:
            print(f"- {tabla[0]}")
        cursor.close()
        conn.close()
    else:
        print("❌ Error de conexión a la base de datos.")

if __name__ == "__main__":
    probar_conexion()
