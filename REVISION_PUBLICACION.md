# Revisión de publicación — Almacen_Don_Oscar_3.0

28 de octubre de 2026. Ver [CRITERIOS.md](CRITERIOS.md).

## Alcance del proyecto

Sistema local de caja e inventario; contiene datos comerciales y de clientes cuando se usa.

## Revisión y cambios

Se detectó creación con contraseña de fábrica en texto y hash SHA-256 rápido con salt fijo. La corrección adjunta exige credenciales propias en instalaciones nuevas, verifica/migra hashes antiguos al iniciar sesión y exige cambiar credenciales heredadas de fábrica. Se conservan tablas, usuarios, clientes y ventas existentes.

## Pendientes y límites

La base SQLite y respaldos siguen siendo archivos privados; no quedan cifrados por cambiar el hash de contraseñas. El PIN de cancelación mantiene el formato esperado por el sistema y debe protegerse junto a la base. Copiar la base antes de actualizar; no se certifica toda la aplicación ni el historial público.

Esta intervención unifica documentación y controles de mantenimiento; no afirma una auditoría completa de todos los commits, contenedores, dependencias, imágenes, infraestructura o despliegues. No se cambia la visibilidad existente ni los permisos de LICENSE. Los componentes o pruebas no ejecutados permanecen pendientes.

## Antes de publicar una entrega

1. Revisar contenido actual, todas las referencias Git pertinentes y contenedores históricos. Ejecutar el comprobador local y atender sus advertencias sin compartir valores secretos.
2. Revisar manualmente capturas, PDF, video, ZIP, bundles y logs. Un respaldo cifrado también es privado.
3. Revisar licencias y créditos, confirmar versión y pruebas; no extender evidencia entre plataformas.
4. Conservar claves privadas fuera del repositorio y verificar sumas de los artefactos que se distribuyan.
5. Revisar los datos o credenciales incorporados desde esta revisión antes de cualquier cambio de visibilidad.

## Verificación de esta corrección

Nueve pruebas aisladas aprobadas con SQLite en memoria: salt aleatorio, verificación y rechazo de parámetros inválidos, migración de hash legado solo tras contraseña correcta, reemplazo de credencial y PIN de fábrica (incluida la contraseña de fábrica ya hasheada), cancelación atómica, usuario inactivo, alta nueva sin credencial universal y conservación de credencial vigente. Una venta ficticia se conserva durante la migración. No se ejecutó una prueba integral del sistema de caja ni una actualización con datos reales.

Ejecutar desde la raíz: `python3 test_seguridad.py -v`. Mantener una copia privada de la base antes de actualizar una instalación. La corrección cambia el código de futuros inicios; no modifica contraseñas reales desde GitHub ni elimina el historial público que contiene las constantes antiguas.
