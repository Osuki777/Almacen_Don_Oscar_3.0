# © 2025-2026 Oscar Salvador Fernandez, Buenos Aires, Argentina.
# Todos los derechos reservados. Ver LICENSE y LEGAL.md.
# modulos/productos.py
"""
Este módulo contiene toda la lógica de negocio para los productos.

Aquí defino los menús, los flujos para agregar, editar, ver y eliminar
productos, llamando a las funciones de `database.py` para los datos y a
`ui.py` para mostrar las cosas en pantalla.
"""
import modulos.ui as ui, modulos.database as db

def _agregar_producto_interactivo(conn):
    """
    Un asistente guiado para que el usuario agregue un nuevo producto.
    
    Lo diseñé para que sea un formulario simple y lineal, donde las
    validaciones y el formateo de datos se hacen automáticamente.
    """
    ui.imprimir_titulo("Agregar Nuevo Producto")
    nuevo_prod = {}
    
    ui.imprimir_info("El nombre debe ser descriptivo, incluyendo peso o volumen si aplica.")
    nuevo_prod['nombre'] = ui.formatear_titulo_inteligente(ui.obtener_input_validado("Nombre del producto: ", str))
    nuevo_prod['marca'] = ui.formatear_titulo_inteligente(ui.obtener_input_validado("Marca: ", str))
    
    descripcion_input = ui.obtener_input_validado("Descripción (Enter para omitir): ", str, permitir_vacio=True)
    nuevo_prod['descripcion'] = descripcion_input.capitalize() if descripcion_input else ""

    nuevo_prod['stock'] = ui.obtener_input_validado("Cantidad de unidades a ingresar al stock: ", int, [(lambda x: x >= 0, "El stock no puede ser negativo.")])
    nuevo_prod['costo'] = ui.obtener_input_validado("Costo de compra por unidad/paquete ($): ", float, [(lambda x: x > 0, "El costo debe ser positivo.")])
    
    margen_input = ui.obtener_input_validado("Margen de ganancia individual (%) (Enter para usar el global): ", float, [(lambda x: x > 0, "El margen debe ser positivo.")], permitir_vacio=True)
    nuevo_prod['margen_ganancia_individual'] = margen_input / 100 if margen_input is not None else None
    nuevo_prod['unidad_medida'] = 'u'

    ui.imprimir_advertencia("¿Desea agregar este producto? (S/N)")
    if ui.obtener_opcion() == 'S':
        db.agregar_producto(conn, nuevo_prod)
        ui.imprimir_exito("Producto agregado correctamente.")
    else:
        ui.imprimir_info("Operación cancelada.")
    ui.presione_enter()

def _ver_listado_productos(conn):
    """
    Muestro una tabla formateada de todos los productos.
    
    Le pregunto al usuario cómo quiere ordenar la lista (por nombre o ID)
    y después genero una tabla prolija con los datos más importantes.
    """
    ui.limpiar_pantalla()
    ui.imprimir_titulo("Listado Completo de Productos")
    
    op_orden = ui.obtener_input_validado("Ordenar por: [1] Nombre (A-Z)  [2] ID (Ascendente): ", str, [(lambda x: x in ['1', '2'], "Opción no válida.")])
    ordenar_por = 'nombre' if op_orden == '1' else 'id'

    productos = db.obtener_pagina_productos(conn, 1, 1000, ordenar_por=ordenar_por)
    
    if not productos:
        print("\nNo hay productos para mostrar."); ui.presione_enter(); return

    print("\n" + f"{'ID':<5}{'Producto':<40}{'Marca':<20}{'Stock':<10}{'Precio Venta':>15}")
    print("-" * 90)
    
    for prod in productos:
        config = db.obtener_configuracion(conn)
        margen_global = float(config.get('ganancia_global', 0.3))
        margen_ind = prod.get('margen_ganancia_individual')
        precio_venta = prod['costo'] * (1 + (margen_ind if margen_ind is not None else margen_global))
        stock_str = f"{int(prod['stock'])} u"
        
        print(f"{prod['id']:<5}{prod['nombre']:<40}{prod['marca']:<20}{stock_str:<10}{ui.formatear_moneda(precio_venta):>15}")
    
    ui.presione_enter()

def _editar_producto_interactivo(conn, prod):
    """
    Abre un menú para editar un producto específico, aplicando formateo.
    """
    item_temporal = prod.copy()
    if item_temporal.get('margen_ganancia_individual') is not None:
        item_temporal['margen_ganancia_individual'] *= 100

    while True:
        ui.limpiar_pantalla()
        ui.mostrar_detalle_item(f"Editando: {item_temporal['nombre']}", item_temporal)
        
        opciones_edicion = {
            '1': ("Nombre del producto", 'nombre'), '2': ("Marca", 'marca'),
            '3': ("Descripción", 'descripcion'), '4': ("Costo", 'costo'),
            '5': ("Stock (unidades)", 'stock'), '6': ("Margen de ganancia individual (%)", 'margen_ganancia_individual')
        }
        
        print("\n" + ui.Colores.HINT + "Seleccione el campo que desea editar:")
        for k, (desc, _) in opciones_edicion.items(): print(f"  [{k}] - {desc}")
        print(f"  [G] - Guardar cambios\n  [C] - Cancelar edición")

        op = ui.obtener_opcion()

        if op == 'C': ui.imprimir_info("Edición cancelada."); break
        if op == 'G':
            if item_temporal.get('margen_ganancia_individual') is not None:
                item_temporal['margen_ganancia_individual'] /= 100
            db.actualizar_producto(conn, item_temporal['id'], item_temporal)
            ui.imprimir_exito("Los cambios han sido guardados."); break
        
        if op in opciones_edicion:
            desc_campo, clave_a_editar = opciones_edicion[op]
            nuevo_valor_str = ui.obtener_input_validado(f"\nNuevo valor para '{desc_campo}': ", str)
            try:
                if clave_a_editar in ['nombre', 'marca']:
                    item_temporal[clave_a_editar] = ui.formatear_titulo_inteligente(nuevo_valor_str)
                elif clave_a_editar == 'descripcion':
                    item_temporal[clave_a_editar] = nuevo_valor_str.capitalize()
                elif clave_a_editar == 'costo':
                    item_temporal[clave_a_editar] = float(nuevo_valor_str)
                elif clave_a_editar == 'stock':
                    item_temporal[clave_a_editar] = int(nuevo_valor_str)
                elif clave_a_editar == 'margen_ganancia_individual':
                    item_temporal[clave_a_editar] = float(nuevo_valor_str)
            except (ValueError, TypeError):
                ui.imprimir_error(f"Valor inválido para '{desc_campo}'."); ui.presione_enter()

def _eliminar_producto_interactivo(conn, prod):
    """Pide confirmación y elimina un producto (solo para admin)."""
    ui.imprimir_advertencia(f"¿Está seguro de que desea eliminar '{prod['nombre']}'? Esta acción es irreversible. (S/N)")
    if ui.obtener_opcion() == 'S':
        if db.eliminar_producto_por_id(conn, prod['id']):
            ui.imprimir_exito("Producto eliminado correctamente."); return True
        else:
            ui.imprimir_error("No se pudo eliminar. Puede que esté asociado a una venta existente.")
    return False

def _seleccionar_y_gestionar_producto(conn, usr_logueado):
    """
    Muestra la lista paginada para que el usuario elija un producto a gestionar.
    
    Esta función mejora la experiencia de usuario, porque en vez de pedir un ID
    a ciegas, primero muestra la lista para que encuentre el que busca.
    """
    ui.imprimir_info("Seleccione un producto de la lista ingresando su ID.")
    prod_id = ui.mostrar_paginado(conn, "Seleccionar Producto para Gestionar", db.contar_total_productos, db.obtener_pagina_productos)
    if prod_id is None:
        ui.imprimir_info("Selección cancelada."); ui.presione_enter(); return

    prod = db.buscar_producto_por_id(conn, prod_id)
    if not prod:
        ui.imprimir_error("El ID seleccionado no es válido."); ui.presione_enter(); return

    while True:
        ui.limpiar_pantalla()
        ui.mostrar_detalle_item(f"Gestionando Producto: {prod['nombre']}", prod)
        opciones = {'1': "Editar Producto", '0': "Volver"}
        if usr_logueado['rol'] == 'admin':
            opciones['2'] = "Eliminar Producto"
        ui.mostrar_menu("Acciones para este Producto", opciones)
        op = ui.obtener_opcion()
        if op == '1':
            _editar_producto_interactivo(conn, prod)
            prod = db.buscar_producto_por_id(conn, prod['id'])
        elif op == '2' and usr_logueado['rol'] == 'admin':
            if _eliminar_producto_interactivo(conn, prod): break
        elif op == '0':
            break

def menu_gestion_productos(conn, usr_logueado):
    """El menú principal para todo lo relacionado con productos."""
    while True:
        opciones_menu = {
            '1': "Ver listado de productos", '2': "Agregar nuevo producto",
            '3': "Gestionar un producto por ID", '0': "Volver al menú principal"
        }
        ui.mostrar_menu("Gestión de Productos", opciones_menu)
        op = ui.obtener_opcion()
        if op == '1': _ver_listado_productos(conn)
        elif op == '2': _agregar_producto_interactivo(conn)
        elif op == '3': _seleccionar_y_gestionar_producto(conn, usr_logueado)
        elif op == '0': break
        else: ui.imprimir_error("Opción no válida."), ui.presione_enter()