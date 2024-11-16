import requests

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
        print(f"Error al obtener provincias: {e}")
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
        print(f"Error al obtener localidades de {provincia_nombre}: {e}")
        return []
