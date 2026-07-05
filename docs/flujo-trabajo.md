# Flujo de trabajo del equipo

## Ramas
- main: producción
- develop: integración
- feature/*: desarrollo por módulo

## Reglas
1. Nunca trabajar directo en main ni en develop.
2. Cada cambio importante debe ir en un commit claro.
3. Antes de subir cambios, actualizar con `git pull origin develop`.
4. Crear Pull Request para integrar cambios.
5. Julio revisa y hace merge.

## Cómo bajar y actualizar cambios
Cada vez que empiecen a trabajar:

```bash
git checkout develop
git pull origin develop
```

Si van a trabajar en una rama específica:

```bash
git checkout feature/documentos
git pull origin develop
```

## Orden de trabajo recomendado
El orden más claro para que el proyecto quede listo es:

1. feature/estructura-proyecto
   - base del proyecto
   - configuración inicial
   - apps, templates y rutas

2. feature/documentos
   - CRUD de documentos
   - subida, descarga y eliminación
   - modelo Documento

3. feature/certificados
   - carga de archivos .cer y .key
   - lectura de información del certificado

4. feature/firma-digital
   - lógica de firma digital
   - verificación de firma

5. feature/dashboard
   - panel principal
   - cards y resumen

6. feature/historial
   - historial de acciones
   - auditoría y pruebas finales

## Nota práctica
Sí, en este momento la rama que sigue es feature/documentos, porque ya quedó preparada la base del proyecto. La idea es trabajar por módulos en ese orden para que cada parte se construya sobre lo anterior y no se rompa la integración.
