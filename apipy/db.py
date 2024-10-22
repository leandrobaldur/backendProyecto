import psycopg2

def obtener_conexion():
    try:
        conexion = psycopg2.connect(
            host='localhost',     # Cambia si es necesario
            user='postgres',     # Cambia por tu usuario de PostgreSQL
            password='admin',  # Cambia por tu contraseña
            dbname='proyecto'        # Cambia por tu base de datos
        )
        return conexion
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
