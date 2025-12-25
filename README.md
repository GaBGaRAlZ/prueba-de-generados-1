# Proyecto: Página de un hotel para mascotas

## Tabla de contenidos

- Descripción
- Requisitos
- Instalación y configuración
- Ejecución
- Estructura del proyecto
- Principales rutas / blueprints
- Base de datos y scripts
- Cómo contribuir al código (guía técnica)

---

## Descripción

Aplicación web construida con Flask que permite gestionar registros de usuarios, mascotas, reservas y pagos simulados. El proyecto está pensado como base para ampliar funcionalidades o integrarlo en proyectos mayores.

---

## Requisitos

- Python 3.10 o superior
- pip
- Entorno virtual (recomendado)
- Dependencias en `dependencias.txt`

---

## Instalación y configuración

1. Clonar el repositorio:

```bash
git clone <URL-del-repositorio>
cd pagina
```

2. Crear y activar un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows (PowerShell)
```

3. Instalar dependencias:

```bash
pip install -r dependencias.txt
```

4. Configurar variables de entorno (recomendado):

```bash
export SECRET_KEY="cambia-esto-en-produccion"
# Para la conexión a PostgreSQL, definir las variables necesarias si desea sobrescribir las de `config.py`.
```

Nota: en el código actual `index.py` define `app.secret_key = "111"` por simplicidad; en entornos de producción debe establecerse mediante una variable de entorno segura.

---

## Ejecutar la aplicación

Ejecución rápida:

```bash
python index.py
```

La aplicación quedará accesible en `http://127.0.0.1:5000/`.

También puede utilizarse Flask CLI para desarrollo:

```bash
export FLASK_APP=index.py
export FLASK_ENV=development
flask run
```

---

## Estructura del proyecto

```
pagina/
├─ index.py                # Punto de entrada; registra blueprints
├─ config.py               # Configuración y helper de conexión a PostgreSQL (psycopg2)
├─ dependencias.txt        # Lista de dependencias pip
├─ esquema.sql             # Script SQL para crear tablas en la base de datos
├─ templates/              # Plantillas Jinja2 (HTML)
├─ static/                 # Recursos estáticos (CSS, JS, imágenes)
├─ pages/                  # Blueprints organizados por funcionalidad
│  ├─ __init__.py
│  ├─ autenticacion.py     # Rutas de autenticación: login, registro, cerrar sesión
│  ├─ usuario.py           # Perfil y actualización de datos de usuario
│  ├─ mascota.py           # Alta y gestión de mascotas
│  ├─ reserva.py           # Reserva y pago (simulado)
│  └─ publico.py           # Rutas públicas: inicio, servicios, instalaciones
└─ csv/                    # Archivos CSV para datos (razas, nombres, etc.)
```

---

## Principales rutas / blueprints

Ejemplos de endpoints y cómo referenciarlos con `url_for`:

- Público
  - `publico.inicio` → `/`
  - `publico.instalaciones` → `/instalaciones`
  - `publico.servicios` → `/servicios`

- Autenticación (`autenticacion`)
  - `autenticacion.registro` (GET)
  - `autenticacion.iniciar_sesion_get` (GET)
  - `autenticacion.iniciar_sesion` (POST)
  - `autenticacion.registrar` (POST)
  - `autenticacion.cerrar_sesion` (GET)

- Usuario (`usuario`)
  - `usuario.perfil` → `/perfil`
  - `usuario.actualizar_perfil` (POST)

- Mascota (`mascota`)
  - `mascota.alta_mascota` → `/alta_mascota`
  - `mascota.registrar_mascota` (POST)

- Reserva (`reserva`)
  - `reserva.reserva` → `/reserva`
  - `reserva.pago` → `/pago`

Si se renombra un blueprint o endpoint, es necesario actualizar las llamadas en las plantillas (`templates/*.html`) que usan `url_for('<blueprint>.<endpoint>')`.

---

## Base de datos

La aplicación usa PostgreSQL a través de `psycopg2`. La conexión se centraliza en `config.py`, que expone la función `get_db_connection()`.

Ejemplo (actual en `config.py`):

```python
import psycopg2

DB_HOST = "localhost"
DB_NAME = "proyecto"
DB_USER = "aquuz"
DB_PASS = "123"

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )
    return conn
```

Práctica actual en los blueprints:
- Cada vista que necesita acceso a datos importa `get_db_connection()` y usa la conexión de forma explícita:
  - `conn = get_db_connection()`
  - `cur = conn.cursor()`
  - `cur.execute(sql, params)` (consultas parametrizadas con `%s`)
  - `cur.fetchone()` o `cur.fetchall()`
  - `cur.close()` y `conn.close()`

## Cómo contribuir al código

Esta sección explica cómo está organizado el código, cómo se implementan las funciones y las convenciones utilizadas.

1) Estructura y responsabilidades de los archivos
- `index.py`: inicializa la aplicación Flask, configura `app.secret_key` (actualmente en código) y registra los blueprints.
- `config.py`: define parámetros de conexión con la base de datos y exporta `get_db_connection()` que devuelve una conexión `psycopg2`.
- `pages/*.py`: cada archivo define un `Blueprint` y agrupa rutas relacionadas. Ejemplo: `autenticacion.py` contiene rutas y funciones relacionadas con login y registro.

2) Convenciones y estilo de las funciones
- Nombres: usar `snake_case` para funciones y variables, y nombres descriptivos (por ejemplo `iniciar_sesion`, `registrar_mascota`).
- Blueprints: la variable del blueprint termina en `_bp` (por ejemplo `autenticacion_bp`, `mascota_bp`).
- Endpoints: en las plantillas se usan con `url_for('<blueprint>.<endpoint>')`.

3) Patrón común en las vistas
Cada vista HTTP sigue este esquema general:

```python
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import get_db_connection

bp = Blueprint('ejemplo', __name__)

@bp.route('/ruta', methods=['GET', 'POST'])
def nombre_funcion():
    if request.method == 'POST':
        # obtener datos del formulario
        datos = request.form.get('campo')
        # abrir conexión
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT ... WHERE campo = %s', (datos,))
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        # redirigir o renderizar
        return redirect(url_for('otro_blueprint.otra_funcion'))
    return render_template('plantilla.html')
```

4) Sesión y mensajes
- La aplicación usa `session` para almacenar, por ejemplo, `user_id` después del login.
- `flash(message, category)` se usa para mostrar notificaciones al usuario; las categorías comunes son `success`, `danger`, `warning`, `info`.

5) Consultas a la base de datos
- Use siempre consultas parametrizadas (como `cur.execute(sql, params)`) para evitar inyecciones SQL.

6) Ajustes en plantillas
- Si cambia rutas o nombres de funciones, actualice las llamadas en templates (`url_for('<blueprint>.<endpoint>')`) y verifique que los formularios apunten a los endpoints correctos (`<form action="{{ url_for('autenticacion.iniciar_sesion') }}" method="post">`).

