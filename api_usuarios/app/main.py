from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, auth
from app.database.db_config import engine, Base

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestión de Usuarios",
    description="API para gestionar usuarios con autenticación JWT",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes en desarrollo
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