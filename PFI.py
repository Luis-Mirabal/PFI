# ******************************************************************
# DECLARACION DE FUNCIONES
# ******************************************************************

import sqlite3

# DECLARACION DE CONSTANTES
ruta_db = r"C:\Users\Casa\Documents\PFI\inventario.db"


from colorama import init, Fore, Style, Back

init()

init(autoreset=True)

#
#db_crear_tabla_productos()
#######################################
#Esta función utiliza a sqlite3 para conectarse con la base "inventario.db" y crea la tabla productos



def db_crear_tabla_productos():
    try:
        conexion = sqlite3.connect("inventario.db")
        cursor = conexion.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                categoria TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )"""
        )
        conexion.commit()
        # print("""Los Datos fueron
        #        Registrados
        #        Exitosamente""")
    except sqlite3.Error as e:
        print(f"Ha ocurrido un error y no fue posible crear la Tabla: {e}")
    finally:
        conexion.close()



#db_insertar_producto(producto)
####################################

#se utiliza un diccionario para almacenar de manera temporal los datos ingresados por el usuario
#y luego seran insertados a la tabla



def db_insertar_producto(producto):
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    query = "INSERT INTO productos (nombre, descripcion, categoria, cantidad, precio) VALUES (?,?,?,?,?)"
    placeholders = (
        producto["nombre"],
        producto["descripcion"],
        producto["categoria"],
        producto["cantidad"],
        producto["precio"],
    )

    cursor.execute(query, placeholders)
    conexion.commit()
    conexion.close()



#db_get_productos()
########################
#se hace una lectura de los datos de la tabla productos
#retorna una lista de tuplas con los datos de la tabla



def db_get_productos():
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    query = "SELECT * FROM productos"
    cursor.execute(query)
    lista_productos = cursor.fetchall()  # retorna una lista de tuplas
    conexion.close()
    return lista_productos


# cursor.fetchone() retorno solo una tupla
##############################################

# db_get_producto_by_id(id)

#se hace una busqueda del ID en la tabla y
#retorna una tupla con el resultado
#


def db_get_producto_by_id(id):
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    query = "SELECT * FROM productos WHERE id = ?"
    placeholders = (id,)
    cursor.execute(query, placeholders)
    producto = cursor.fetchone()
    conexion.close()
    return producto



#db_actualizar_producto(id, nueva_cantidad)

# actualiza la cantidad del producto según el id



def db_actualizar_producto(id, nueva_cantidad):
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    query = "UPDATE productos SET cantidad = ? WHERE id = ?"
    placeholders = (nueva_cantidad, id)
    cursor.execute(query, placeholders)
    conexion.commit()
    conexion.close()



#db_eliminar_producto(id)

# se hace una busqueda por id y se procede a eliminar el articulo si fue encontrado



def db_eliminar_producto(id):
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    query = "DELETE FROM productos WHERE id = ?"
    placeholders = (id,)
    cursor.execute(query, placeholders)
    conexion.commit()
    conexion.close()



#db_get_productos_by_condicion(minimo_stock)

# devuelve una lista con los registros cuya cantidad es inferior a minimo_stock



def db_get_productos_by_condicion(minimo_stock):
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    query = "SELECT * FROM productos WHERE cantidad < ?"
    placeholders = (minimo_stock,)
    cursor.execute(query, placeholders)
    lista_productos = cursor.fetchall()
    conexion.close()
    return lista_productos




#menu_mostrar_opciones()
# muestra un listado con las opciones disponibles
# captura y retorna la opcion seleccionada



def menu_mostrar_opciones():
    print("-" * 30)

    print(Fore.RED +" Menú principal")
    print("-" * 30)
    print(Fore.GREEN +
        """
          1. Agregar producto
          2. Mostrar producto
          3. Actualizar
          4. Eliminar
          5. Buscar producto
          6. Reporte bajo Stock
          7. Salir
        """
    )

    
###------------------------------------------------------------------------------------------

    while True:
        # Solicitar el ingreso del dato
        ingreso = input(Fore.CYAN +"Ingrese la opción deseada: ")

        # Intentar convertir el dato ingresado a un entero
        if ingreso.isdigit() or (ingreso.startswith('-') and ingreso[1:].isdigit()):
            # Convertir a entero
            opcion = int(ingreso)
            
            # Validar que el número esté en el rango de 1 a 7
            if 1 <= opcion <= 7:
                
                #print("La opcion seleccionada fué:", opcion)
                return opcion
                break  # Salir del bucle si la validación es exitosa
            else:
                print("Debe seleccionar una Opción valida. Intenta de nuevo.")
        else:
            print("Eso no es una opcion válida. Intenta de nuevo.")
        
       
               
###-------------------------------------------------------------------------------------------


#menu_registrar_producto()
# Se solicita el ingreso de todos los datos
# validamos los datos y los almacena en un diccionario temporal
# Se llama a la funcion db_insertar_producto(producto) y le pasa el diccionario producto para que lo registre en la base de datos



def menu_registrar_producto():
    print("\nIngrese los siguientes datos del producto:")
    nombre = validacion_get_nombre()
    descripcion = validacion_get_descripcion()
    categoria = validacion_get_categoria()
    cantidad = validacion_get_cantidad()
    precio = validacion_get_precio()

    # Creamos un diccionario temporal
    producto = {
        "nombre": nombre,
        "descripcion": descripcion,
        "categoria": categoria,
        "cantidad": cantidad,
        "precio": precio,
    }
    db_insertar_producto(producto)
    print(Fore.GREEN +"\nProducto insertado exitosamente")



#menu_mostrar_productos()
# no recibe ningún argumento
# llama a la funcion  db_get_productos() que retorna una lista de tuplas con el contenido de la tabla
# usamos un bucle for para mostrar en consola



def menu_mostrar_productos():
    lista_productos = db_get_productos()

    if lista_productos:
        for producto in lista_productos:
            print(producto)
    else:
        print("No hay productos que mostrar")



#menu_actualizar_producto()
# solicita al usuario que ingrese el id del producto a modificar
# buscamos el producto en la tabla (si no existe informamos)
# mostramos cantidad actual y pedimos que ingrese la nueva cantidad
# llamar a db_actualizar_registro que solo va a actualizar el campo cantidad(id, nueva_cantidad)




def menu_actualizar_producto():
    id = int(input("\nIngrese el id del producto a actualizar"))
    get_producto = db_get_producto_by_id(id)
    if not get_producto:
        print(Fore.CYAN +"ERROR: no se ha encontrado ningún producto con el id {id}")
    else:
        print(f"Cantidad actual {get_producto[4]} ")
        nueva_cantidad = validacion_get_cantidad("Nueva cantidad")
        db_actualizar_producto(id, nueva_cantidad)
        print(Fore.GREEN +"Registro actualizado exitosamente!")



#menu_eliminar_producto()
# solicita al usuario que ingrese el id del producto a eliminar
# buscamos el producto en la tabla (si no existe informamos)
# mostramos el producto y solicitamos confirmación
# llamar a db_eliminar_producto(id)



def menu_eliminar_producto():
    id = int(input("\nIngrese el id del producto a eliminar: "))
    get_producto = db_get_producto_by_id(id)
    if not get_producto:
        print("ERROR: no se ha encontrado ningún producto con el id {id}")
    else:
        print("\nATENCION: se eliminará el siguiente registro:")
        print(get_producto)
        confirmacion = input(
            "\nIngrese 's' para confirmar o cualquier otro para cancelar: "
        ).lower()
        if confirmacion == "s":
            db_eliminar_producto(id)
            print(Fore.GREEN +"Registro eliminado exitosamente!")
        else:
            print(Fore.LIGHTMAGENTA_EX +"Operación cancelada.")



#menu_buscar_producto()
# solicita al usuario que ingrese el id del producto a buscar
# llamar a db_get_producto_by_id(id)



def menu_buscar_producto():
    id = int(input("\nIngrese el id del producto que desea consultar: "))
    get_producto = db_get_producto_by_id(id)
    if not get_producto:
        print(Fore.LIGHTMAGENTA_EX +"ERROR: no se ha encontrado ningún producto con el id {id}")
    else:
        print(get_producto)



#menu_reporte_bajo_stock()
# solicita al usuario que ingrese la cantidad mínima para el reporte
# llamar a db_get_productos_by_condicion(condicion) que retorna una lista_productos



def menu_reporte_bajo_stock():
    minimo_stock = int(input("\nIngrese el unmbral de mínimo stock:"))
    lista_productos = db_get_productos_by_condicion(minimo_stock)
    if not lista_productos:
        print(Fore.CYAN +"No se ha encontrado ningún producto con stock menor a {minimo_stock}")
    else:
        for producto in lista_productos:
            print(producto)



#validacion_get_nombre()

# Solicita el usuario que ingrese el nombre del producto
# No se admite dato nulo
# El nombre puede contener cualquier caracter



def validacion_get_nombre():
    while True:
        nombre = input("Nombre: ").strip()
        if nombre:  # si la variable nombre esta vacia
            break
        else:
            print(Fore.LIGHTMAGENTA_EX +"No se admite dato nulo. Ingrese el nombre: ")
    return nombre



#validacion_get_descripcion()

# Solicita el usuario que ingrese la descripción del producto
# Se admite dato nulo
# La descripción puede contener cualquier caracter



def validacion_get_descripcion():
    descripcion = input("Descripción: ").strip()
    return descripcion  # return es equivalente a break



#validacion_get_categoria()

# Solicita el usuario que ingrese la categoria del producto
# No se admite dato nulo
# La categoría puede contener cualquier caracter



def validacion_get_categoria():
    while True:
        categoria = input("Categoría: ").strip()
        if not categoria:
            print(Fore.LIGHTMAGENTA_EX +"No se admite dato nulo. Ingrese la categoría: ")
        else:
            return categoria



#validacion_get_cantidad()

# Solicita el usuario que ingrese la cantidad del producto
# No se admite dato nulo
# La categoría debe ser entero



def validacion_get_cantidad(mensaje="Cantidad: "):
    while True:
        try:
            cantidad = int(input(f"{mensaje} ").strip())
            if not cantidad:
                print(Fore.LIGHTMAGENTA_EX +"No se admite dato nulo. Ingrese la cantidad: ")
            elif cantidad <= 0:
                print(Fore.LIGHTMAGENTA_EX +"La cantidad debe ser mayor a 0. Ingrese la cantidad: ")
            else:
                return cantidad

        except ValueError:
            print(Fore.LIGHTMAGENTA_EX +"Tipo de dato no valido. Ingrese la cantidad: ")



#validacion_get_precio()

# Solicita el usuario que ingrese el precio del producto
# No se admite dato nulo
# El precio debe ser entero o float



def validacion_get_precio():
    while True:
        try:
            precio = float(input("Precio: ").strip())
            if not precio:
                print(Fore.LIGHTMAGENTA_EX +"No se admite dato nulo. Ingrese el precio: ")
            else:
                return precio

        except ValueError:
            print(Fore.LIGHTMAGENTA_EX +"Tipo de dato no valido. Ingrese el precio: ")



# Declaramos la funcion principal main

def main():
    # Inicializamos la base de datos y creamos la tabla (si no existe)
    db_crear_tabla_productos()

    # Cuerpo de la función main
    while True:
        # menu_mostrar_opciones() muestra y retorna la opcion seleccionada por el usuario
        opcion = menu_mostrar_opciones()
        print("Usted selcciono: ", opcion)
        dato = opcion
        #print ("esta es el valor de la variable", dato)
        if dato == 1:
            menu_registrar_producto()
        elif dato == 2:
            menu_mostrar_productos()
        elif dato == 3:
            menu_actualizar_producto()
        elif dato == 4:
            menu_eliminar_producto()
        elif dato == 5:
            menu_buscar_producto()
        elif dato == 6:
            menu_reporte_bajo_stock()
        elif dato == 7:
            print(Fore.GREEN +"\nSaliendo del Sistema")
            break
        else:
            print("Opción no válida. Por favor, elija una opción válida.")

        continuar = input(
            "\nIngrese 's' para salir o cualquier tecla para conitnuar: "
        ).lower()  # pausa para que el usuario pueda ver
        if continuar == "s":
            print(Fore.RED"\nSaliendo de la Apicación")
            break


# ******************************************************************
# INVOCAMOS A LA FUNCION PRINCIPAL
# ******************************************************************
main()  # invocar o llamar a la funcion main()
