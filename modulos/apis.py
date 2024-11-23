import requests
from modulos.registro import generar_registro


#funcion para obtener provincias desde la API
def obtener_provincias():
   
    url = "https://apis.datos.gob.ar/georef/api/provincias"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['provincias']
    except Exception as e:
        generar_registro(f"Error al obtener provincias: {e}")
        return []

#funcion para obtener las localidades de cada provincia desde la API
def obtener_localidades(provincia_nombre):
    
    #seteamos el max en 1 para no sufrir sobrecargas/demoras a la hora de probar el programa, este valor deberia cambiarse si se quiere guardar todas las localidades
    url = f"https://apis.datos.gob.ar/georef/api/municipios?provincia={provincia_nombre}&max=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['municipios']
    except Exception as e:
        generar_registro(f"Error al obtener localidades de {provincia_nombre}: {e}")
        return []

#funcion para obtener el clima de cada localidad desde la API
def obtener_clima_localidades(db):
    try:
        # Obtener todas las localidades de la colección
        coleccion_localidades = db["localidades"]
        localidades = list(coleccion_localidades.find())

        if not localidades:
            generar_registro("No se encontraron localidades en la base de datos.")
            return []

        APIkey = "9e0f15069eb1de07860de8224e530bd0"
        clima_localidades = []
        errores = []

        for localidad in localidades:
            if "centroide" not in localidad:
                generar_registro(f"La localidad {localidad['nombre']} no tiene datos de centroide.")
                continue

            lat = localidad["centroide"]["lat"]
            lon = localidad["centroide"]["lon"]
            nombre_localidad = localidad["nombre"]

            #se completa la url de la api con los datos obtenidos de cada localidad
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={APIkey}"

            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                #obtenemos los datos relevantes
                clima = { 
                    "localidad": nombre_localidad,
                    "temperatura_actual": round(data["main"]["temp"] - 273.15, 2), #formula para pasar de kelvin a celsius
                    "descripcion": data["weather"][0]["description"],
                    "humedad": data["main"]["humidity"],     
                }
                clima_localidades.append(clima)
            except Exception as e:
                errores.append(f"Error al obtener clima para {nombre_localidad}: {e}")
                return[]
            
        if errores:
            generar_registro("Se produjo un error crítico al obtener climas: " + "; ".join(errores))
            return[]
        else:
            generar_registro("Clima obtenido exitosamente para todas las localidades.")
            return clima_localidades
             
    except Exception as e:
        generar_registro(f"Error al procesar las localidades: {e}")
        return []