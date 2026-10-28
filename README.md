# Almacén de Don Oscar 3.0 — Sistema de Punto de Venta (POS)

![El mostrador de un almacén de barrio, de noche, con el ticket en blanco](docs/portada.jpg)

**La caja del barrio, sin alquilar un sistema.** Stock, clientes, ticket y dos llaves: admin y cajero.

| | |
|---|---|
| Para quién | Un almacén que vende en el mostrador y no quiere una mensualidad |
| Qué incluye | Productos, clientes, ventas, informes y copia de seguridad |
| Qué no hace | No es una tienda online. No cobra con tarjeta. Corre en la computadora del local |

**Autor:** Oscar Salvador Fernandez · Buenos Aires, Argentina  
**©** 2025–2026 Oscar Salvador Fernandez. Todos los derechos reservados.  
**Cita:** Fernandez, Oscar Salvador. *Almacén de Don Oscar 3.0: Sistema de punto de venta.* Buenos Aires, 2025.

No es software libre ni de código abierto. Ver [LICENSE](./LICENSE) y [LEGAL.md](./LEGAL.md).

Este es el sistema de gestión para el **Almacén de Don Oscar**. Es una aplicación de consola en Python para inventario, clientes, ventas y caja.

---

## ¿Qué Hace Este Programa?

*   **Gestiona Productos:** Podés agregar, ver, editar y eliminar productos del inventario. La idea es que el nombre sea bien descriptivo (ej: "Arroz Gallo 1kg") para manejar distintas presentaciones.
*   **Lleva un Registro de Clientes:** Mantiene una base de datos de tus clientes, con la posibilidad de buscarlos por su ID o DNI (con o sin puntos).
*   **Procesa Ventas de Forma Rápida:** Flujo de venta ágil para el cajero. Al final, imprime un ticket con el detalle.
*   **Tiene Roles (Admin y Cajero):**
    *   El **Admin** tiene el control total: gestiona cajeros, configuración (ganancia, PIN de cancelación), informes y backups.
    *   El **Cajero** accede a vender, clientes y productos (permisos limitados).
*   **Ofrece Informes Clave:** Dashboard de ventas, productos populares y stock bajo. Historial de ventas.
*   **Protección de acceso:** las contraseñas nuevas usan PBKDF2 con salt aleatorio; los hashes antiguos se actualizan al autenticar. Esto no cifra la base SQLite ni certifica la seguridad integral.

---

## Cómo Ponerlo en Marcha

### ¿Qué Necesitás?

*   **Python 3**. Si no lo tenés: [python.org](https://www.python.org/downloads/).

### Instalación

1.  Descargá el proyecto: carpeta `Almacen_Don_Oscar_3.0`.
2.  Abrí una terminal (PowerShell, CMD o Terminal).
3.  Entrá a la carpeta del proyecto:
    ```bash
    cd Almacen_Don_Oscar_3.0
    ```
4.  Instalá colorama:
    ```bash
    pip install colorama
    ```

### Arranque

Desde la raíz del proyecto:

```bash
python main.py
```

### Primeros pasos

Al primer arranque elegí tu usuario, contraseña y PIN propios. Si actualizás una instalación antigua, los datos se conservan: al autenticar con credenciales de fábrica se exige cambiarlas antes de entrar al menú. Hacé una copia privada de la base antes de actualizar.

---

## Autoría

© 2025–2026 Oscar Salvador Fernandez, Buenos Aires, Argentina.  
Ley 11.723. El derecho nace con la obra. El depósito DNDA (software inédito) es optativo.  
Contacto: [github.com/Osuki777](https://github.com/Osuki777)

## Criterios de mantenimiento y publicación

Ver [CRITERIOS.md](CRITERIOS.md), [SECURITY.md](SECURITY.md) y [REVISION_PUBLICACION.md](REVISION_PUBLICACION.md). Autoría y permisos específicos de la obra se conservan según LICENSE y sus avisos. Publicar no convierte el proyecto en código abierto ni acredita auditoría o certificación.
