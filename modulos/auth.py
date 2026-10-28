# © 2025-2026 Oscar Salvador Fernandez. Derechos reservados. Ver LICENSE y LEGAL.md.
"""Autenticación local con migración compatible de hashes históricos."""
import getpass
import modulos.ui as ui
from seguridad_credenciales import hash_password, verificar_password, es_password_fabrica, pedir_password, pedir_pin, leer_secreto

def _verificar_password(pwd_plano, hash_almacenado):
    return verificar_password(pwd_plano, hash_almacenado)

def login(conn):
    for intento in range(3):
        ui.limpiar_pantalla()
        ui.imprimir_titulo("Inicio de Sesión")
        username=input(ui.Colores.INPUT + "Usuario: ").strip()
        try:
            password=leer_secreto("Contraseña: ")
        except (EOFError,KeyboardInterrupt,getpass.GetPassWarning):
            ui.imprimir_advertencia("Inicio cancelado. No se abrió una sesión.")
            return None
        cursor=conn.execute("SELECT id, username, password_hash, nombre_completo, rol, is_activo FROM usuarios WHERE username = ?",(username,))
        row=cursor.fetchone()
        if row:
            usr=dict(zip([d[0] for d in cursor.description],row))
            if not usr['is_activo']:
                ui.imprimir_error("Usuario inactivo. Contacte al administrador.")
                return None
            if verificar_password(password,usr['password_hash']):
                try:
                    nuevo_hash=None; nuevo_pin=None
                    if es_password_fabrica(password):
                        ui.imprimir_advertencia("La cuenta conserva una contraseña de fábrica. Elegí una propia antes de continuar.")
                        nuevo_hash=hash_password(pedir_password())
                    elif not usr['password_hash'].startswith('pbkdf2_sha256$600000$'):
                        nuevo_hash=hash_password(password)
                    if usr['rol']=='admin':
                        pin=conn.execute("SELECT valor FROM configuracion WHERE clave='clave_cancelacion'").fetchone()
                        if pin is None or pin[0] in ('','1234'):
                            ui.imprimir_advertencia("Configurá un PIN propio antes de continuar.")
                            nuevo_pin=pedir_pin()
                    with conn:
                        if nuevo_hash:
                            conn.execute("UPDATE usuarios SET password_hash=? WHERE id=?",(nuevo_hash,usr['id']))
                            usr['password_hash']=nuevo_hash
                        if nuevo_pin:
                            conn.execute("INSERT OR REPLACE INTO configuracion(clave,valor) VALUES('clave_cancelacion',?)",(nuevo_pin,))
                except (EOFError,KeyboardInterrupt,getpass.GetPassWarning):
                    ui.imprimir_advertencia("Configuración cancelada. No se abrió una sesión ni se cambiaron las credenciales.")
                    return None
                ui.imprimir_exito(f"¡Bienvenido, {usr['nombre_completo']}!")
                ui.presione_enter()
                return usr
        ui.imprimir_error(f"Usuario o contraseña incorrectos. Intentos restantes: {2-intento}")
        ui.presione_enter()
    return None
