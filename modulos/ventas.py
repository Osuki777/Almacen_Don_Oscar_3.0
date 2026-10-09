# © 2025-2026 Oscar Salvador Fernandez, Buenos Aires, Argentina.
# Todos los derechos reservados. Ver LICENSE y LEGAL.md.
# modulos/ventas.py
"""
Este módulo maneja todo el proceso de ventas y caja.

Contiene la lógica para el flujo de realizar una venta (seleccionar cliente,
armar el carrito), la cancelación de ventas (con autorización de admin) y
la impresión de tickets profesionales.
"""
import modulos.ui as ui, modulos.database as db

def _imprimir_ticket_final(conn, vta_id):
    """
    Imprime un ticket de venta con formato profesional.
    
    Busca todos los datos necesarios (venta, items, cliente, vendedor) y
    los presenta en un formato de ticket claro y bien alineado.
    """
    vta = db.obtener_venta_por_id(conn, vta_id)
    if not vta: return

    items = db.obtener_items_venta(conn, vta_id)
    cliente = db.buscar_cliente_por_id(conn, vta['cliente_id'])
    vendedor = db.buscar_usuario_por_id(conn, vta['usuario_id'])
    
    ui.limpiar_pantalla()
    print("\n" + "="*42)
    print(f"|      Almacén de Don Oscar      |")
    print("="*42)
    print(f" TICKET DE VENTA N°: {vta_id:06d}")
    print(f" Fecha: {vta['fecha']}")
    print("-" * 42)
    print(f" Cliente: {cliente['nombre'] if cliente else 'N/A'}")
    print(f" Atendido por: {vendedor['nombre_completo'] if vendedor else 'N/A'}")
    print("-" * 42)
    print(f"{'Cant.':<7} {'Descripción':<22} {'Precio':>11}")
    print("-" * 42)
    for item in items:
        prod = db.buscar_producto_por_id(conn, item['producto_id'])
        nombre_prod = prod['nombre'] if prod else "Producto Eliminado"
        cant_str = f"{item['cantidad']:.2f}kg" if prod and prod['unidad_medida'] == 'kg' else f"{int(item['cantidad'])} u"
        precio_str = ui.formatear_moneda(item['precio_unitario_venta'] * item['cantidad'])
        print(f"{cant_str:<7} {nombre_prod:<22} {precio_str:>11}")
    print("-" * 42)
    print(f"{'TOTAL A PAGAR:':>30} {ui.formatear_moneda(vta['total']):>11}")
    print("\n         ¡Gracias por su compra!         \n")

def realizar_venta(conn, usr_logueado):
    """
    Gestiona el flujo principal y rápido para realizar una venta.
    
    Este flujo está optimizado para la velocidad: no hay pausas innecesarias.
    El cajero puede agregar productos al carrito uno tras otro hasta que
    decide finalizar la compra.
    """
    ui.limpiar_pantalla()
    ui.imprimir_titulo("Iniciar Nueva Venta")
    
    cli_id = ui.mostrar_paginado(conn, "Seleccione el Cliente", db.contar_total_clientes, db.obtener_pagina_clientes)
    if cli_id is None:
        ui.imprimir_advertencia("Venta cancelada."); ui.presione_enter(); return
    
    carrito = []
    while True:
        ui.limpiar_pantalla()
        ui.imprimir_titulo("Añadir Productos al Carrito")
        if carrito:
            total_carrito = sum(p['precio_venta'] * p['qty'] for p in carrito)
            print(f"Items: {len(carrito)} | Total actual: {ui.formatear_moneda(total_carrito)}")
            print("-" * 20)
            for item in carrito: print(f"  - {item['qty']} x {item['nombre']}")
            print("-" * 20)
        
        prod_id = ui.mostrar_paginado(conn, "Seleccione un Producto", db.contar_total_productos, db.obtener_pagina_productos)
        if prod_id is None: break # El usuario presiona 'X' para finalizar

        prod = db.buscar_producto_por_id(conn, prod_id)
        if not prod or prod.get('stock', 0) <= 0:
            ui.imprimir_error("Producto no válido o sin stock."); ui.presione_enter(); continue
        
        qty = ui.obtener_input_validado(f"Cantidad para '{prod['nombre']}' (Stock: {prod.get('stock', 0)}): ", float, [(lambda x: 0 < x <= prod.get('stock', 0), "Cantidad inválida o excede el stock.")])
        
        config_db = db.obtener_configuracion(conn)
        margen_global = float(config_db.get('ganancia_global', 0.3))
        margen_individual = prod.get('margen_ganancia_individual')
        prod['precio_venta'] = round(prod['costo'] * (1 + (margen_individual if margen_individual is not None else margen_global)), 2)
        prod['qty'] = qty
        
        item_existente = next((item for item in carrito if item["id"] == prod_id), None)
        if item_existente:
            item_existente['qty'] += qty
        else:
            carrito.append(prod)
        
        ui.imprimir_exito(f"Añadido: {qty} x {prod['nombre']}")
    
    if not carrito:
        ui.imprimir_advertencia("Venta cancelada, no se añadieron productos."); ui.presione_enter(); return

    total_final = sum(p['precio_venta'] * p['qty'] for p in carrito)
    ui.limpiar_pantalla()
    ui.imprimir_titulo("Resumen de la Venta")
    for p in carrito: print(f"  - {p['qty']} x {p['nombre']} @ {ui.formatear_moneda(p['precio_venta'])} = {ui.formatear_moneda(p['precio_venta'] * p['qty'])}")
    print("-" * 30)
    print(f"TOTAL A PAGAR: {ui.formatear_moneda(total_final)}")
    
    ui.imprimir_advertencia("¿Confirmar venta? (S/N)")
    if ui.obtener_opcion() == 'S':
        vta_datos = {'cli_id': cli_id, 'usr_id': usr_logueado['id'], 'total': total_final, 'carrito': carrito}
        vta_id = db.registrar_venta(conn, vta_datos)
        if vta_id:
            ui.imprimir_exito(f"Venta #{vta_id} registrada correctamente.")
            _imprimir_ticket_final(conn, vta_id)
        else:
            ui.imprimir_error("No se pudo registrar la venta debido a un problema con la base de datos.")
    else:
        ui.imprimir_advertencia("Venta cancelada por el usuario.")
    ui.presione_enter()

def _cancelar_venta_interactivo(conn):
    """
    Gestiona la cancelación de una venta con autorización del admin.
    
    Para hacerlo más seguro y fácil, primero muestro una lista de las
    últimas 10 ventas, así el cajero puede elegir el ID correcto sin
    tener que memorizarlo.
    """
    ui.imprimir_titulo("Cancelar Venta")
    ui.imprimir_info("Mostrando las últimas 10 ventas completadas:")
    
    ultimas_ventas = db.obtener_ultimas_ventas(conn)
    if not ultimas_ventas:
        ui.imprimir_advertencia("No hay ventas recientes para cancelar."); ui.presione_enter(); return
        
    print("\n" + f"{'ID':<5} {'Fecha':<22} {'Cliente':<25} {'Total':>15}")
    print("-" * 67)
    for vta in ultimas_ventas:
        print(f"{vta[0]:<5} {vta[1]:<22} {vta[2]:<25} {ui.formatear_moneda(vta[3]):>15}")

    vta_id = ui.obtener_input_validado("\nIngrese el ID de la Venta a cancelar (0 para volver): ", int)
    if vta_id == 0: return

    vta = db.obtener_venta_por_id(conn, vta_id)
    if not vta: ui.imprimir_error("Venta no encontrada."); ui.presione_enter(); return
    if vta.get('estado') == 'Cancelada': ui.imprimir_advertencia("Esta venta ya está cancelada."); ui.presione_enter(); return

    pin_ingresado = ui.obtener_input_validado("\nIngrese PIN de administrador para autorizar: ", str)
    pin_correcto = db.obtener_pin_cancelacion(conn)

    if pin_ingresado == pin_correcto:
        items = db.obtener_items_venta(conn, vta_id)
        if db.ejecutar_cancelacion_venta(conn, vta_id, items):
            ui.imprimir_exito("Venta cancelada y stock restituido.")
    else:
        ui.imprimir_error("PIN incorrecto. Cancelación no autorizada.")
    ui.presione_enter()

def menu_caja_y_ventas(conn, usr_logueado):
    """El menú principal para las operaciones de venta y caja."""
    while True:
        opciones_menu = {
            '1': "Realizar Nueva Venta",
            '2': "Cancelar Venta (Requiere PIN)",
            '0': "Volver al Menú Principal"
        }
        ui.mostrar_menu("Gestión de Ventas y Caja", opciones_menu)
        op = ui.obtener_opcion()
        if op == '1': realizar_venta(conn, usr_logueado)
        elif op == '2': _cancelar_venta_interactivo(conn)
        elif op == '0': break
        else: ui.imprimir_error("Opción no válida."), ui.presione_enter()