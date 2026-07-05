# Proceso para integrar a main

## Flujo recomendado
1. Cada integrante trabaja en su rama de funcionalidad:
   - feature/estructura-proyecto
   - feature/documentos
   - feature/certificados
   - feature/firma-digital
   - feature/dashboard
   - feature/historial
2. Cuando una rama está lista, se hace Pull Request hacia develop.
3. Julio revisa el PR, verifica que todo funcione y hace merge a develop.
4. Cuando develop esté estable, Julio hace merge de develop a main.

## ¿Por qué así?
- main representa la versión estable y lista para entregar.
- develop es la rama de integración donde se juntan los avances.
- feature/* permite trabajar de forma ordenada sin romper el proyecto principal.
- Así se evita mezclar cambios incompletos directamente en main.

## Recomendación para Julio
- Revisar que cada PR tenga un objetivo claro.
- Aceptar solo cambios que estén completos y funcionales.
- Hacer merge a develop primero.
- Cuando el proyecto esté listo, hacer merge de develop a main.

## Comandos para Julio
```bash
git checkout develop
git pull origin develop
git checkout main
git pull origin main
git merge develop
git push origin main
```
