from pymongo import MongoClient
from modulos.registro import generar_registro  
from modulos.apis import obtener_provincias, obtener_localidades, obtener_clima_localidades
from pymongo import MongoClient

#funcion para crear la base de datos o conectarse si ya esta creada
def conectar_o_crear_bd():
    
    nombre_bd="argentina"
 
    try:
        
        client = MongoClient('mongodb://localhost:27017/')
        db = client[nombre_bd]
        
        #se verifica si la base de datos ya existe
        if nombre_bd in client.list_database_names():
            generar_registro(f"Conexion exitosa a la base de datos: '{nombre_bd}'")
        else:
            #si no existe, se crea la base de datos con sus colecciones
            generar_registro(f"Creando la base de datos '{nombre_bd}'...")
            colecciones= ["provincias", "localidades", "clima"]
            for coleccion in colecciones:
                db.create_collection(coleccion)
                generar_registro(f"Coleccion '{coleccion}' creada en la base de datos '{nombre_bd}'.")
            generar_registro(f"Base de datos '{nombre_bd}' creada y lista para su uso.")
        
        return db
    except Exception as e:
        print(f"Error al conectar o crear la base de datos: {e}")
        return None


#funcion para guardar las provincias en la db
def guardar_provincias(db, provincias):
    coleccion = db['provincias']
    try:
        coleccion.delete_many({})  
        coleccion.insert_many(provincias)
        generar_registro(f"Se guardaron {len(provincias)} provincias en MongoDB.")
    except Exception as e:
        generar_registro(f"Error al guardar provincias: {e}")

#funcion para guardar las localidades en la db
def guardar_localidades(db, localidades, provincia_nombre):
    coleccion = db['localidades']
    try:
        coleccion.delete_many({"provincia": provincia_nombre})
        for localidad in localidades:
            localidad['provincia'] = provincia_nombre
        coleccion.insert_many(localidades)
        generar_registro(f"Se guardaron {len(localidades)} localidades de {provincia_nombre} en MongoDB.")
    except Exception as e:
        generar_registro(f"Error al guardar localidades de {provincia_nombre}: {e}")

#funcion para guardar los climas en la db    
def guardar_clima_en_bd(db, clima_localidades):
    try:
        coleccion_clima = db["clima"]  

        for clima in clima_localidades:
            try:
                
                coleccion_clima.update_one(
                    {"localidad": clima["localidad"]},  
                    {"$set": clima},  
                    upsert=True  
                )
                generar_registro(f"Clima guardado para la localidad {clima['localidad']}.")
            except Exception as e:
                generar_registro(f"Error al guardar clima para {clima['localidad']}: {e}")
    except Exception as e:
        generar_registro(f"Error al guardar datos del clima en la base de datos: {e}")

#funcion para las consultas
def consultar_clima_por_localidad(db, nombre_localidad):
    try:
        coleccion_clima = db["clima"]
        clima = coleccion_clima.find_one({"localidad": nombre_localidad})

        if clima:
            generar_registro(f"El usuario busco el clima de {nombre_localidad}.")
            return {
                "localidad": clima.get("localidad"),
                "temperatura_actual": clima.get("temperatura_actual"),
                "descripcion": clima.get("descripcion"),
                "humedad": clima.get("humedad"),   
                
            }
            
        else:
            generar_registro(f"No se encontraron datos de clima para la localidad {nombre_localidad}.")
            return None

    except Exception as e:
        generar_registro(f"Error al consultar el clima para la localidad {nombre_localidad}: {e}")
        return None

#funcion para traer los datos de la api y cargarlos en la db
def cargar_datos_iniciales(db):
  
    generar_registro("Cargando datos...")

    #provincias
    provincias = obtener_provincias()
    if provincias:
        guardar_provincias(db, provincias)
    #localidades
    for provincia in provincias:
        provincia_nombre = provincia['nombre']
        localidades = obtener_localidades(provincia_nombre)
        if localidades:
            guardar_localidades(db, localidades, provincia_nombre)
    #climas
    clima = obtener_clima_localidades(db)
    if clima:
        guardar_clima_en_bd(db, clima)

    generar_registro("Datos cargados exitosamente.\n")

#consultas del usuario por consola
def consultar_clima(db):
 
    while True:
        localidad = input("Ingrese el nombre de la localidad para consultar el clima (o '0' para salir): ").strip()

        if localidad == "0":
            print("Saliendo del programa...")
            generar_registro("Saliendo del programa...")
            break

        if not localidad:
            print("Debe ingresar el nombre de una localidad.")
            continue

        resultado = consultar_clima_por_localidad(db, localidad)

        if resultado:
           
            print(f"Clima en la localidad {resultado['localidad']}:")
            print(f"  Temperatura actual: {resultado['temperatura_actual']}°C")
            print(f"  Descripcion: {resultado['descripcion']}")
            print(f"  Humedad: {resultado['humedad']}%")
            print("-" * 40)
        else:
            print(f"No se encontraron datos de clima para la localidad {localidad}.\n")

