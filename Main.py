from mongodb import conectar_mongodb, guardar_provincias, guardar_localidades, guardar_clima_en_bd, consultar_clima_por_localidad
from apis import obtener_provincias, obtener_localidades, obtener_clima_localidades

def cargar_datos_iniciales(db):
    """
    Carga automáticamente los datos de provincias, localidades y clima en la base de datos.
    """
    print("Cargando datos...")

    # Obtener y guardar provincias desde la API
    provincias = obtener_provincias()
    if provincias:
        guardar_provincias(db, provincias)

        # Obtener y guardar localidades desde la API para cada provincia
        for provincia in provincias:
            provincia_nombre = provincia['nombre']
            localidades = obtener_localidades(provincia_nombre)
            if localidades:
                guardar_localidades(db, localidades, provincia_nombre)

    # Obtener y guardar el clima para todas las localidades
    clima = obtener_clima_localidades(db)
    if clima:
        guardar_clima_en_bd(db, clima)

    print("Datos cargados exitosamente.\n")


def consultar_clima(db):
    """
    Solicita al usuario una localidad y muestra el clima de esa localidad.
    """
    while True:
        localidad = input("Ingrese el nombre de la localidad para consultar el clima (o '0' para salir): ").strip()

        if localidad == "0":
            print("Saliendo del programa...")
            break

        if not localidad:
            print("Debe ingresar el nombre de una localidad.")
            continue

        # Llamar a la función corregida
        resultado = consultar_clima_por_localidad(db, localidad)

        if resultado:
            #faltan los demas datos de clima
            print(f"Clima en la localidad {resultado['localidad']}:")
            print(f"  Temperatura actual: {resultado['temperatura_actual']}°K")
            print(f"  Latitud: {resultado['lat']}")
            print(f"  Longitud: {resultado['lon']}")
            print("-" * 40)
        else:
            print(f"No se encontraron datos de clima para la localidad {localidad}.\n")

if __name__ == "__main__":
    db = conectar_mongodb()
    if db is not None:  # Comparación explícita
        cargar_datos_iniciales(db)
        consultar_clima(db)
    else:
        print("No se pudo conectar a la base de datos. Saliendo del programa.")
