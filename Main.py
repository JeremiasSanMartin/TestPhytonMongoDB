from mongodb import conectar_mongodb, guardar_provincias, guardar_localidades
from apis import obtener_provincias, obtener_localidades

# Función principal
def main():
    # Conexion a la base de datos
    db = conectar_mongodb()
    if db is None:
        return

    # Obtener y guardar provincias desde la API
    provincias = obtener_provincias()
    if provincias:
        guardar_provincias(db, provincias)

        # Obtener y guardar localidades desde la api de cada provincia
        for provincia in provincias:
            provincia_nombre = provincia['nombre']
            localidades = obtener_localidades(provincia_nombre)
            #si encuentra alguna las guarda
            if localidades:
                guardar_localidades(db, localidades, provincia_nombre)

if __name__ == "__main__":
    main()
