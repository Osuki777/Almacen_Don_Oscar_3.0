# Almacén de Don Oscar - Sistema de Punto de Venta (POS)



Este es el sistema de gestión para el **Almacén de Don Oscar**. Es una aplicación de consola que hice en Python para manejar todo lo importante de un negocio de barrio: inventario, clientes, ventas y caja. La idea fue hacer algo robusto y fácil de usar, pero sin salir de la terminal.

---

## 📋 ¿Qué Hace Este Programa?

*   **Gestiona Productos:** Podés agregar, ver, editar y eliminar productos del inventario. La idea es que el nombre sea bien descriptivo (ej: "Arroz Gallo 1kg") para manejar distintas presentaciones.
*   **Lleva un Registro de Clientes:** Mantiene una base de datos de tus clientes, con la posibilidad de buscarlos por su ID o DNI (con o sin puntos, ¡simplificado!).
*   **Procesa Ventas de Forma Rápida:** Tiene un flujo de venta ágil para que el cajero pueda sumar productos al carrito sin pausas innecesarias. Al final, imprime un ticket con todo el detalle.
*   **Tiene Roles (Admin y Cajero):**
    *   El **Admin** tiene el control total: gestiona a los cajeros, cambia la configuración (como el % de ganancia o el PIN para cancelar ventas), ve informes y hace backups.
    *   El **Cajero** tiene acceso a lo que necesita para el día a día: vender, gestionar clientes y productos (con permisos limitados).
*   **Ofrece Informes Clave:** El admin puede ver un **Dashboard** con un resumen del negocio: cuánto se vendió, qué productos son los más populares y cuáles tienen poco stock. También puede consultar el historial de ventas completo.
*   **Es Seguro:** Las contraseñas se guardan encriptadas (hasheadas) y las operaciones críticas como las ventas y cancelaciones se manejan con transacciones para que la base de datos nunca quede inconsistente.

---

## 🚀 Cómo Ponerlo en Marcha

### ¿Qué Necesitás?

*   Tener **Python 3** instalado. Si no lo tenés, lo bajás de [python.org](https://www.python.org/downloads/).

### Pasos para la Instalación

1.  **Descargá el Proyecto:** Poné la carpeta `Almacen_Don_Oscar_3.0` en algún lugar cómodo de tu equipo.

2.  **Abrí una Terminal:** En Windows es PowerShell o CMD, en Mac/Linux es Terminal.

3.  **Andá a la Carpeta del Proyecto:** Usá el comando `cd` para navegar hasta donde guardaste la carpeta.
    ```bash
    # Ejemplo en Windows:
    cd C:\Users\TuUsuario\Desktop\Almacen_Don_Oscar_3.0
    ```

4.  **Instalá la Única Dependencia:** El programa usa `colorama` para los colores. Lo instalás con este comando:
    ```bash
    pip install colorama
    ```

### ¡A Usarlo!

Para arrancar el programa, asegurate de estar en la carpeta raíz (`aAlmacen_Don_Oscar_3.0/`) y ejecutá:

```bash
python main.py
```

### 🔐 Primeros Pasos

Cuando arranques por primera vez, usá estas credenciales:

*   Usuario: root
*   Contraseña: toor

Importante: Ni bien entres, andá al Panel de Administración (opción 8)> Configuración del Sistema (opción 4) 
y cambiá tu nombre, tu contraseña y el PIN de cancelación por unos que te acuerdes.

Este proyecto fue un desafío para crear una aplicación de consola completa y bien estructurada, pensando siempre en que sea útil y fácil de usar.