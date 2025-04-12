# API de Gestión de Usuarios

API RESTful para gestión de usuarios con autenticación JWT utilizando Python 3.12, FastAPI y PostgreSQL.

## Características

- Autenticación JWT
- Gestión completa de usuarios (CRUD)
- Validación de datos
- Migraciones de base de datos con Alembic
- Conexión a PostgreSQL

## Requisitos

- Python 3.12
- PostgreSQL
- Pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:

```bash
git clone <url_del_repositorio>
cd api_usuarios
```

2. Crear un entorno virtual e instalar dependencias:

```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

3. Variables de entorno:

El proyecto ya contiene un archivo `.env` configurado con los siguientes valores:

```
DATABASE_URL=postgresql://postgres:GoccYXshsENGrHaqhseNPWiyAUDhTrEg@mainline.proxy.rlwy.net:44570/railway
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Ejecutar migraciones:

```bash
cd api_usuarios
alembic upgrade head
```

## Ejecutar el servidor

```bash
cd api_usuarios
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`

## Documentación

La documentación automática estará disponible en:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints principales

- `/auth/token` - Obtener token JWT (login)
- `/users/` - CRUD de usuarios
- `/users/me` - Obtener perfil del usuario actual

## Ejemplos de uso

### Crear un usuario

```bash
curl -X 'POST' \
  'http://localhost:8000/users/' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "usuario@ejemplo.com",
  "username": "usuario1",
  "full_name": "Usuario Ejemplo",
  "password": "contraseña123"
}'
```

### Obtener token (login)

```bash
curl -X 'POST' \
  'http://localhost:8000/auth/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=usuario1&password=contraseña123'
``` 