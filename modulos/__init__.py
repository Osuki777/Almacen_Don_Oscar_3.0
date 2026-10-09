# © 2025-2026 Oscar Salvador Fernandez, Buenos Aires, Argentina.
# Todos los derechos reservados. Ver LICENSE y LEGAL.md.
# modulos/__init__.py
"""
Convierte la carpeta 'modulos' en un paquete de Python.

La presencia de este archivo permite que Python
trate el directorio como un paquete, facilitando la organización del
código y las importaciones limpias en todo el proyecto.

También se puede usar para hacer que las importaciones sean más convenientes
exponiendo las funciones o módulos clave directamente en el nivel del paquete.
"""

# Por ejemplo, podemos exponer los módulos completos
from . import ui
from . import database as db # Podemos incluso definir el alias aquí
from . import auth
from . import productos
from . import clientes
from . import ventas
from . import admin_panel
from . import informes

# Esto nos permitirá en el futuro hacer importaciones como:
# from modulos import ui, db, auth
# en lugar de importar cada archivo por separado.