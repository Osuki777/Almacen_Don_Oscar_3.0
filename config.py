# config.py
"""
Almacena todas las constantes y configuraciones globales de la aplicación.

Modificar este archivo permite cambiar parámetros clave del sistema
(como el % de ganancia o las credenciales iniciales) sin alterar la
lógica del código principal.
"""

DB_NAME = "almacen.db"
BACKUP_DIR = "backups"

# Credenciales iniciales del administrador
ADMIN_USERNAME_INICIAL = "root"
ADMIN_PASSWORD_INICIAL = "toor"

# Configuración de negocio inicial
PORCENTAJE_GANANCIA_GLOBAL_INICIAL = 0.30  # 30%
CLAVE_CANCELACION_INICIAL = "1234"

# Nombre del programa para mostrar en mensajes finales, esto es modificable facilmente en entorno real... (banner en ascii creado facil en www.asciiart.eu)
NOMBRE_PROGRAMA = "Almacén Don Oscar"