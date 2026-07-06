# Flujo de trabajo para la rama feature/documentos

## 1. Clonar el repositorio
```bash
git clone https://github.com/JulioMelendez10/Web_Firma_Digital.git
cd Web_Firma_Digital
```

## 2. Actualizar main antes de crear la rama
```bash
git checkout main
git pull origin main
```

## 3. Crear la rama feature/documentos
```bash
git checkout -b feature/documentos
```

## 4. Trabajar en la rama
- Agregar el modelo `Documento`
- Crear vistas, formularios y templates para CRUD
- Implementar subida y descarga de archivos
- Agregar cálculo de hash SHA256 si aplica
- Probar que todo funcione localmente

## 5. Guardar cambios en commits pequeños
```bash
git add .
git commit -m "Crear modelo Documento"
git commit -m "Agregar vista y template de lista de documentos"
git commit -m "Agregar subida de documento y hash SHA256"
```

## 6. Subir la rama al remoto
```bash
git push -u origin feature/documentos
```

## 7. Crear Pull Request hacia main
- Base: `main`
- Compare: `feature/documentos`
- Título claro, por ejemplo: `feature/documentos: CRUD y subida de documentos`
- Descripción breve de lo que se hizo

## 8. Esperar revisión y merge en main
- No hacer merge directo sin revisión
- Si hay conflictos, actualizar con `git pull origin main` y resolver
