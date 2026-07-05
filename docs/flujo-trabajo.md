# Flujo de trabajo del equipo

## Ramas
- main: producción
- feature/*: desarrollo por módulo

## Reglas
1. Nunca trabajar directo en main sin revisar primero en una rama feature.
2. Cada cambio importante debe ir en un commit claro.
3. Antes de subir cambios, actualizar con `git pull origin main`.
4. Crear Pull Request hacia main para integrar cambios.
5. Julio revisa y hace merge.

## Cómo bajar y actualizar cambios
Cada vez que empiecen a trabajar:

```bash
git checkout main
git pull origin main
```

Si van a trabajar en una rama específica:

```bash
git checkout feature/documentos
git pull origin main
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
