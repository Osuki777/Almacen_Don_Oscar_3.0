# Criterios comunes de autoría, privacidad y publicación

Versión 1 — 28 de octubre de 2026. Aplicación a este repositorio; no implica que otros proyectos del autor hayan superado una auditoría.

## Autoría y derechos

Se identifica a **Oscar Salvador Fernandez (Osuki777)** como autor/responsable del proyecto y de sus aportes originales conforme a sus avisos existentes. Se conservan los años, citas, permisos específicos y créditos originales, incluida la asistencia de herramientas cuando esté documentada. No se atribuyen en exclusiva materiales de terceros, ideas ni contenido no protegible. No se declara un registro DNDA, una marca registrada o una certificación que no esté acreditada.

`LICENSE` conserva su vigencia y sus permisos específicos. Estos criterios no la reemplazan, no revocan autorizaciones válidas ni convierten el proyecto en código abierto. La visibilidad pública no concede por sí sola una licencia general de explotación comercial; las funciones de GitHub permiten ver y hacer forks dentro de la plataforma conforme a sus términos. No se promete impedir técnicamente copias. Las dependencias, imágenes, fuentes, citas y materiales de terceros conservan sus licencias y atribuciones.

## Datos, claves y funcionamiento real

Las claves privadas de firma, contraseñas, tokens, bases reales, respaldos incluso cifrados, documentos y capturas con información privada quedan fuera del repositorio. El certificado público de una APK y las sumas de verificación no equivalen a una clave privada.

La documentación debe indicar qué almacena la edición concreta, dónde, qué transmite, cómo se exporta o elimina y qué no puede recuperar. No se extiende la afirmación «offline» a un despliegue web completo sin verificar sus recursos, servidor, autenticación, analítica e integraciones. No se infiere tratamiento de datos solo porque exista una carpeta heredada de infraestructura; tampoco se elimina esa infraestructura sin estudiar sus dependencias.

## Seguridad y evidencia

Se distingue entre **documentado**, **comprobado** y **pendiente**. No usar «seguro», «sin riesgo», «probado», «cifrado» o «listo para producción» como garantía general. Un hash de integridad no acredita autoría por sí solo ni demuestra seguridad. El hash de contraseñas no es cifrado de una base ni evita todo ataque.

Toda prueba debe indicar versión y alcance: lógica, navegador, emulador, teléfono o despliegue. La aprobación de una edición no se traslada automáticamente a otra. Los ZIP, APK, PDF, imágenes y bundles históricos son entregas independientes: los cambios de documentación en la raíz no modifican sus bytes ni sus garantías. No reemplazarlos silenciosamente ni renovar sus sumas sin verificarlos.

## Publicación y mantenimiento

Antes de publicar o actualizar: comprobar archivos e historial, revisar manualmente imágenes y contenedores no inspeccionados, comprobar licencias, datos de ejemplo, releases, registros de Actions y referencias públicas. El comprobador local ayuda pero no certifica el resultado. Un secreto real publicado debe revocarse/rotarse y tratarse también en el historial; agregarlo a `.gitignore` no basta.

Prioridad a cambios aditivos y compatibles. Quitar algo solo por una razón documentada —secreto, dato privado, afirmación falsa o dependencia efectivamente innecesaria—, con respaldo y verificación. No borrar historial, eliminar datos ni cambiar visibilidad o permisos como parte de una normalización documental.

## Documentos y referencias

- [Seguridad](SECURITY.md)
- [Revisión y pendientes concretos](REVISION_PUBLICACION.md)
- `python3 comprobar_publicacion.py .` — archivos actuales y contenedores ZIP/APK/JAR.
- `python3 comprobar_publicacion.py . --history` — además, objetos alcanzables de las referencias del clon local; no incluye ramas remotas que no se hayan traído.

Referencias primarias: [licencias en GitHub](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository), [visibilidad](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility) y [almacenamiento de contraseñas OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).

Estos textos no sustituyen una revisión jurídica ni una auditoría de seguridad del producto o despliegue.
