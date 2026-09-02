# Almacén de Don Oscar 3.0 — Sistema de Punto de Venta (POS)

**Autor:** Oscar Salvador Fernandez · Buenos Aires, Argentina  
**©** 2025–2026 Oscar Salvador Fernandez. Todos los derechos reservados.  
**Cita:** Fernandez, Oscar Salvador. *Almacén de Don Oscar 3.0: Sistema de punto de venta.* Buenos Aires, 2025.

Ver [LICENSE](./LICENSE) y [LEGAL.md](./LEGAL.md).

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
*   **Es Seguro:** Las contraseñas se guardan hasheadas. Ventas y cancelaciones van en transacciones.

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

Al primer arranque, cambiá las credenciales de administrador en **Panel de Administración → Configuración del Sistema**. No dejes el usuario y la contraseña de fábrica.

---

## Autoría

© 2025–2026 Oscar Salvador Fernandez, Buenos Aires, Argentina.  
Ley 11.723. El derecho nace con la obra. El depósito DNDA (software inédito) es optativo.  
Contacto: [github.com/Osuki777](https://github.com/Osuki777)
