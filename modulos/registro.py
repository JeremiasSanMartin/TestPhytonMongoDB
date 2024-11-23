from datetime import datetime

def generar_registro(mensaje, archivo="registro.txt"):
        #se obtiene la fecha y hora actual
        tiempo_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        #se escriben los registros con su fecha y hora
        with open(archivo, 'a') as archivo:
            archivo.write(f'{tiempo_actual} - {mensaje}\n')