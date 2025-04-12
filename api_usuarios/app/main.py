from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, auth
from app.database.db_config import engine, Base
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestión de Usuarios",
    description="API para gestionar usuarios con autenticación JWT",
    version="1.0.0"
)

# Configuración de CORS
origins = []
# Obtener orígenes permitidos de variables de entorno o usar valores predeterminados
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,https://pwa-test.vercel.app,https://pwa-test-7ypj.vercel.app")
if allowed_origins:
    origins.extend(allowed_origins.split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista de orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "API de Gestión de Usuarios"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}