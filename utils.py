# Función para guardar mensajes en un archivo de texto
def guardar_en_archivo(mensaje):
    try:
        # Abrir el archivo en modo "a" para sobrescribirlo cada vez que se ejecuta el programa
        with open("registro.txt", "a") as archivo:
            archivo.write(mensaje + "\n")  # Escribir el mensaje seguido de un salto de línea
    except Exception as e:
        print(f"Error al guardar mensaje en archivo: {e}")