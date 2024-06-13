import sqlite3
import mysql.connector
import time

def conexion_SQLite3():
    try:
        db = 'ValmoMixDB.db'
        conexionSQL = sqlite3.connect(db)
        cursorSQL = conexionSQL.cursor()
        cursorSQL.execute(f"SELECT COUNT(*) FROM tblMPMovimientos")
        count = cursorSQL.fetchone()[0]
    except Exception as e:
        print("Error en la base de datos:", e)
    return conexionSQL, cursorSQL


# Conexion a la base de datos: aqui se hace la conexion a la base de datos MySQL y se valida que la conexion sea correcta
def conexion_MySQL():  
    with open('conexion.txt', 'r') as archivo:
        contenido = archivo.read()
    try:
        conexion = mysql.connector.connect(
            host = contenido,
            user ="root",
            password ="",  
            database ="valmo",
            port =3306
        )
                
        if conexion.is_connected():
            cursor = conexion.cursor()
            mysql_value = 1
            conexion_est = True
            
            print("Conexion establecida")
        else:
            mysql_value = 0
            conexion_est = False
    except Exception as e:
        mysql_value = 0
        conexion = False
        cursor = False
        conexion_est = False
        print("Sin conexion")
    return conexion, cursor, conexion_est

def evento():
    conexion, cursor, conexion_est = conexion_MySQL()
    try:
        if conexion_est  == True:
            cursor.execute("""SELECT Productos, Recetas, MateriaPrima from Aplicacion_tbleventosvalmosys where ID = 1""")
            rows = cursor.fetchall()
            for row in rows:
                Productos = row[0]
                Recetas = row[1]
                MateriaPrima = row[2]
                
                if Productos == 1:
                    productosMysql()
                elif Recetas == 1:
                    recetasMysql()
                elif MateriaPrima == 1:
                    materiaPrimaMysql()
                print(Productos, Recetas, MateriaPrima)      
        else:
            print("Error")
        validacionTablasProductos()
        validacionTablasMateriaPrima()
    except Exception as e:
        print("Error: ", e)


# ------------------------------------------------------------------CREAR RESPALDO DE SQLITE3 A MYSQL------------------------------------------------------------------
def materiaPrimaMovimientosSQLite(id_tabla):
    conexionSQL, cursorSQL = conexion_SQLite3()
    # Conectar a la base de datos MySQL
    conexion, cursor, conexion_est = conexion_MySQL()

    try:

        # aqui validamos que las columnas de SQLite3 sean mayores a las columnas de MYSQL
        cursorSQL = conexionSQL.execute("""SELECT ID, Fecha, IDMP, Cantidad, ReFolioProd FROM tblMPMovimientos WHERE Enviado = 0""")
        rows = cursorSQL.fetchall()
        for row in rows:
            id_tabla += 1
            Idfolio = 'P-{:06d}'.format(id_tabla)
            Fecha = row[1]
            Idmp = row[2]
            cantidad = row[3]
            reFolioprod = row[4]
            notas = ""
            almacen = 3
            cliente = 48
            presentacion = 2
            try:
                # insertamos en las tablas de mysql
                cursor.execute("""
                    INSERT INTO Aplicacion_tblsalidamp (ID, IDFolio, cantidad, referencia, fecha, notas, IDAlmacen_id, IDCliente_id, IDMateriaPrima_id, IDPresentacion_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (id_tabla, Idfolio, cantidad, reFolioprod, Fecha, notas, almacen, cliente, Idmp, presentacion ))
                # Confirmar los cambio
                conexion.commit()

                print("movimientos de materia prima insertado en entrada salida materia prima exitosamente")
                cursorSQL = conexionSQL.execute("""UPDATE tblMPMovimientos SET Enviado = 1 WHERE Enviado = 0 """)
                conexionSQL.commit() 
            except mysql.connector.Error as e:
                print("Error al actualizar registros en MySQL:", e)
                conexion.rollback()
                
    except mysql.connector.Error as e:
        print("Error en la consulta corral seleccionado:", e)
        return []
    finally:
        cursorSQL.close()
        conexionSQL.close()
        cursor.close()
        conexion.close()
        
def productosMovimientosSQLite(id_tabla):
    conexionSQL, cursorSQL = conexion_SQLite3()
    # Conectar a la base de datos MySQL
    conexion, cursor, conexion_est = conexion_MySQL()
    try:
        # aqui validamos que las columnas de SQLite3 sean mayores a las columnas de MYSQL
        cursorSQL = conexionSQL.execute("""SELECT ID, RefFolioProd, Fecha, TipoMov, IDProd, Cant, Notas from tblProductoMovimientos WHERE Enviado = 0""")
        rows = cursorSQL.fetchall()
        for row in rows:
            id_tabla += 1
            Idfolio = 'P-{:06d}'.format(id_tabla)
            cantidad = row[5]
            Referencia = row[1]
            Fecha = row[2]
            notas = row[6]
            almacen = 3
            presentacion = 2
            idproducto = row[4]
            proveedor = 34
            tipoMov = row[3]
            try:
                # insertamos en las tablas de mysql
                cursor.execute("""
                    INSERT INTO Aplicacion_tblentradaproductos (ID, IDFolio, cantidad, referencia, fecha, notas, IDAlmacen_id, IDPresentacion_id, IDProductos_id, IDProveedor_id, IDTipoMov_id ) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, (id_tabla, Idfolio, cantidad, Referencia, Fecha, notas, almacen, presentacion, idproducto, proveedor, tipoMov))
                # Confirmar los cambio
                conexion.commit()
                
                print("movimientos de procuctos insertado en entrada productos exitosamente")
                cursorSQL = conexionSQL.execute("""UPDATE tblProductoMovimientos SET Enviado = 1 WHERE Enviado = 0""")
                conexionSQL.commit() 
            except mysql.connector.Error as e:
                print("Error al actualizar registros en MySQL:", e)
                conexion.rollback()
                
    except mysql.connector.Error as e:
        print("Error en la consulta corral seleccionado:", e)
        return []
    finally:
        cursorSQL.close()
        conexionSQL.close()
        
# ---------------------------------------------------------------CREAR UN RESPALDO DE MYSQL A SQLITE3---------------------------------------------------------------
def productosMysql():
    conexion, cursor, conexion_est = conexion_MySQL()
    try:
        if conexion_est  == True:
            cursor.execute("""SELECT ID, Clave, Descripcion, IDEstatus_id, IDUnidadMedida_id, PrecioUnitario from Aplicacion_tblproductos""")
            rows = cursor.fetchall()

            conexionSQL, cursorSQL = conexion_SQLite3()
            for row in rows:
                # Obtener el ID de la fila actual
                id = row[0]
                clave = row[1]
                descripcion = row[2]
                if row[3] == 1:
                    estatus = "Activo"
                else:
                    estatus = "Baja"
                if row[4] == 1:
                    unidad = "KG"
                elif row[4] == 2:
                    unidad = "Paca"
                else:
                    unidad = ""
                preciounidad = row[5]
                
                print(id, clave, descripcion, estatus, unidad, preciounidad)      
                try:
                    cursorSQL = conexionSQL.execute("""UPDATE tblProductos SET Clave = ?, Descripcion = ?, UdeM = ?, IDTipoStatus = ? WHERE ID = ? """, (clave, descripcion, unidad, estatus, id, ))
                    conexionSQL.commit() 
                    cursor.execute("""UPDATE Aplicacion_tbleventosvalmosys SET Productos = 0 WHERE ID = 1""")
                    conexion.commit()
                except sqlite3.IntegrityError as e:
                    if "UNIQUE constraint failed: Aplicacion_tblcorrales.ID" in str(e):
                        print("Error: Violación de restricción única. El ID ya existe en la tabla.")
                    else:
                        print("Error al ejecutar la consulta corrales listos:", e)
        else:
            print("Error")
    except Exception as e:
        print("Error: ", e)
        
def materiaPrimaMysql():
    conexion, cursor, conexion_est = conexion_MySQL()
    try:
        if conexion_est  == True:
            cursor.execute("""SELECT ID, Clave, Descripcion, IDEstatus_id, IDUnidadMedida_id from Aplicacion_tblmateriaprima""")
            rows = cursor.fetchall()

            conexionSQL, cursorSQL = conexion_SQLite3()
            for row in rows:
                # Obtener el ID de la fila actual
                id = row[0]
                clave = row[1]
                descripcion = row[2]
                if row[3] == 1:
                    estatus = "Activo"
                else:
                    estatus = "Baja "
                if row[4] == 1:
                    unidad = "Kg"
                else:
                    unidad = ""
                
                print(id, clave, descripcion, estatus, unidad)      
                try:
                    cursorSQL = conexionSQL.execute("""UPDATE tblMateriaPrima SET Clave = ?, Descripcion = ?, IDUnidadMedida = ?, IDTipoStatus = ? WHERE ID = ? """, (clave, descripcion, unidad, estatus, id, ))
                    conexionSQL.commit() 
                    cursor.execute("""UPDATE Aplicacion_tbleventosvalmosys SET MateriaPrima = 0 WHERE ID = 1""")
                    conexion.commit()
                except sqlite3.IntegrityError as e:
                    if "UNIQUE constraint failed: Aplicacion_tblcorrales.ID" in str(e):
                        print("Error: Violación de restricción única. El ID ya existe en la tabla.")
                    else:
                        print("Error al ejecutar la consulta corrales listos:", e)
        else:
            print("Error")
    except Exception as e:
        print("Error: ", e)

def recetasMysql():
    conexion, cursor, conexion_est = conexion_MySQL()
    try:
        if conexion_est  == True:
            cursor.execute("""SELECT ID, IDMateriaPrima_id, IDProductos_id, Porcentaje, Merma from Aplicacion_tblproductosmateriaprima""")
            rows = cursor.fetchall()

            conexionSQL, cursorSQL = conexion_SQLite3()
            for row in rows:
                # Obtener el ID de la fila actual
                id = row[0]
                materiaprima = row[1]
                productos = row[2]
                porcentaje = row[3]
                merma = row[4]
                
                print(id, materiaprima, productos, porcentaje, merma)      
                try:
                    cursorSQL = conexionSQL.execute("""UPDATE tblProductoReceta SET IDMateriaPrima = ?, Porcentaje = ?, PorMerma = ?, IDProd = ? WHERE ID = ? """, (materiaprima, porcentaje, merma, productos, id, ))
                    conexionSQL.commit() 
                    cursor.execute("""UPDATE Aplicacion_tbleventosvalmosys SET Recetas = 0 WHERE ID = 1""")
                    conexion.commit()
                except sqlite3.IntegrityError as e:
                    if "UNIQUE constraint failed: Aplicacion_tblcorrales.ID" in str(e):
                        print("Error: Violación de restricción única. El ID ya existe en la tabla.")
                    else:
                        print("Error al ejecutar la consulta corrales listos:", e)
        else:
            print("Error")
    except Exception as e:
        print("Error: ", e)

# en esta funcion valida los registros de ambas base de datos, si la de sqlite3 es mayor a la de mysql, se hace una insercion con los datos nuevos
def validacionTablasProductos():
    conexionSQL, cursorSQL = conexion_SQLite3()
    # MOVIMIENTO DE PRODUCTOS EN MYSQL
    
    cursorSQL = conexionSQL.execute("""SELECT ID from tblProductoMovimientos WHERE Enviado = 0""")
    filas = cursorSQL.fetchall()
    if filas :
        conexion, cursor, conexion_est = conexion_MySQL()
        cursor.execute("""SELECT ID from Aplicacion_tblentradaproductos ORDER BY ID DESC LIMIT 1""")
        row = cursor.fetchone()

        # Verificar si se obtuvo un resultado y asignar el ID apropiadamente
        if row is None:
            id_tabla = 0
        else:
            id_tabla = row[0]

        # Imprimir el ID de la materia prima
        print("id materia prima= ", id_tabla)
        productosMovimientosSQLite(id_tabla)
        print("La consulta tiene registros.")
    else:

        print("La consulta no tiene registros.")
        
# en esta funcion valida los registros de ambas base de datos, si la de sqlite3 es mayor a la de mysql, se hace una insercion con los datos nuevos
def validacionTablasMateriaPrima():
    conexionSQL, cursorSQL = conexion_SQLite3()
    # MOVIMIENTO DE PRODUCTOS EN MYSQL
    
    cursorSQL = conexionSQL.execute("""SELECT ID from tblMPMovimientos WHERE Enviado = 0""")
    filas = cursorSQL.fetchall()
    if filas :
        conexion, cursor, conexion_est = conexion_MySQL()
        cursor.execute("""SELECT ID from Aplicacion_tblsalidamp ORDER BY ID DESC LIMIT 1""")
        row = cursor.fetchone()

        # Verificar si se obtuvo un resultado y asignar el ID apropiadamente
        if row is None:
            id_tabla = 0
        else:
            id_tabla = row[0]

        # Imprimir el ID de la materia prima
        print("id materia prima= ", id_tabla)
        materiaPrimaMovimientosSQLite(id_tabla)
        print("La consulta tiene registros.")
    else:

        print("La consulta no tiene registros.")