from app.database.db_config import engine
from sqlalchemy import text

def update_schema():
    # Conectar directamente con la base de datos
    with engine.connect() as connection:
        try:
            # Verificar si la columna username existe y eliminarla
            connection.execute(text("ALTER TABLE users DROP COLUMN IF EXISTS username;"))
            print("Columna 'username' eliminada con éxito (o no existía).")
            
            # Verificar si la columna hashed_password no existe y agregarla
            try:
                connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS hashed_password VARCHAR;"))
                print("Columna 'hashed_password' agregada con éxito (o ya existía).")
            except Exception as e:
                # Si hay un error específico porque la sintaxis no es compatible
                print(f"Error al agregar columna con IF NOT EXISTS: {e}")
                # Intentar verificar si la columna existe primero
                result = connection.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'hashed_password';"))
                if not result.fetchone():
                    connection.execute(text("ALTER TABLE users ADD COLUMN hashed_password VARCHAR;"))
                    print("Columna 'hashed_password' agregada con éxito.")
                else:
                    print("La columna 'hashed_password' ya existe.")
            
            connection.commit()
            print("Esquema actualizado correctamente.")
        except Exception as e:
            print(f"Error al actualizar el esquema: {e}")
            connection.rollback()

if __name__ == "__main__":
    update_schema()
