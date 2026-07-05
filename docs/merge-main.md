# Proceso para integrar a main

## Flujo recomendado
1. Cada integrante trabaja en su rama de funcionalidad:
   - feature/estructura-proyecto
   - feature/documentos
   - feature/certificados
   - feature/firma-digital
   - feature/dashboard
   - feature/historial
2. Cuando una rama está lista, se hace Pull Request hacia main.
3. Julio revisa el PR, verifica que todo funcione y hace merge a main.

## ¿Por qué así?
- main representa la versión estable y lista para entregar.
- feature/* permite trabajar de forma ordenada sin romper el proyecto principal.
- Así se evita mezclar cambios incompletos directamente en main.

## Recomendación para Julio
- Revisar que cada PR tenga un objetivo claro.
- Aceptar solo cambios que estén completos y funcionales.
- Hacer merge directo a main cuando el PR esté aprobado.

## Comandos para Julio
```bash
git checkout main
git pull origin main
git merge feature/estructura-proyecto
# o la rama que se esté revisando

git push origin main
```
