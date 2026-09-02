# © 2025-2026 Oscar Salvador Fernandez, Buenos Aires, Argentina.
# Todos los derechos reservados. Ver LICENSE y LEGAL.md.
# main.py
"""
Punto de entrada principal y orquestador de la aplicación.

Se encarga de inicializar los módulos, manejar el ciclo de vida
(login -> menú -> salida) y cerrar los recursos de forma ordenada.
No contiene lógica de negocio.
"""
import sys
sys.path.append(sys.path[0])

import config
import modulos.database as db, modulos.ui as ui, modulos.auth as auth
import modulos.productos as prods, modulos.clientes as clis, modulos.ventas as vtas
import modulos.admin_panel as admin

def menu_principal(conn, usr_logueado):
    """
    Muestra el menú principal y gestiona la navegación del usuario.

    Este es el bucle principal de la aplicación después de un inicio de sesión
    exitoso. Delega las acciones a los módulos correspondientes según la
    opción seleccionada por el usuario.
    """
    while True:
        ui.limpiar_pantalla()
        ui.mostrar_banner()
        
        print(ui.Colores.TITULO + "\n--- MENÚ PRINCIPAL ---")
        print()
        
        opciones_menu = {
            '1': "Gestión de Ventas y Caja", '2': "Gestión de Productos",
            '3': "Gestión de Clientes"
        }
        if usr_logueado['rol'] == 'admin':
            opciones_menu['8'] = "Panel de Administración"
        opciones_menu['9'] = "Ayuda"
        opciones_menu['0'] = "Cerrar Sesión"

        for op, desc in opciones_menu.items():
            print(f"  [{op}] - {desc}")
        
        print("\n" + ui.Colores.HINT + ("-" * 40))
        pie_menu = f"Usuario: {usr_logueado['username']} ({usr_logueado['rol']}) | '0' para cerrar sesión"
        print(ui.Colores.HINT + pie_menu)
        
        op = ui.obtener_opcion()

        if op == '1': vtas.menu_caja_y_ventas(conn, usr_logueado)
        elif op == '2': prods.menu_gestion_productos(conn, usr_logueado)
        elif op == '3': clis.menu_gestion_clientes(conn, usr_logueado)
        elif op == '8' and usr_logueado['rol'] == 'admin':
            admin.menu_admin(conn, usr_logueado)
        elif op == '9':
            ui.mostrar_ayuda()
        elif op == '0':
            ui.imprimir_advertencia("¿Cerrar sesión? (S/N)")
            if ui.obtener_opcion() == 'S': break
        else:
            ui.imprimir_error("Opción no válida."), ui.presione_enter()

def main():
    """
    Ejecuta el ciclo de vida completo de la aplicación.
    """
    conn = db.inicializar_db()
    usr_logueado = auth.login(conn)
    if usr_logueado:
        menu_principal(conn, usr_logueado)
    conn.close()
    ui.limpiar_pantalla()
    ui.imprimir_exito(f"Gracias por usar {config.NOMBRE_PROGRAMA}.")

if __name__ == "__main__":
    # Este bloque estándar de Python asegura que la función `main()`
    # solo se ejecute cuando el script es invocado directamente.
    main()
