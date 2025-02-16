import mysql.connector
from database.db_config import conectar_bd

def registrar_usuario(username, email, password_hash):
    """Registra un nuevo usuario en la base de datos y muestra depuración."""
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        try:
            print("🔍 Conectado a la base de datos. Ejecutando query...")
            print(f"📝 Query: {query}")
            print(f"📩 Datos: {username}, {email}, {password_hash}")

            cursor.execute(query, (username, email, password_hash))
            conn.commit()

            print(f"✅ Usuario {username} registrado correctamente.")
        except Exception as e:
            print(f"❌ Error al registrar usuario: {e}")
        finally:
            cursor.close()
            conn.close()
            print("🔗 Conexión cerrada.")

def iniciar_sesion(username, password_hash):
    """Verifica el inicio de sesión de un usuario."""
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

def actualizar_usuario(old_username, new_username):
    """Actualiza el nombre de usuario."""
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE users SET username = %s WHERE username = %s"
        try:
            cursor.execute(query, (new_username, old_username))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"✅ Usuario actualizado: {old_username} → {new_username}")
            else:
                print("❌ No se encontró el usuario.")
        except Exception as e:
            print(f"❌ Error al actualizar usuario: {e}")
        finally:
            cursor.close()
            conn.close()

def eliminar_usuario(username):
    """Elimina un usuario de la base de datos."""
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        query = "DELETE FROM users WHERE username = %s"
        try:
            cursor.execute(query, (username,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"✅ Usuario {username} eliminado.")
            else:
                print("❌ No se encontró el usuario.")
        except Exception as e:
            print(f"❌ Error al eliminar usuario: {e}")
        finally:
            cursor.close()
            conn.close()
