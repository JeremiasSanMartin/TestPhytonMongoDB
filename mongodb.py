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

def obtener_latitudes_desde_bd(db):
    try:
        coleccion_localidades = db["localidades"]
        # Extraer latitudes solo si están disponibles
        latitudes = [doc["centroide"]["lat"] for doc in coleccion_localidades.find() if "centroide" in doc and "lat" in doc["centroide"]]
        generar_registro("Latitudes obtenidas de la base de datos.")
        return latitudes
    except Exception as e:
        generar_registro(f"Error al obtener latitudes desde la base de datos: {e}")
        return []
    
def obtener_longitudes_desde_bd(db): 
    try:
        coleccion_localidades = db["localidades"]
        # Extraer longitudes solo si están disponibles
        longitudes = [doc["centroide"]["lon"] for doc in coleccion_localidades.find() if "centroide" in doc and "lon" in doc["centroide"]]
        generar_registro("Longitudes obtenidas de la base de datos.")
        return longitudes
    except Exception as e:
        generar_registro(f"Error al obtener longitudes desde la base de datos: {e}")
        return []
    
def guardar_clima_en_bd(db, clima_localidades):
    try:
        coleccion_clima = db["clima"]  # Colección para guardar el clima

        for clima in clima_localidades:
            try:
                # Guardar o actualizar el clima en la colección
                coleccion_clima.update_one(
                    {"localidad": clima["localidad"]},  # Criterio de búsqueda
                    {"$set": clima},  # Datos a guardar
                    upsert=True  # Si no existe, lo inserta
                )
                generar_registro(f"Clima guardado para la localidad {clima['localidad']}.")
            except Exception as e:
                generar_registro(f"Error al guardar clima para {clima['localidad']}: {e}")
    except Exception as e:
        generar_registro(f"Error al guardar datos del clima en la base de datos: {e}")