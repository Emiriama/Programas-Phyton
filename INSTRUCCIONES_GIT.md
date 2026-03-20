# Cómo subir este proyecto a GitHub

Sigue estos pasos una sola vez para configurar tu repositorio.

## 1. Crea el repositorio en GitHub
- Ve a https://github.com/new
- Ponle un nombre, por ejemplo: `ejercicios-tkinter`
- Déjalo en **Public** para que tu maestra pueda verlo
- NO marques "Add a README" (ya lo tienes)
- Clic en **Create repository**

## 2. Abre una terminal en la carpeta del proyecto

```bash
cd proyecto-tkinter
```

## 3. Inicializa Git y sube todo

```bash
git init
git add .
git commit -m "Ejercicio 01 - Sistema de Aumento de Sueldos"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/ejercicios-tkinter.git
git push -u origin main
```
> Cambia TU_USUARIO por tu nombre de usuario de GitHub.

---

## Cada vez que termines un ejercicio nuevo:

```bash
git add .
git commit -m "Ejercicio 02 - Nombre del ejercicio"
git push
```

---

## Compartir con tu maestra
Solo envíale el link de tu repositorio:
```
https://github.com/TU_USUARIO/ejercicios-tkinter
```
