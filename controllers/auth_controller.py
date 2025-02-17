#import sys
#import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Agrega la carpeta raíz


from database.db_config import conectar_bd

def registrar_usuario(username, email, password_hash):
    """Registra un nuevo usuario en la base de datos."""
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (username, email, password_hash))
            conn.commit()
            print("✅ Usuario registrado correctamente.")
        except Exception as e:
            print(f"❌ Error al registrar usuario: {e}")
        finally:
            cursor.close()
            conn.close()

def iniciar_sesion(username, password_hash):
    """Verifica si un usuario existe y devuelve su información."""
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
        cursor.execute(query, (username, password_hash))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            print(f"✅ Bienvenida, {user['username']}!")
            return user
        else:
            print("❌ Usuario o contraseña incorrectos.")
            return None
