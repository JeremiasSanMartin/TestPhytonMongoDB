import requests
from registro import generar_registro
from mongodb import obtener_latitudes_desde_bd
from mongodb import obtener_longitudes_desde_bd
# Obtener provincias desde la API
def obtener_provincias():
    # Solicitud GET a la API
    url = "https://apis.datos.gob.ar/georef/api/provincias"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['provincias']
    except Exception as e:
        generar_registro(f"Error al obtener provincias: {e}")
        return []

# Obtener localidades por provincia desde la API
def obtener_localidades(provincia_nombre):
    # Solicitud GET a la API
    url = f"https://apis.datos.gob.ar/georef/api/municipios?provincia={provincia_nombre}&max=500"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['municipios']
    except Exception as e:
        generar_registro(f"Error al obtener localidades de {provincia_nombre}: {e}")
        return []

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

        for localidad in localidades:
            if "centroide" not in localidad:
                generar_registro(f"La localidad {localidad['nombre']} no tiene datos de centroide.")
                continue

            lat = localidad["centroide"]["lat"]
            lon = localidad["centroide"]["lon"]
            nombre_localidad = localidad["nombre"]

            # Construir la URL de la API de OpenWeather
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={APIkey}&units=metric&lang=es"

            try:
                # Realizar la solicitud a la API
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                # Preparar los datos del clima
                clima = {
                    "localidad": nombre_localidad,
                    "lat": lat,
                    "lon": lon,
                    "temperatura_actual": data["current"]["temp"],
                    "descripcion": data["current"]["weather"][0]["description"],
                    "humedad": data["current"]["humidity"],
                    "viento": data["current"]["wind_speed"],
                    "timestamp": data["current"]["dt"]
                }
                clima_localidades.append(clima)
                generar_registro(f"Clima obtenido para la localidad {nombre_localidad}.")
            except Exception as e:
                generar_registro(f"Error al obtener clima para {nombre_localidad}: {e}")
                continue

        return clima_localidades
    except Exception as e:
        generar_registro(f"Error al procesar las localidades: {e}")
        return []