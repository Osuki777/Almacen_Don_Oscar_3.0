# modulos/informes.py
"""
Módulo para la visualización de informes, métricas y dashboards.

Este módulo se encarga de consultar la base de datos para obtener
datos agregados (como totales de ventas o productos más vendidos) y
presentarlos de forma clara al administrador.
"""
import modulos.ui as ui, modulos.database as db

def _mostrar_dashboard(conn):
    """Muestra el dashboard principal con estadísticas clave del negocio."""
    stats = db.obtener_estadisticas_dashboard(conn)
    ui.limpiar_pantalla()
    ui.imprimir_titulo("Dashboard General")
    if stats['num_ventas'] > 0:
        print(f"\nIngresos Totales: {ui.Colores.VERDE}{ui.formatear_moneda(stats['total_vendido'])}{ui.Colores.RESET} | Ventas Realizadas: {stats['num_ventas']}")
    else:
        ui.imprimir_info("\nAún no se han registrado ventas.")
    
    ui.imprimir_titulo("Alertas de Stock Bajo (<= 5 unidades)")
    if stats['bajo_stock']:
        for nombre, stock in stats['bajo_stock']:
            print(f"  {ui.Colores.ROJO}⚠️ {nombre:<30} | Stock restante: {stock}")
    else:
        print(f"  {ui.Colores.VERDE}✅ Todo el stock está en niveles aceptables.")

    ui.imprimir_titulo("Top 5 Productos Más Vendidos")
    if stats['top_productos']:
        for nombre, cantidad in stats['top_productos']:
            print(f"  {ui.Colores.AMARILLO}⭐ {nombre:<30} | Unidades vendidas: {int(cantidad)} u")
    else:
        ui.imprimir_info("  Aún no hay datos de ventas suficientes.")
    ui.presione_enter()

def _ver_detalle_venta_completo(conn, vta_id):
    """Muestra el ticket completo y detallado de una venta específica."""
    vta = db.obtener_venta_por_id(conn, vta_id)
    if not vta:
        ui.imprimir_error("Venta no encontrada."); ui.presione_enter(); return

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
    print(f" Vendedor: {vendedor['nombre_completo'] if vendedor else 'N/A'}")
    print(f" Estado: {vta['estado']}")
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
    print(f"{'TOTAL:':>30} {ui.formatear_moneda(vta['total']):>11}")
    print("\n" + "="*42 + "\n")
    ui.presione_enter()

def _ver_historial_de_ventas(conn):
    """
    Muestra el historial de ventas paginado en un formato de 'ficha' visual.
    Desde aquí, el admin puede seleccionar una venta para ver su ticket completo.
    """
    def obtener_pagina_ventas_ficha(conn, pagina, por_pagina):
        ventas_pagina = db.obtener_pagina_ventas(conn, pagina, por_pagina)
        return ventas_pagina

    def contar_func(c): return db.contar_total_ventas(c)
    
    while True:
        ui.limpiar_pantalla()
        ui.imprimir_titulo("Historial de Ventas")
        vta_id_seleccionada = ui.mostrar_paginado_ficha(conn, contar_func, obtener_pagina_ventas_ficha)
        if vta_id_seleccionada:
            _ver_detalle_venta_completo(conn, vta_id_seleccionada)
        else:
            break

def _consultar_ventas_por_comprador(conn):
    """
    Un flujo para encontrar un cliente y luego ver todas sus compras.
    Es útil para buscar el historial de un cliente específico.
    """
    ui.imprimir_titulo("Consultar Tickets por Comprador")
    termino_busqueda = ui.obtener_input_validado("Buscar cliente por nombre, apellido o DNI (sin puntos): ", str)
    
    clientes_encontrados = db.buscar_clientes_por_termino(conn, termino_busqueda)
    if not clientes_encontrados:
        ui.imprimir_error("No se encontraron clientes."); ui.presione_enter(); return
    
    print("\nClientes encontrados:")
    for cli in clientes_encontrados: print(f"  ID: {cli['id']:<4} | {cli['nombre']:<30} | DNI: {cli['dni']}")
        
    cli_id = ui.obtener_input_validado("\nIngrese el ID del cliente a consultar: ", int)
    cliente_seleccionado = next((c for c in clientes_encontrados if c['id'] == cli_id), None)
    if not cliente_seleccionado:
        ui.imprimir_error("ID de cliente no válido."); ui.presione_enter(); return

    ventas_del_cliente = db.obtener_ventas_por_cliente_id(conn, cli_id)
    if not ventas_del_cliente:
        ui.imprimir_info(f"El cliente '{cliente_seleccionado['nombre']}' no tiene ventas registradas."); ui.presione_enter(); return
    
    contar_func = lambda c: len(ventas_del_cliente)
    obtener_func = lambda c, p, pp: ventas_del_cliente[(p-1)*pp : p*pp]
    vta_id = ui.mostrar_paginado_ficha(conn, contar_func, obtener_func, titulo=f"Ventas de {cliente_seleccionado['nombre']}")
    
    if vta_id: _ver_detalle_venta_completo(conn, vta_id)

def menu_informes(conn):
    """El menú principal para la sección de informes y métricas."""
    while True:
        opciones = {
            '1': "Ver Dashboard General", '2': "Ver Historial de Ventas Detallado",
            '3': "Consultar Tickets por Comprador", '0': "Volver al Panel de Administración"
        }
        ui.mostrar_menu("Informes y Métricas", opciones)
        op = ui.obtener_opcion()
        if op == '1': _mostrar_dashboard(conn)
        elif op == '2': _ver_historial_de_ventas(conn)
        elif op == '3': _consultar_ventas_por_comprador(conn)
        elif op == '0': break
        else: ui.imprimir_error("Opción no válida."), ui.presione_enter()