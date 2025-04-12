import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

def reset_pending_transactions():
    """Limpia cualquier transacción pendiente en la base de datos."""
    try:
        # Crear conexión a la base de datos
        engine = create_engine(DATABASE_URL)
        
        # Ejecutar ROLLBACK para limpiar transacciones pendientes
        with engine.connect() as conn:
            conn.execute(text("ROLLBACK"))
            print("Transacciones pendientes limpiadas correctamente.")
        
        return True
    except Exception as e:
        print(f"Error al limpiar transacciones pendientes: {e}")
        return False

if __name__ == "__main__":
    reset_pending_transactions()
