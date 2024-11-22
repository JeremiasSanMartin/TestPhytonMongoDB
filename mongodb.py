from pymongo import MongoClient
from registro import generar_registro  # Importamos la función para guardar en archivo

# Configuración de MongoDB
def conectar_mongodb():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['argentina']
        generar_registro("Conexión exitosa a MongoDB.")  # Guardar el mensaje en el archivo
        return db
    except Exception as e:
        generar_registro(f"Error al conectar con MongoDB: {e}")
        return None

def guardar_provincias(db, provincias):
    coleccion = db['provincias']
    try:
        coleccion.delete_many({})  # Limpiar colección
        coleccion.insert_many(provincias)
        generar_registro(f"Se guardaron {len(provincias)} provincias en MongoDB.")
    except Exception as e:
        generar_registro(f"Error al guardar provincias: {e}")

def guardar_localidades(db, localidades, provincia_nombre):
    coleccion = db['localidades']
    try:
        for localidad in localidades:
            localidad['provincia'] = provincia_nombre
        coleccion.insert_many(localidades)
        generar_registro(f"Se guardaron {len(localidades)} localidades de {provincia_nombre} en MongoDB.")
    except Exception as e:
        generar_registro(f"Error al guardar localidades de {provincia_nombre}: {e}")
