# © 2025-2026 Oscar Salvador Fernandez, Buenos Aires, Argentina.
# Todos los derechos reservados. Ver LICENSE y LEGAL.md.
# modulos/clientes.py
"""
Módulo para la gestión de la base de clientes.

Sigue una estructura muy similar a la de productos, con funciones para
ver, agregar y gestionar clientes, aplicando las reglas de formateo
y validación correspondientes.
"""
import modulos.ui as ui, modulos.database as db

def _agregar_cliente_interactivo(conn):
    """Un asistente para agregar un nuevo cliente con formateo automático."""
    ui.imprimir_titulo("Agregar Nuevo Cliente")
    nombre = ui.formatear_titulo_inteligente(ui.obtener_input_validado("Nombre: ", str))
    apellido = ui.formatear_titulo_inteligente(ui.obtener_input_validado("Apellido: ", str))
    nombre_completo = f"{nombre} {apellido}"
    dni_val = [(lambda x: x.isdigit() and len(x) in [7, 8], "Debe ser un número de 7 u 8 dígitos.")]
    dni_sin_formato = ui.obtener_input_validado("DNI (sin puntos): ", str, dni_val)
    dni_formateado = ui.formatear_dni(dni_sin_formato)
    tel_val = [(lambda x: x.isdigit() and len(x) == 10, "Debe ser un número de 10 dígitos (ej: 1122334455).")]
    telefono = ui.obtener_input_validado("Teléfono (10 dígitos, sin 0 ni 15): ", str, tel_val)
    email_val = [(lambda x: "@" in x and "." in x.split('@')[1], "Formato de email no válido.")]
    email = ui.obtener_input_validado("Email: ", str, email_val).lower()
    nuevo_cli = {'nombre': nombre_completo, 'dni': dni_formateado, 'telefono': telefono, 'email': email}
    ui.imprimir_advertencia("¿Desea agregar este cliente? (S/N)")
    if ui.obtener_opcion() == 'S':
        db.agregar_cliente(conn, nuevo_cli)
        ui.imprimir_exito("Cliente agregado.")
    else:
        ui.imprimir_info("Operación cancelada.")
    ui.presione_enter()

def _editar_cliente_interactivo(conn, cli):
    """Un menú personalizado para editar un cliente con formateo y validación."""
    item_temporal = cli.copy()
    while True:
        ui.limpiar_pantalla()
        ui.mostrar_detalle_item(f"Editando Cliente: {item_temporal['nombre']}", item_temporal)
        opciones_edicion = {'1': ("Nombre y Apellido", 'nombre'), '2': ("DNI", 'dni'), '3': ("Teléfono", 'telefono'), '4': ("Email", 'email')}
        print("\n" + ui.Colores.HINT + "Seleccione el campo que desea editar:")
        for k, (desc, _) in opciones_edicion.items(): print(f"  [{k}] - {desc}")
        print(f"  [G] - Guardar cambios\n  [C] - Cancelar edición")
        op = ui.obtener_opcion()
        if op == 'C': ui.imprimir_info("Edición cancelada."); break
        if op == 'G':
            db.actualizar_cliente(conn, item_temporal['id'], item_temporal)
            ui.imprimir_exito("Los cambios han sido guardados."); break
        if op in opciones_edicion:
            desc_campo, clave_a_editar = opciones_edicion[op]
            try:
                if clave_a_editar == 'nombre':
                    nombre_nuevo = ui.formatear_titulo_inteligente(ui.obtener_input_validado("Nuevo Nombre: ", str))
                    apellido_nuevo = ui.formatear_titulo_inteligente(ui.obtener_input_validado("Nuevo Apellido: ", str))
                    item_temporal['nombre'] = f"{nombre_nuevo} {apellido_nuevo}"
                elif clave_a_editar == 'dni':
                    dni_val = [(lambda x: x.isdigit() and len(x) in [7, 8], "Debe ser un número de 7 u 8 dígitos.")]
                    dni_nuevo = ui.obtener_input_validado("Nuevo DNI (sin puntos): ", str, dni_val)
                    item_temporal['dni'] = ui.formatear_dni(dni_nuevo)
                elif clave_a_editar == 'telefono':
                    tel_val = [(lambda x: x.isdigit() and len(x) == 10, "Debe ser un número de 10 dígitos.")]
                    item_temporal['telefono'] = ui.obtener_input_validado("Nuevo Teléfono (10 dígitos): ", str, tel_val)
                elif clave_a_editar == 'email':
                    email_val = [(lambda x: "@" in x and "." in x.split('@')[1], "Formato de email no válido.")]
                    item_temporal['email'] = ui.obtener_input_validado("Nuevo Email: ", str, email_val).lower()
            except Exception:
                ui.presione_enter()

def _eliminar_cliente_interactivo(conn, cli):
    """Pide confirmación y realiza un 'soft-delete' de un cliente."""
    ui.imprimir_advertencia(f"¿Desactivar a '{cli['nombre']}'? El historial se mantendrá. (S/N)")
    if ui.obtener_opcion() == 'S':
        if db.soft_delete_cliente_por_id(conn, cli['id']):
            ui.imprimir_exito("Cliente desactivado."); return True
        else:
            ui.imprimir_error("No se pudo desactivar. No se puede desactivar al 'Consumidor Final'.")
    return False

def _menu_acciones_cliente(conn, cli, usr_logueado):
    """
    Muestra el menú de acciones para un cliente ya seleccionado.
    
    Esta función la reutilizo para evitar duplicar código, sin importar
    si al cliente lo encontré por ID o por DNI.
    """
    while True:
        ui.limpiar_pantalla()
        ui.mostrar_detalle_item(f"Gestionando Cliente: {cli['nombre']}", cli)
        opciones = {'1': "Editar Cliente", '0': "Volver"}
        if usr_logueado['rol'] == 'admin': opciones['2'] = "Desactivar Cliente"
        ui.mostrar_menu("Acciones para este Cliente", opciones)
        op = ui.obtener_opcion()
        if op == '1':
            _editar_cliente_interactivo(conn, cli)
            cli = db.buscar_cliente_por_id(conn, cli['id'])
        elif op == '2' and usr_logueado['rol'] == 'admin':
            if _eliminar_cliente_interactivo(conn, cli): break
        elif op == '0': break

def _gestionar_cliente_por_id(conn, usr_logueado):
    """Pide un ID, busca al cliente y lo pasa al menú de acciones."""
    cli_id = ui.mostrar_paginado(conn, "Seleccionar Cliente para Gestionar", db.contar_total_clientes, db.obtener_pagina_clientes)
    if cli_id is None: ui.imprimir_info("Selección cancelada."); ui.presione_enter(); return
    cli = db.buscar_cliente_por_id(conn, cli_id)
    if cli: _menu_acciones_cliente(conn, cli, usr_logueado)
    else: ui.imprimir_error("El ID seleccionado no es válido."), ui.presione_enter()

def _gestionar_cliente_por_dni(conn, usr_logueado):
    """Pide un DNI, busca al cliente y lo pasa al menú de acciones."""
    dni = ui.obtener_input_validado("Ingrese el DNI del cliente a buscar (sin puntos): ", str)
    cli = db.buscar_cliente_por_dni(conn, dni)
    if cli: _menu_acciones_cliente(conn, cli, usr_logueado)
    else: ui.imprimir_error("DNI de cliente no encontrado."), ui.presione_enter()

def menu_gestion_clientes(conn, usr_logueado):
    """El menú principal para todo lo relacionado con clientes."""
    while True:
        opciones_menu = {'1': "Ver listado de clientes", '2': "Agregar nuevo cliente", '3': "Gestionar un cliente por ID", '4': "Gestionar un cliente por DNI", '0': "Volver al menú principal"}
        ui.mostrar_menu("Gestión de Clientes", opciones_menu)
        op = ui.obtener_opcion()
        if op == '1': ui.mostrar_paginado(conn, "Listado de Clientes", db.contar_total_clientes, db.obtener_pagina_clientes)
        elif op == '2': _agregar_cliente_interactivo(conn)
        elif op == '3': _gestionar_cliente_por_id(conn, usr_logueado)
        elif op == '4': _gestionar_cliente_por_dni(conn, usr_logueado)
        elif op == '0': break
        else: ui.imprimir_error("Opción no válida."), ui.presione_enter()