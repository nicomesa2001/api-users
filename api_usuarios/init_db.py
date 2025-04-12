from app.database.db_config import SessionLocal, engine, Base
from app.models.user import User
from app.auth.auth import get_password_hash
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def init_db():
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión
    db = SessionLocal()
    
    # Verificar si ya existe un usuario administrador
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "adminpassword")
    admin_name = os.getenv("ADMIN_NAME", "Administrador")
    
    existing_user = db.query(User).filter(User.email == admin_email).first()
    
    if not existing_user:
        # Crear usuario administrador
        hashed_password = get_password_hash(admin_password)
        admin_user = User(
            email=admin_email,
            full_name=admin_name,
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print(f"Usuario administrador creado: {admin_email}")
    else:
        print(f"El usuario administrador ya existe: {admin_email}")
    
    db.close()

if __name__ == "__main__":
    init_db()
