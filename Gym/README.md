# GYM PRO RF01–RF50 · versión web

Aplicación web basada en Flask que reutiliza la lógica de negocio y la base de datos del proyecto original de escritorio. Incluye módulos de clientes, empleados, entrenadores, membresías/pagos, accesos/asistencia, máquinas, rutinas, clases, pagos a instructores, resumen mensual, reportes y usuarios por rol.

## Ejecutar localmente

Requiere Python 3.10 o superior.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

En Windows PowerShell:

```powershell
$env:GYM_ADMIN_PASSWORD="cambia-esta-clave"
python app.py
```

Abre http://127.0.0.1:5000. Usuario inicial: `admin`. La contraseña será la que configures en `GYM_ADMIN_PASSWORD`; debes definirla antes de iniciar la aplicación.

## Publicar en Render

El repositorio incluye `render.yaml` para crear un Web Service. La configuración utiliza:

- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app --workers 1 --threads 4 --timeout 120`
- SQLite: `/var/data/gimnasio.db`
- Disco persistente: `/var/data` (1 GB)
- Variables: `SECRET_KEY` autogenerada, `GYM_ADMIN_USER` y `GYM_ADMIN_PASSWORD`.

**Importante:** Render exige un servicio de pago para adjuntar un disco persistente. Sin ese disco, SQLite se perdería al reiniciar o volver a desplegar. El `render.yaml` usa el plan `starter` (nombre heredado del plan de pago). Puedes cambiar a PostgreSQL en una siguiente etapa si esperas múltiples instancias o mayor concurrencia.

### Pasos de despliegue

1. Sube todos los archivos de esta carpeta a la raíz del repositorio de GitHub.
2. En Render, selecciona **New + → Blueprint**.
3. Conecta GitHub y elige el repositorio que contiene `render.yaml`.
4. Antes de confirmar, Render pedirá `GYM_ADMIN_PASSWORD`: define una contraseña larga, única y privada. Puedes cambiar `GYM_ADMIN_USER` si quieres.
5. Revisa que el servicio tenga el disco `gym-pro-data` montado en `/var/data` y crea el Blueprint.
6. Espera a que termine el deploy y abre la URL `https://...onrender.com`.
7. Inicia sesión con el usuario y contraseña configurados.

## Seguridad y datos

- No subas `gimnasio.db`, contraseñas ni datos personales al repositorio.
- Los usuarios creados desde el módulo Usuarios almacenan contraseñas con hash.
- Las contraseñas heredadas en texto plano se convierten a hash al iniciar sesión correctamente.
- Haz copias de seguridad periódicas del archivo SQLite que está en `/var/data`.
- La app usa una sola instancia porque SQLite y el disco persistente están asociados a un único servicio.

## Alcance de esta conversión

Se implementó una primera interfaz web para las operaciones de los módulos RF01–RF50 y se mantuvo la lógica de datos del proyecto original. Antes de utilizarla con datos reales, conviene hacer pruebas funcionales completas con usuarios de cada rol, fechas, pagos, membresías y reportes. La base SQLite está pensada para una instalación pequeña de una sola instancia; para producción con varios usuarios concurrentes se recomienda migrar a PostgreSQL.
