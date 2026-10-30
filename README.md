# Almacén de Don Oscar 3.0

![Menú principal](docs/images/almacen_menu.png)

**La caja del barrio, sin alquilar un sistema.** Stock, clientes, ticket y dos llaves: admin y cajero.

| | |
|---|---|
| **Para quién** | Un almacén que vende en el mostrador y no quiere una mensualidad |
| **Qué incluye** | Productos, clientes, ventas, informes y copia de seguridad |
| **Qué no hace** | No es una tienda online. No cobra con tarjeta. Corre en la computadora del local |

## Propósito

Sistema de punto de venta (POS) de consola en Python para gestionar inventario, clientes, ventas y caja en un almacén de barrio.

## Público

Dueños y cajeros de almacenes que necesitan un sistema simple, local y sin costo mensual.

## Funciones principales

- Gestión de productos (alta, edición, eliminación, stock)
- Registro de clientes (búsqueda por ID o DNI)
- Proceso de venta ágil con impresión de ticket
- Roles: Admin (control total) y Cajero (permisos limitados)
- Informes: dashboard de ventas, productos populares, stock bajo
- Protección de acceso (PBKDF2)
- Copia de seguridad

## Capturas

| Vista | Descripción |
|-------|-------------|
| Menú principal | Opciones de navegación |
| Venta | Flujo de venta y ticket |
| Stock | Gestión de productos e inventario |

## Instalación / Uso

1. Tené Python 3 instalado.
2. Entrá a la carpeta del proyecto.
3. Instalá colorama: `pip install colorama`
4. Ejecutá: `python main.py`
5. En el primer arranque configurá usuario, contraseña y PIN.

## Estado

- **Versión:** 3.0
- **Estado:** Funcional
- **Formato:** Aplicación de consola Python

## Limitaciones

- Es un sistema de consola local. No es tienda online.
- No procesa pagos con tarjeta.
- Corre en la computadora del local.
- No es software libre ni de código abierto.
- La protección de contraseñas no cifra la base SQLite completa.

## Derechos

© 2025–2026 Oscar Salvador Fernandez, Buenos Aires, Argentina.  
Todos los derechos reservados. No es código abierto.

Ver [LICENSE](LICENSE) y [LEGAL.md](LEGAL.md).

---

**Cita:** Fernandez, Oscar Salvador. *Almacén de Don Oscar 3.0: Sistema de punto de venta.* Buenos Aires, 2025.
