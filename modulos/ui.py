# modulos/ui.py
"""
Módulo de Interfaz de Usuario (UI).

Centraliza todas las funciones responsables de la interacción visual con
el usuario. Esto incluye la impresión de menús, el manejo de colores,
la obtención de entradas validadas y el formateo de datos para su
visualización.
"""
import os, sys, math
try:
    import colorama
except ImportError:
    print("❌ Error: El paquete 'colorama' no está instalado.")
    print("   Por favor, instálelo ejecutando el comando: pip install colorama")
    sys.exit(1)

colorama.init(autoreset=True)

class Colores:
    """Centraliza los códigos de color de la consola para un uso consistente."""
    RESET = colorama.Style.RESET_ALL
    ROJO = colorama.Fore.RED
    AMARILLO = colorama.Fore.YELLOW
    VERDE = colorama.Fore.GREEN
    TITULO = colorama.Fore.CYAN + colorama.Style.BRIGHT
    INPUT = colorama.Fore.YELLOW
    HINT = colorama.Fore.LIGHTBLACK_EX

def limpiar_pantalla():
    """Limpia la pantalla de la terminal de forma compatible con múltiples OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def presione_enter(mensaje="Presione Enter para continuar..."):
    """Pausa la ejecución del programa hasta que el usuario presiona Enter."""
    print(Colores.HINT + f"\n{mensaje}")
    input()

def imprimir_titulo(texto):
    """Imprime un título de sección con un estilo visual uniforme."""
    print(Colores.TITULO + f"\n--- {texto.upper()} ---")

def imprimir_error(texto):
    """Muestra un mensaje de error estandarizado."""
    print(Colores.ROJO + f"❌ Error: {texto}")

def imprimir_advertencia(texto):
    """Muestra un mensaje de advertencia estandarizado."""
    print(Colores.AMARILLO + f"⚠️ Advertencia: {texto}")

def imprimir_exito(texto):
    """Muestra un mensaje de éxito estandarizado."""
    print(Colores.VERDE + f"✅ Éxito: {texto}")

def imprimir_info(texto):
    """Muestra un mensaje informativo estandarizado."""
    print(Colores.HINT + f"ℹ️ {texto}")

def mostrar_banner():
    """Muestra el banner ASCII personalizado del programa."""
    banner_ascii = r"""
╔══════════════════════════════════════════╗
║░░░█▀▀░█░░░░░█▀█░█░░░█▄█░█▀█░█▀▀░█▀▀░█▀█░░║
║░░░█▀▀░█░░░░░█▀█░█░░░█░█░█▀█░█░░░█▀▀░█░█░░║
║░░░▀▀▀░▀▀▀░░░▀░▀░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░░║
║░░░░░░░░░░░░░░░█▀▄░█▀▀░░░░░░░░░░░░░░░░░░░░║
║░░░░░░░░░░░░░░░█░█░█▀▀░░░░░░░░░░░░░░░░░░░░║
║░░░░░░░░░░░░░░░▀▀░░▀▀▀░░░░░░░░░░░░░░░░░░░░║
║░░░░░█▀▄░█▀█░█▀█░░░█▀█░█▀▀░█▀▀░█▀█░█▀▄░░░░║
║░░░░░█░█░█░█░█░█░░░█░█░▀▀█░█░░░█▀█░█▀▄░░░░║
║░░░░░▀▀░░▀▀▀░▀░▀░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀░▀░░░░║
╚══════════════════════════════════════════╝
    """
    print(Colores.TITULO + banner_ascii)

def obtener_opcion() -> str:
    """Solicita al usuario que ingrese una opción de menú y la retorna."""
    return input(Colores.INPUT + "\nSeleccione una opción: ").strip().upper()

def mostrar_menu(titulo: str, opciones: dict, pie_de_pagina: str = ""):
    """Muestra un menú de opciones con un formato estándar."""
    limpiar_pantalla()
    imprimir_titulo(titulo)
    print()
    for op, desc in opciones.items():
        print(f"  [{op}] - {desc}")
    print("\n" + Colores.HINT + ("-" * 40))
    if pie_de_pagina:
        print(Colores.HINT + pie_de_pagina)

def mostrar_ayuda():
    """Muestra la ayuda del programa de forma paginada y visualmente atractiva."""
    C_CMD, C_SEC, C_RST = Colores.AMARILLO, Colores.VERDE, Colores.RESET
    
    limpiar_pantalla()
    mostrar_banner()
    imprimir_titulo("Ayuda: Navegación General (Pág 1/2)")
    print(f"""
El sistema se navega principalmente con números y algunas teclas clave.
- {C_CMD}[Número]{C_RST}: Selecciona una opción del menú.
- {C_CMD}[0]{C_RST}:      Generalmente significa 'Volver' o 'Salir'.
- {C_CMD}[Enter]{C_RST}:  Confirma una entrada o la omite si es opcional.

En las {C_SEC}listas paginadas{C_RST} (productos, clientes, etc.), usa estas teclas:
- {C_CMD}[A]{C_RST}: Página Anterior | {C_CMD}[D]{C_RST}: Página Siguiente.
- {C_CMD}[ID]{C_RST}: Ingresa el ID para Seleccionar o gestionar un ítem.
- {C_CMD}[X]{C_RST}: Salir de la lista y volver.
""")
    presione_enter("[Enter] para ver la siguiente página...")

    limpiar_pantalla()
    mostrar_banner()
    imprimir_titulo("Ayuda: Descripción de Secciones (Pág 2/2)")
    print(f"""
{C_SEC}--- Secciones Principales ---{C_RST}
- {C_CMD}[1] Gestión de Ventas:{C_RST} Realiza ventas y cancela transacciones.
- {C_CMD}[2] Gestión de Productos:{C_RST} Administra tu inventario.
- {C_CMD}[3] Gestión de Clientes:{C_RST} Administra tu base de clientes.
- {C_CMD}[8] Panel de Administración:{C_RST} (Solo para 'admin') Centro de control.
- {C_CMD}[9] Ayuda:{C_RST} Muestra esta pantalla.
""")
    presione_enter("[Enter] para volver al menú principal...")

def formatear_titulo_inteligente(texto: str) -> str:
    """
    Capitaliza un texto en formato de título inteligente.
    
    Mantiene conectores y artículos comunes en minúscula, a menos que sean
    la primera palabra, para un formato de datos más limpio y profesional.
    """
    if not texto: return ""
    palabras_minusculas = ['de', 'la', 'el', 'los', 'las', 'y', 'e', 'o', 'u', 'a', 'en', 'con', 'por', 'para']
    palabras = texto.lower().split()
    palabras_formateadas = [palabras[0].capitalize()]
    for palabra in palabras[1:]:
        if palabra in palabras_minusculas: palabras_formateadas.append(palabra)
        else: palabras_formateadas.append(palabra.capitalize())
    return " ".join(palabras_formateadas)

def formatear_dni(dni_sin_puntos: str) -> str:
    """Recibe un string de DNI numérico y le agrega los separadores de miles."""
    if not dni_sin_puntos or not dni_sin_puntos.isdigit(): return dni_sin_puntos
    dni_reverso = dni_sin_puntos[::-1]
    partes = [dni_reverso[i:i+3] for i in range(0, len(dni_reverso), 3)]
    return ".".join(partes)[::-1]

def formatear_moneda(valor: float) -> str:
    """Convierte un número en un string con formato de moneda argentina."""
    try:
        return f"${valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "$ --.--"

def obtener_input_validado(prompt: str, tipo_dato: type, validaciones: list = None, permitir_vacio: bool = False) -> any:
    """
    Solicita y valida una entrada del usuario de forma robusta.
    
    Esta función centraliza la lógica para pedir datos, asegurando que el
    usuario no pueda ingresar datos de tipo incorrecto o que no cumplan
    con las validaciones específicas, previniendo errores en el resto del programa.
    """
    while True:
        entrada_str = input(Colores.INPUT + prompt).strip()
        if permitir_vacio and not entrada_str: return None
        if not permitir_vacio and not entrada_str:
            imprimir_error("La entrada no puede estar vacía."); continue
        try:
            valor_casteado = tipo_dato(entrada_str)
            if validaciones:
                for val_func, msg_err in validaciones:
                    if not val_func(valor_casteado):
                        imprimir_error(msg_err); raise ValueError()
            return valor_casteado
        except (ValueError, TypeError):
            imprimir_error(f"Valor inválido. Se esperaba un dato de tipo '{tipo_dato.__name__}'.")

def mostrar_detalle_item(titulo: str, item: dict):
    """Muestra los detalles de un ítem (producto, cliente) en formato de ficha."""
    imprimir_titulo(titulo)
    for clave, valor in item.items():
        nombre_campo = clave.replace("_", " ").capitalize()
        print(f"  {nombre_campo:<30}: {valor}")

def menu_editar_item(conn, item: dict, campos_editables: dict, func_actualizar_db) -> bool:
    """
    Muestra un menú genérico para editar los campos de un ítem.
    
    Es un componente reutilizable, aunque fue personalizado en algunas secciones
    para manejar casos especiales como el formateo de datos.
    """
    item_temporal = item.copy()
    while True:
        limpiar_pantalla()
        mostrar_detalle_item(f"Editando: {item['nombre']}", item_temporal)
        print("\n" + Colores.HINT + "Seleccione el campo que desea editar:")
        opciones_edicion = {}
        i = 1
        for clave, (desc, _, _) in campos_editables.items():
            opciones_edicion[str(i)] = (clave, desc)
            print(f"  [{i}] - {desc}")
            i += 1
        print(f"  [G] - Guardar cambios\n  [C] - Cancelar edición")
        op = obtener_opcion()
        if op == 'C': return False
        if op == 'G':
            func_actualizar_db(conn, item_temporal['id'], item_temporal)
            imprimir_exito("Los cambios han sido guardados."); return True
        if op in opciones_edicion:
            clave_a_editar, desc_campo = opciones_edicion[op]
            _, tipo_dato, validaciones = campos_editables[clave_a_editar]
            nuevo_valor = input(f"\nIngrese el nuevo valor para '{desc_campo}': ").strip()
            try:
                valor_casteado = tipo_dato(nuevo_valor)
                if validaciones:
                    for val_func, msg_err in validaciones:
                        if not val_func(valor_casteado):
                            imprimir_error(msg_err); raise ValueError()
                item_temporal[clave_a_editar] = valor_casteado
            except ValueError:
                imprimir_error(f"Valor inválido para '{desc_campo}'."); presione_enter()

def mostrar_paginado(conn, titulo: str, func_contar_total, func_obtener_pagina) -> int | None:
    """
    Muestra una lista simple de forma paginada y devuelve el ID seleccionado.
    """
    pagina_actual = 1
    items_por_pagina = 10
    while True:
        limpiar_pantalla()
        imprimir_titulo(titulo)
        total_items = func_contar_total(conn)
        if total_items == 0:
            print("\nNo hay ítems para mostrar."); presione_enter(); return None
        total_paginas = math.ceil(total_items / items_por_pagina)
        items_pagina = func_obtener_pagina(conn, pagina_actual, items_por_pagina)
        for item in items_pagina:
            id_item = item.get('id', 'N/A')
            nombre_item = item.get('nombre', 'N/A')
            print(f"  ID: {id_item:<4} | {nombre_item}")
        pie_de_pagina = f"Pág: {pagina_actual}/{total_paginas} | A: Ant | D: Sig | ID: Sel. | X: Salir/Cancelar"
        print("\n" + Colores.HINT + ("-" * 40) + "\n" + Colores.HINT + pie_de_pagina)
        op = obtener_opcion()
        if op == 'A' and pagina_actual > 1: pagina_actual -= 1
        elif op == 'D' and pagina_actual < total_paginas: pagina_actual += 1
        elif op == 'X': return None
        elif op.isdigit(): return int(op)

def mostrar_paginado_ficha(conn, func_contar_total, func_obtener_pagina, titulo=""):
    """
    Muestra una lista en formato de "ficha" y devuelve un ID seleccionado.
    
    A diferencia del paginado simple, este es más visual y lo usamos para
    el historial de ventas.
    """
    pagina_actual = 1
    items_por_pagina = 3
    while True:
        limpiar_pantalla()
        if titulo: imprimir_titulo(titulo)
        total_items = func_contar_total(conn)
        if total_items == 0:
            print("\nNo hay ítems para mostrar."); presione_enter(); return None
        total_paginas = math.ceil(total_items / items_por_pagina)
        items_pagina = func_obtener_pagina(conn, pagina_actual, items_por_pagina)
        print()
        for item in items_pagina:
            print("-" * 40)
            for clave, valor in item.items():
                if clave != 'nombre':
                    nombre_campo = clave.replace("_", " ").capitalize()
                    if clave == 'total': valor = formatear_moneda(valor)
                    print(f"  {nombre_campo:<10}: {valor}")
            print("-" * 40)
        pie_de_pagina = f"Pág: {pagina_actual}/{total_paginas} | A: Ant | D: Sig | ID: Ver Detalle | X: Salir"
        print(Colores.HINT + pie_de_pagina)
        op = obtener_opcion()
        if op == 'A' and pagina_actual > 1: pagina_actual -= 1
        elif op == 'D' and pagina_actual < total_paginas: pagina_actual += 1
        elif op == 'X': return None
        elif op.isdigit(): return int(op)