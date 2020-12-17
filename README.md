# ProyectoFinal
1) el archivo models.py no hace nada para el codigo, solo tiene instrucciones de como crear la base de datos via la consola interactiva de python
2) el archivo funciones.py tiene todas las funciones que creé y probe por consola (tiene el CRUD para imagenes y usuarios)
3) se hicieron muchas modificaciones al archivo app.py (incluir librerias y el modelo)
4) la libreria de SQLAlchemy elimina los caracteres peligrosos de las entradas por lo cual no es necesario sanitizar nada antes de enviar a la base de datos
5) use la funcion de hash que vimos en clase (la de werkzeug.security) para las contraseñas cuando se crea o actualiza un usuario el automaticamente encripta la clave y creé un funcion para verificar que la clave coincida con solo usuario y contraseña.
