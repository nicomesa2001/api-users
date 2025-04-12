import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

def check_database_connection():
    """Verifica la conexión a la base de datos sin realizar cambios."""
    try:
        # Crear conexión a la base de datos
        engine = create_engine(DATABASE_URL)
        
        # Verificar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).fetchone()
            if result:
                print("✅ Conexión a la base de datos establecida correctamente.")
                return True
            else:
                print("❌ No se pudo verificar la conexión a la base de datos.")
                return False
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return False

if __name__ == "__main__":
    check_database_connection()
