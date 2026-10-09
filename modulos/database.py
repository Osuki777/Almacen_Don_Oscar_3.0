# © 2025-2026 Oscar Salvador Fernandez, Buenos Aires, Argentina.
# Todos los derechos reservados. Ver LICENSE y LEGAL.md.
# modulos/database.py
"""
Este es el corazón de la persistencia de datos.

Todo lo que tenga que ver con hablar con la base de datos SQLite está aquí.
La idea es que el resto del programa no sepa de SQL; simplemente llama
a una función de este módulo (ej: `agregar_producto`) y este se encarga
de la lógica de la base de datos.
"""
import sqlite3, os, sys, config

def conectar_db():
    """
    Establece la conexión con el archivo de la base de datos.

    Esta es la primera función crítica. Si no puedo conectar con la base de datos,
    el programa no puede funcionar, así que directamente se cierra con un
    mensaje de error claro.
    """
    try:
        db_path = os.path.join(os.path.dirname(__file__), '..', config.DB_NAME)
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = 1;")
        return conn
    except sqlite3.OperationalError as e:
        print(f"❌ Error crítico al conectar con la base de datos: {e}")
        print("Asegúrese de que el programa tiene permisos para escribir en el directorio.")
        sys.exit(1)

def crear_schema(conn):
    """
    Crea toda la estructura de tablas y los datos iniciales.

    Esta función es el "plano" de la base de datos. Se ejecuta una
    sola vez, cuando el programa detecta que el archivo .db no existe.
    Define las tablas, sus columnas y las relaciones entre ellas.
    """
    print("ℹ️ Creando esquema de la base de datos por primera vez...")
    cursor = conn.cursor()
    schema_sql = """
    CREATE TABLE IF NOT EXISTS configuracion (clave TEXT PRIMARY KEY, valor TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, nombre_completo TEXT NOT NULL, rol TEXT NOT NULL, is_activo BOOLEAN NOT NULL DEFAULT 1);
    CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, dni TEXT UNIQUE, telefono TEXT, email TEXT, is_activo BOOLEAN NOT NULL DEFAULT 1);
    CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, marca TEXT, descripcion TEXT, unidad_medida TEXT NOT NULL DEFAULT 'u', costo REAL NOT NULL, margen_ganancia_individual REAL, stock REAL NOT NULL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS ventas (id INTEGER PRIMARY KEY AUTOINCREMENT, cliente_id INTEGER, usuario_id INTEGER, fecha DATETIME DEFAULT CURRENT_TIMESTAMP, total REAL NOT NULL, estado TEXT NOT NULL, FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE SET NULL, FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE SET NULL);
    CREATE TABLE IF NOT EXISTS ventas_detalle (id INTEGER PRIMARY KEY AUTOINCREMENT, venta_id INTEGER NOT NULL, producto_id INTEGER NOT NULL, cantidad REAL NOT NULL, precio_unitario_venta REAL NOT NULL, FOREIGN KEY (venta_id) REFERENCES ventas (id) ON DELETE CASCADE, FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE RESTRICT);
    """
    cursor.executescript(schema_sql)
    
    print("ℹ️ Insertando datos iniciales...")
    cursor.execute("INSERT OR IGNORE INTO usuarios (username, password_hash, nombre_completo, rol) VALUES (?, ?, ?, ?)", (config.ADMIN_USERNAME_INICIAL, config.ADMIN_PASSWORD_INICIAL, 'Administrador del Sistema', 'admin'))
    cursor.execute("INSERT OR IGNORE INTO clientes (id, nombre, dni) VALUES (?, ?, ?)", (1, 'Consumidor Final', '00000000'))
    cursor.execute("INSERT OR IGNORE INTO configuracion (clave, valor) VALUES (?, ?)", ('ganancia_global', str(config.PORCENTAJE_GANANCIA_GLOBAL_INICIAL)))
    cursor.execute("INSERT OR IGNORE INTO configuracion (clave, valor) VALUES (?, ?)", ('clave_cancelacion', config.CLAVE_CANCELACION_INICIAL))
    conn.commit()
    print("✅ Base de datos creada y configurada exitosamente.")

def inicializar_db():
    """
    Punto de entrada para la gestión de la DB.

    Esta es la única función que se llama desde fuera de este módulo.
    Orquesta todo: se conecta y, si es necesario, llama a `crear_schema`
    para construir la base de datos desde cero.
    """
    db_path = os.path.join(os.path.dirname(__file__), '..', config.DB_NAME)
    db_existe = os.path.exists(db_path)
    conn = conectar_db()
    if not db_existe:
        crear_schema(conn)
    else:
        print("ℹ️ Conectado a la base de datos existente.")
    return conn

# --- A partir de aquí, las funciones son las "herramientas" que usan los otros módulos ---

def contar_total_productos(conn):
    """Devuelve la cantidad total de productos en el inventario."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) FROM productos")
    return cursor.fetchone()[0]

def obtener_pagina_productos(conn, pagina, por_pagina, ordenar_por = 'nombre'):
    """
    Obtiene una 'página' de productos para mostrar en las listas.
    
    Le paso qué página quiero y cuántos productos por página. También le digo
    cómo ordenarlos ('nombre' o 'id'). Así, no traigo miles de productos a la
    memoria de una, solo los necesarios.
    """
    cursor = conn.cursor()
    offset = (pagina - 1) * por_pagina
    if ordenar_por not in ['nombre', 'id']: ordenar_por = 'nombre'
    sql = f"SELECT id, nombre, marca, costo, stock, unidad_medida, margen_ganancia_individual FROM productos ORDER BY {ordenar_por} ASC LIMIT ? OFFSET ?"
    cursor.execute(sql, (por_pagina, offset))
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    # Convierto las tuplas que me da la base de datos en una lista de diccionarios.
    # Así es más fácil trabajar con los datos después.
    lista_de_productos = []
    for fila in filas:
        producto_dic = dict(zip(columnas, fila))
        lista_de_productos.append(producto_dic)
    return lista_de_productos

def agregar_producto(conn, prod):
    """Guarda un nuevo producto en la base de datos."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, marca, descripcion, unidad_medida, costo, margen_ganancia_individual, stock) VALUES (?, ?, ?, ?, ?, ?, ?)", (prod['nombre'], prod['marca'], prod.get('descripcion'), prod['unidad_medida'], prod['costo'], prod.get('margen_ganancia_individual'), prod['stock']))
    conn.commit()

def buscar_producto_por_id(conn, prod_id):
    """Busca y devuelve un único producto a partir de su ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (prod_id,))
    fila = cursor.fetchone()
    if not fila: return None
    columnas = [desc[0] for desc in cursor.description]
    return dict(zip(columnas, fila))

def actualizar_producto(conn, prod_id, datos_actualizados):
    """
    Actualiza uno o más campos de un producto.
    
    Esta función es flexible. Construyo la consulta SQL dinámicamente
    dependiendo de los campos que me pasen en `datos_actualizados`.
    """
    set_clause = ", ".join([f"{key} = ?" for key in datos_actualizados.keys()])
    valores = list(datos_actualizados.values())
    valores.append(prod_id)
    sql = f"UPDATE productos SET {set_clause} WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, valores)
    conn.commit()

def eliminar_producto_por_id(conn, prod_id):
    """

    Elimina un producto de forma permanente.
    
    Devuelve `False` si no se puede borrar (por ejemplo, porque está
    asociado a una venta), gracias a la restricción 'ON DELETE RESTRICT'.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (prod_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        return False

def contar_total_clientes(conn, incluir_inactivos = False):
    """Cuenta el número total de clientes."""
    sql = "SELECT COUNT(id) FROM clientes"
    if not incluir_inactivos: sql += " WHERE is_activo = 1"
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchone()[0]

def obtener_pagina_clientes(conn, pagina, por_pagina):
    """Obtiene una 'página' de clientes activos de la base de datos."""
    cursor = conn.cursor()
    offset = (pagina - 1) * por_pagina
    cursor.execute("SELECT id, nombre, dni, telefono, email FROM clientes WHERE is_activo = 1 ORDER BY nombre ASC LIMIT ? OFFSET ?", (por_pagina, offset))
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    lista_de_clientes = []
    for fila in filas:
        cliente_dic = dict(zip(columnas, fila))
        lista_de_clientes.append(cliente_dic)
    return lista_de_clientes

def agregar_cliente(conn, cli):
    """Inserta un nuevo cliente en la base de datos."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nombre, dni, telefono, email) VALUES (?, ?, ?, ?)", (cli['nombre'], cli.get('dni'), cli.get('telefono'), cli.get('email')))
    conn.commit()

def buscar_cliente_por_id(conn, cli_id):
    """Busca y devuelve un único cliente por su ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cli_id,))
    fila = cursor.fetchone()
    if not fila: return None
    columnas = [desc[0] for desc in cursor.description]
    return dict(zip(columnas, fila))

def actualizar_cliente(conn, cli_id, datos_actualizados):
    """Actualiza uno o más campos de un cliente existente."""
    set_clause = ", ".join([f"{key} = ?" for key in datos_actualizados.keys()])
    valores = list(datos_actualizados.values())
    valores.append(cli_id)
    sql = f"UPDATE clientes SET {set_clause} WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, valores)
    conn.commit()

def soft_delete_cliente_por_id(conn, cli_id):
    """
    Realiza un borrado lógico (soft-delete) de un cliente.
    
    En lugar de borrarlo de verdad, solo lo marco como inactivo.
    Así no pierdo su referencia en ventas antiguas.
    """
    if cli_id == 1: return False # No se puede borrar al Consumidor Final
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET is_activo = 0 WHERE id = ?", (cli_id,))
    conn.commit()
    return cursor.rowcount > 0

def buscar_cliente_por_dni(conn, dni):
    """
    Busca un cliente por su DNI, ignorando los puntos en la búsqueda.
    """
    cursor = conn.cursor()
    # Uso REPLACE para que la búsqueda funcione con o sin puntos
    cursor.execute("SELECT * FROM clientes WHERE REPLACE(dni, '.', '') = ?", (dni.replace('.', ''),))
    fila = cursor.fetchone()
    if not fila: return None
    columnas = [desc[0] for desc in cursor.description]
    return dict(zip(columnas, fila))

def registrar_venta(conn, vta_datos):
    """
    Registro una venta completa y actualizo el stock en una transacción segura.

    Esta función es crítica. La envuelvo en una 'transacción' para evitar
    inconsistencias. Esto significa que o todas las operaciones (registrar venta,
    detalles, actualizar stock) se completan con éxito, o si una sola falla,
    revierto todo con el 'rollback'. Así me aseguro de que la base de datos
    siempre quede en un estado correcto.
    """
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO ventas (cliente_id, usuario_id, total, estado) VALUES (?, ?, ?, ?)", (vta_datos['cli_id'], vta_datos['usr_id'], vta_datos['total'], 'Completada'))
        venta_id = cursor.lastrowid
        for item in vta_datos['carrito']:
            cursor.execute("INSERT INTO ventas_detalle (venta_id, producto_id, cantidad, precio_unitario_venta) VALUES (?, ?, ?, ?)", (venta_id, item['id'], item['qty'], item['precio_venta']))
            cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (item['qty'], item['id']))
        conn.commit()
        return venta_id
    except sqlite3.Error:
        conn.rollback()
        return None

def obtener_pin_cancelacion(conn):
    """Obtiene la clave de cancelación actual de la configuración."""
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM configuracion WHERE clave = 'clave_cancelacion'")
    resultado = cursor.fetchone()
    return resultado[0] if resultado else ""

def obtener_venta_por_id(conn, vta_id):
    """Obtiene la cabecera de una venta por su ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ventas WHERE id = ?", (vta_id,))
    fila = cursor.fetchone()
    if not fila: return None
    columnas = [desc[0] for desc in cursor.description]
    return dict(zip(columnas, fila))

def obtener_items_venta(conn, vta_id):
    """Obtiene los items (detalle) de una venta específica."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ventas_detalle WHERE venta_id = ?", (vta_id,))
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    lista_de_items = []
    for fila in filas:
        item_dic = dict(zip(columnas, fila))
        lista_de_items.append(item_dic)
    return lista_de_items

def ejecutar_cancelacion_venta(conn, vta_id, items):
    """
    Marca la venta como 'Cancelada' y restituye el stock de los productos.
    Todo dentro de una transacción para seguridad.
    """
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE ventas SET estado = 'Cancelada' WHERE id = ?", (vta_id,))
        for item in items:
            cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (item['cantidad'], item['producto_id']))
        conn.commit()
        return True
    except sqlite3.Error:
        conn.rollback()
        return False

def obtener_ultimas_ventas(conn, limite = 10):
    """Obtiene las últimas 'N' ventas para facilitar la cancelación."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.id, v.fecha, c.nombre as cliente, v.total
        FROM ventas v
        LEFT JOIN clientes c ON v.cliente_id = c.id
        WHERE v.estado = 'Completada'
        ORDER BY v.id DESC
        LIMIT ?
    """, (limite,))
    return cursor.fetchall()

def obtener_todos_los_usuarios(conn):
    """Obtiene una lista de todos los usuarios."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, nombre_completo, rol, is_activo FROM usuarios")
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    lista_de_usuarios = []
    for fila in filas:
        usuario_dic = dict(zip(columnas, fila))
        lista_de_usuarios.append(usuario_dic)
    return lista_de_usuarios

def actualizar_usuario(conn, usr_id, datos):
    """Actualiza campos de un usuario (para cambiar pwd, nombre o estado)."""
    set_clause = ", ".join([f"{key} = ?" for key in datos.keys()])
    valores = list(datos.values())
    valores.append(usr_id)
    sql = f"UPDATE usuarios SET {set_clause} WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, valores)
    conn.commit()

def obtener_configuracion(conn):
    """Obtiene toda la configuración del sistema como un diccionario."""
    cursor = conn.cursor()
    cursor.execute("SELECT clave, valor FROM configuracion")
    return dict(cursor.fetchall())

def actualizar_configuracion(conn, clave, valor):
    """Actualiza un valor de configuración."""
    cursor = conn.cursor()
    cursor.execute("UPDATE configuracion SET valor = ? WHERE clave = ?", (valor, clave))
    conn.commit()

def agregar_usuario(conn, usr_datos):
    """Inserta un nuevo usuario en la base de datos."""
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, password_hash, nombre_completo, rol) VALUES (?, ?, ?, ?)", (usr_datos['username'], usr_datos['password_hash'], usr_datos['nombre_completo'], usr_datos['rol']))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def buscar_usuario_por_id(conn, usr_id):
    """Busca y devuelve un único usuario por su ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usr_id,))
    fila = cursor.fetchone()
    if not fila: return None
    columnas = [desc[0] for desc in cursor.description]
    return dict(zip(columnas, fila))

def obtener_estadisticas_dashboard(conn):
    """Recopila varias estadísticas clave para el dashboard principal."""
    cursor = conn.cursor()
    stats = {}
    cursor.execute("SELECT SUM(total) FROM ventas WHERE estado = 'Completada'")
    stats['total_vendido'] = cursor.fetchone()[0] or 0.0
    cursor.execute("SELECT COUNT(id) FROM ventas WHERE estado = 'Completada'")
    stats['num_ventas'] = cursor.fetchone()[0] or 0
    cursor.execute("SELECT nombre, stock FROM productos WHERE stock <= 5 ORDER BY stock ASC")
    stats['bajo_stock'] = cursor.fetchall()
    cursor.execute("SELECT p.nombre, SUM(vd.cantidad) as total_cantidad FROM ventas_detalle vd JOIN productos p ON vd.producto_id = p.id JOIN ventas v ON vd.venta_id = v.id WHERE v.estado = 'Completada' GROUP BY p.nombre ORDER BY total_cantidad DESC LIMIT 5")
    stats['top_productos'] = cursor.fetchall()
    return stats

def contar_total_ventas(conn):
    """Cuenta el número total de ventas registradas (completadas o canceladas)."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) FROM ventas")
    return cursor.fetchone()[0]

def obtener_pagina_ventas(conn, pagina, por_pagina):
    """Obtiene una 'página' del historial de ventas, uniendo nombres para claridad."""
    cursor = conn.cursor()
    offset = (pagina - 1) * por_pagina
    cursor.execute("""
        SELECT v.id, v.fecha, v.total, v.estado, c.nombre as cliente, u.username as vendedor
        FROM ventas v
        LEFT JOIN clientes c ON v.cliente_id = c.id
        LEFT JOIN usuarios u ON v.usuario_id = u.id
        ORDER BY v.id DESC
        LIMIT ? OFFSET ?
    """, (por_pagina, offset))
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    ventas_formateadas = []
    for fila in filas:
        venta_dict = dict(zip(columnas, fila))
        venta_dict['nombre'] = f"Venta #{venta_dict['id']} - {venta_dict['fecha'].split()[0]}"
        ventas_formateadas.append(venta_dict)
    return ventas_formateadas

def buscar_clientes_por_termino(conn, termino):
    """
    Busca clientes por nombre, apellido o DNI (ignorando puntos).
    Asegura que solo se busquen clientes activos.
    """
    cursor = conn.cursor()
    termino_like = f'%{termino}%'
    sql = "SELECT id, nombre, dni FROM clientes WHERE (nombre LIKE ? OR REPLACE(dni, '.', '') LIKE ?) AND is_activo = 1"
    cursor.execute(sql, (termino_like, termino_like))
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    lista_de_clientes = []
    for fila in filas:
        cliente_dic = dict(zip(columnas, fila))
        lista_de_clientes.append(cliente_dic)
    return lista_de_clientes

def obtener_ventas_por_cliente_id(conn, cli_id):
    """Obtiene todas las ventas asociadas a un ID de cliente."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, fecha, total, estado FROM ventas WHERE cliente_id = ? ORDER BY id DESC", (cli_id,))
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    ventas_formateadas = []
    for fila in filas:
        venta_dict = dict(zip(columnas, fila))
        venta_dict['nombre'] = f"Venta #{venta_dict['id']} - {venta_dict['fecha'].split()[0]} - ${venta_dict['total']:.2f}"
        ventas_formateadas.append(venta_dict)
    return ventas_formateadas