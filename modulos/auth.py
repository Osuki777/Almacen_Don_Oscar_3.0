# © 2025-2026 Oscar Salvador Fernandez, Buenos Aires, Argentina.
# Todos los derechos reservados. Ver LICENSE y LEGAL.md.
# modulos/auth.py
"""
Aquí manejo todo lo relacionado a la autenticación.

La función principal es `login`, pero también tengo las herramientas
para "hashear" las contraseñas. Esto es clave para la seguridad: nunca
guardo la contraseña real en la base de datos, sino una versión
encriptada (hash) que es imposible de revertir.

Glosario de abreviaturas:
- auth: Authentication (Autenticación)
- usr: Usuario
- pwd: Contraseña
- hash: Resultado de una función criptográfica de hash
"""
import hashlib
import modulos.ui as ui
import config

# 'Salt' es un texto secreto que le agrego a la contraseña antes de
# hashearla. Es una capa extra de seguridad para que, incluso si dos
# usuarios tienen la misma contraseña, sus hashes sean diferentes.
_SALT = b"don_oscar_salt_secreto"

def hash_password(pwd):
    """Aplico un hash SHA-256 a una contraseña usando el salt."""
    hasher = hashlib.sha256()
    hasher.update(_SALT + pwd.encode('utf-8'))
    return hasher.hexdigest()

def _verificar_password(pwd_plano, hash_almacenado):
    """
    Verifico si una contraseña que ingresa el usuario coincide con la que
    tengo guardada en la base de datos.
    """
    return hash_password(pwd_plano) == hash_almacenado

def login(conn):
    """
    Gestiono el proceso completo de inicio de sesión.
    
    Pido usuario y contraseña, y le doy al usuario 3 intentos. Si falla,
    devuelvo None y el programa se cierra. Si tiene éxito, devuelvo un
    diccionario con todos los datos del usuario logueado.
    """
    intentos = 0
    max_intentos = 3

    while intentos < max_intentos:
        ui.limpiar_pantalla()
        ui.imprimir_titulo("Inicio de Sesión")
        
        username = input(ui.Colores.INPUT + "Usuario: ").strip()
        password = input(ui.Colores.INPUT + "Contraseña: ").strip()

        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash, nombre_completo, rol, is_activo FROM usuarios WHERE username = ?", (username,))
        usr_data_tupla = cursor.fetchone()

        if usr_data_tupla:
            columnas = [desc[0] for desc in cursor.description]
            usr = dict(zip(columnas, usr_data_tupla))
            
            if not usr['is_activo']:
                ui.imprimir_error(f"El usuario '{username}' está inactivo. Contacte al administrador.")
                ui.presione_enter()
                return None

            login_exitoso = False
            # Caso especial: Primer login del admin con la contraseña inicial.
            if usr['rol'] == 'admin' and usr['password_hash'] == config.ADMIN_PASSWORD_INICIAL:
                if password == config.ADMIN_PASSWORD_INICIAL:
                    ui.imprimir_advertencia("Primer inicio de sesión detectado. Asegurando la cuenta del administrador...")
                    nuevo_hash = hash_password(password)
                    cursor.execute("UPDATE usuarios SET password_hash = ? WHERE id = ?", (nuevo_hash, usr['id']))
                    conn.commit()
                    login_exitoso = True
            else:
                # Caso normal: Verifico contra el hash que ya está en la DB.
                if _verificar_password(password, usr['password_hash']):
                    login_exitoso = True

            if login_exitoso:
                ui.imprimir_exito(f"¡Bienvenido, {usr['nombre_completo']}!")
                ui.presione_enter()
                return usr
        
        intentos += 1
        ui.imprimir_error(f"Usuario o contraseña incorrectos. Intentos restantes: {max_intentos - intentos}")
        ui.presione_enter()

    ui.imprimir_error("Demasiados intentos fallidos. El programa se cerrará.")
    ui.presione_enter()
    return None