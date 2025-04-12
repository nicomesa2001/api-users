import sys
import os
from sqlalchemy.orm import Session
from app.database.db_config import SessionLocal, engine, Base
from app.models.user import User
from app.auth.auth import get_password_hash
from sqlalchemy import inspect

# Función para verificar si una tabla existe
def table_exists(engine, table_name):
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()

# Eliminar la tabla de usuarios si existe para recrearla con el esquema correcto
if table_exists(engine, 'users'):
    User.__table__.drop(engine)
    print("Tabla de usuarios eliminada para recrearla con el esquema correcto.")

# Crear todas las tablas si no existen
Base.metadata.create_all(bind=engine)
print("Tablas creadas/actualizadas correctamente.")

def create_default_user():
    db = SessionLocal()
    try:
        # Check if default user already exists
        default_user = db.query(User).filter(User.email == "admin@example.com").first()
        if default_user:
            print("Default user already exists.")
            return
        
        # Create default user
        hashed_password = get_password_hash("admin123")
        default_user = User(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(default_user)
        db.commit()
        db.refresh(default_user)
        print(f"Default user created with email: {default_user.email}")
        print("You can now use this user to obtain tokens.")
        
    except Exception as e:
        print(f"Error creating default user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_default_user()
