# modulos/admin_panel.py
"""
Este es el centro de control del administrador.

Desde aquí, el admin puede gestionar a los otros usuarios (cajeros),
acceder a los informes del negocio, realizar backups y cambiar la
configuración global del sistema.
"""
import shutil, datetime
import modulos.ui as ui, modulos.database as db, modulos.auth as auth
import modulos.informes as informes, config

def _agregar_usuario_interactivo(conn):
    """Un asistente para que el admin agregue nuevos cajeros."""
    ui.limpiar_pantalla()
    ui.imprimir_titulo("Agregar Nuevo Cajero")
    username = ui.obtener_input_validado("Nuevo nombre de usuario: ", str)
    password = ui.obtener_input_validado("Contraseña inicial: ", str)
    nombre_completo = ui.formatear_titulo_inteligente(ui.obtener_input_validado("Nombre completo del empleado: ", str))
    
    usr_datos = {
        'username': username, 'password_hash': auth.hash_password(password),
        'nombre_completo': nombre_completo, 'rol': 'cajero'
    }
    if db.agregar_usuario(conn, usr_datos):
        ui.imprimir_exito(f"Usuario '{username}' creado exitosamente.")
    else:
        ui.imprimir_error(f"El nombre de usuario '{username}' ya existe.")
    ui.presione_enter()

def _gestionar_usuarios(conn):
    """Submenú para que el admin gestione las cuentas de los cajeros."""
    while True:
        ui.limpiar_pantalla()
        ui.imprimir_titulo("Gestión de Cajeros")
        usuarios = db.obtener_todos_los_usuarios(conn)
        for u in usuarios:
            if u['rol'] == 'admin': continue
            estado = ui.Colores.VERDE + "Activo" if u['is_activo'] else ui.Colores.ROJO + "Inactivo"
            print(f"ID: {u['id']:<3} | User: {u['username']:<15} | Nombre: {u['nombre_completo']:<25} | Estado: {estado}")
        
        op_gest_usr = ui.obtener_input_validado("\n[1] Agregar Cajero [2] Modificar Cajero Existente [0] Volver: ", int)
        if op_gest_usr == 1:
            _agregar_usuario_interactivo(conn)
        elif op_gest_usr == 2:
            usr_id = ui.obtener_input_validado("ID del cajero a modificar: ", int)
            cajero = db.buscar_usuario_por_id(conn, usr_id)
            if cajero and cajero['rol'] != 'admin':
                op_mod = ui.obtener_input_validado("¿Qué desea hacer? [1] Activar/Desactivar [2] Cambiar Contraseña [3] Cambiar Nombre (0 para cancelar): ", int, [(lambda x: x in [0, 1, 2, 3], "Opción no válida.")])
                if op_mod == 1:
                    nuevo_estado = ui.obtener_input_validado("Nuevo estado ([1] Activo [0] Inactivo): ", int, [(lambda x: x in [0,1], "Opción no válida.")])
                    db.actualizar_usuario(conn, usr_id, {'is_activo': nuevo_estado})
                    ui.imprimir_exito("Estado del cajero actualizado.")
                elif op_mod == 2:
                    nueva_pwd = ui.obtener_input_validado("Ingrese la nueva contraseña: ", str)
                    nuevo_hash = auth.hash_password(nueva_pwd)
                    db.actualizar_usuario(conn, usr_id, {'password_hash': nuevo_hash})
                    ui.imprimir_exito("Contraseña actualizada.")
                elif op_mod == 3:
                    nuevo_nombre = ui.formatear_titulo_inteligente(ui.obtener_input_validado("Ingrese el nuevo nombre completo: ", str))
                    db.actualizar_usuario(conn, usr_id, {'nombre_completo': nuevo_nombre})
                    ui.imprimir_exito("Nombre del cajero actualizado.")
                if op_mod != 0: ui.presione_enter()
            else:
                ui.imprimir_error("ID de cajero no encontrado o no es válido."); ui.presione_enter()
        elif op_gest_usr == 0: break

def _realizar_backup():
    """Crea una copia de seguridad de la base de datos con fecha y hora."""
    ui.imprimir_titulo("Realizar Backup")
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_backup = f"backup_{fecha_hora}.db"
    ruta_destino = f"{config.BACKUP_DIR}/{nombre_backup}"
    try:
        shutil.copy(config.DB_NAME, ruta_destino)
        ui.imprimir_exito(f"Backup creado exitosamente en: {ruta_destino}")
    except Exception as e:
        ui.imprimir_error(f"No se pudo crear el backup: {e}")
    ui.presione_enter()

def _configuracion_sistema(conn, usr_logueado):
    """Submenú para cambiar parámetros globales y los datos del propio admin."""
    admin_data = db.buscar_usuario_por_id(conn, usr_logueado['id'])
    config_actual = db.obtener_configuracion(conn)
    
    ui.limpiar_pantalla()
    ui.imprimir_titulo("Configuración del Sistema")
    
    print(f"Nombre de Admin Actual: {admin_data['nombre_completo']}")
    print(f"Ganancia Global Actual: {float(config_actual.get('ganancia_global', 0.3)) * 100:.2f}%")
    print(f"PIN de Cancelación Actual: {config_actual.get('clave_cancelacion', '****')}")

    op = ui.obtener_input_validado("\n¿Qué desea cambiar? [1] Mi Nombre/Contraseña [2] Ganancia Global [3] PIN de Cancelación (0 para volver): ", int)
    
    if op == 1:
        ui.imprimir_info("Editando datos del Administrador...")
        nuevo_nombre = ui.formatear_titulo_inteligente(ui.obtener_input_validado(f"Nuevo nombre completo (Enter para mantener '{admin_data['nombre_completo']}'): ", str, permitir_vacio=True))
        nueva_pwd = ui.obtener_input_validado("Nueva contraseña (Enter para no cambiar): ", str, permitir_vacio=True)
        datos_a_actualizar = {}
        if nuevo_nombre:
            datos_a_actualizar['nombre_completo'] = nuevo_nombre
            usr_logueado['nombre_completo'] = nuevo_nombre
        if nueva_pwd:
            datos_a_actualizar['password_hash'] = auth.hash_password(nueva_pwd)
        if datos_a_actualizar:
            db.actualizar_usuario(conn, usr_logueado['id'], datos_a_actualizar)
            ui.imprimir_exito("Datos del administrador actualizados.")
        else:
            ui.imprimir_info("No se realizaron cambios.")
    elif op == 2:
        nuevo_porc = ui.obtener_input_validado("Nuevo % de ganancia global (ej: 35): ", float, [(lambda x: x > 0, "Debe ser un número positivo.")])
        db.actualizar_configuracion(conn, 'ganancia_global', str(nuevo_porc / 100))
        ui.imprimir_exito("Porcentaje de ganancia actualizado.")
    elif op == 3:
        nuevo_pin = ui.obtener_input_validado("Nuevo PIN de cancelación (numérico): ", str)
        db.actualizar_configuracion(conn, 'clave_cancelacion', nuevo_pin)
        ui.imprimir_exito("PIN de cancelación actualizado.")
    
    if op != 0: ui.presione_enter()

def menu_admin(conn, usr_logueado):
    """El menú principal del Panel de Administración."""
    while True:
        opciones_menu = {
            '1': "Gestionar Cajeros", '2': "Informes y Métricas",
            '3': "Realizar Backup Manual", '4': "Configuración del Sistema",
            '0': "Volver al Menú Principal"
        }
        ui.mostrar_menu("Panel de Administración", opciones_menu)
        op = ui.obtener_opcion()
        if op == '1': _gestionar_usuarios(conn)
        elif op == '2': informes.menu_informes(conn)
        elif op == '3': _realizar_backup()
        elif op == '4': _configuracion_sistema(conn, usr_logueado)
        elif op == '0': break
        else: ui.imprimir_error("Opción no válida."), ui.presione_enter()