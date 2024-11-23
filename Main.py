from modulos.mongodb import conectar_o_crear_bd, consultar_clima, cargar_datos_iniciales

if __name__ == "__main__":
    db = conectar_o_crear_bd()
    if db is not None:  
        cargar_datos_iniciales(db)
        consultar_clima(db)
    else:
        print("No se pudo conectar a la base de datos. Saliendo del programa.")
