# PFI
Proyecto Final Integrador


Al ejecutar el programa de inventario, el usuario verá un menú interactivo donde puede agregar productos, ver productos o articulos con bajo stock, actualizar cantidades o eliminar productos.
Los datos se guardan en el archivo inventario.db, que puede abrirse con cualquier herramienta compatible con SQLite para ver y manipular los datos.


Se utiliza SQLite: a traves la conexión con la base de datos inventario.db. Si la base de datos no existe, SQLite la creará automáticamente.

Crea la tabla productos si no existe. Esta tabla tiene las columnas id, nombre, descripcion, cantidad, y precio.

Agregar un producto:
  La función registrar_producto() inserta un nuevo producto en la tabla.

Mostrar los productos:
  La función mostrar_productos() consulta y muestra todos los productos en el inventario.

Actualizar :
  	La función actualizar_producto() permite actualizar la cantidad de un producto en base a su id.

Eliminar un producto:
  	La función eliminar_producto() elimina un producto de la tabla por su id.

Buscar producto
	La función buscar_producto() busca un producto de la tabla por su id

Reporte Bajo Stock
Esta funcion solicita al usuario el parametro minismo de stock para asi mostrar los articulos en la tabla que cumplan con ese parametro

y la funcion salir que hace un break y permite salir del aplicativo

Interfaz de usuario:
	El programa tiene un menú de opciones que permite al usuario seleccionar lo que desea hacer (agregar, mostrar, actualizar o eliminar productos).


Cursante Luis Mirabal
