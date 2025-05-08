import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql", # cambiar en caso que no sea su contraseña
        database="tiendadelsol"
    )
# CRUD articulos
def insertar_articulo(codigo, nombre, precio, costo, existencia, unidad, descripcion, id_categoria):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO articulos (codigo, nombre, precio, costo, existencia, unidad, descripcion, id_categoria)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (codigo, nombre, precio, costo, existencia, unidad, descripcion, id_categoria))
    con.commit()
    con.close()

def leer_articulos():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articulos")
    resultados = cursor.fetchall()
    con.close()
    return resultados

def actualizar_articulo(codigo, nombre, precio, costo, existencia, unidad, descripcion, id_categoria):
    con = conectar()
    cursor = con.cursor()
    query = """UPDATE articulos 
               SET nombre = %s, precio = %s, costo = %s, existencia = %s, unidad = %s, descripcion = %s, id_categoria = %s 
               WHERE codigo = %s"""
    cursor.execute(query, (nombre, precio, costo, existencia, unidad, descripcion, id_categoria, codigo))
    con.commit()
    con.close()

def eliminar_articulo(codigo):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM articulos WHERE codigo = %s", (codigo,))
    con.commit()
    con.close()

# CRUD clientes
def insertar_cliente(telefono, nombre, direccion, rfc, correo):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO clientes (telefono, nombre, direccion, rfc, correo)
        VALUES (%s, %s, %s, %s, %s)
    """, (telefono, nombre, direccion, rfc, correo))
    con.commit()
    con.close()

def leer_clientes():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    resultados = cursor.fetchall()
    con.close()
    return resultados

def actualizar_cliente(id_cliente, telefono, nombre, direccion, rfc, correo):
    con = conectar()
    cursor = con.cursor()
    query = """UPDATE clientes 
               SET telefono = %s, nombre = %s, direccion = %s, rfc = %s, correo = %s 
               WHERE id_cliente = %s"""
    cursor.execute(query, (telefono, nombre, direccion, rfc, correo, id_cliente))
    con.commit()
    con.close()

def eliminar_cliente(id_cliente):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
    con.commit()
    con.close()

# CRUD empleado
def insertar_empleado(nombre, cargo, telefono, correo):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO empleados (nombre, cargo, telefono, correo)
        VALUES (%s, %s, %s, %s)
    """, (nombre, cargo, telefono, correo))
    con.commit()
    con.close()

def leer_empleados():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM empleados")
    resultados = cursor.fetchall()
    con.close()
    return resultados

def actualizar_empleado(id_empleado, nombre, cargo, telefono, correo):
    con = conectar()
    cursor = con.cursor()
    query = """UPDATE empleados 
               SET nombre = %s, cargo = %s, telefono = %s, correo = %s 
               WHERE id_empleado = %s"""
    cursor.execute(query, (nombre, cargo, telefono, correo, id_empleado))
    con.commit()
    con.close()

def eliminar_empleado(id_empleado):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM empleados WHERE id_empleado = %s", (id_empleado,))
    con.commit()
    con.close()

def insertar_categoria(nombre):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre,))
    con.commit()
    con.close()

def leer_categorias():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categorias")
    resultados = cursor.fetchall()
    con.close()
    return resultados

def actualizar_categoria(id_categoria, nombre):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("UPDATE categorias SET nombre = %s WHERE id_categoria = %s", (nombre, id_categoria))
    con.commit()
    con.close()

def eliminar_categoria(id_categoria):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM categorias WHERE id_categoria = %s", (id_categoria,))
    con.commit()
    con.close()

#crud venta 
def insertar_venta(id_cliente):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("INSERT INTO ventas (id_cliente) VALUES (%s)", (id_cliente,))
    con.commit()
    id_venta = cursor.lastrowid
    con.close()
    return id_venta

def insertar_detalle_venta(id_venta, codigo_articulo, cantidad, precio_venta):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO detalle_ventas (id_venta, codigo_articulo, cantidad, precio_venta)
        VALUES (%s, %s, %s, %s)
    """, (id_venta, codigo_articulo, cantidad, precio_venta))
    con.commit()
    con.close()

def actualizar_existencia_articulo(codigo_articulo, nueva_existencia):
    con = conectar()
    cursor = con.cursor(dictionary=True)

    # Leer todos los campos actuales del artículo
    cursor.execute("SELECT * FROM articulos WHERE codigo = %s", (codigo_articulo,))
    art = cursor.fetchone()

    if not art:
        con.close()
        raise Exception("Artículo no encontrado.")

    # Actualizar manteniendo todos los campos, solo cambiando existencia
    query = """
        UPDATE articulos
        SET nombre = %s, precio = %s, costo = %s, existencia = %s,
            unidad = %s, descripcion = %s, id_categoria = %s
        WHERE codigo = %s
    """
    cursor.execute(query, (
        art["nombre"],
        art["precio"],
        art["costo"],
        nueva_existencia,
        art["unidad"],
        art["descripcion"],
        art["id_categoria"],
        codigo_articulo
    ))
    con.commit()
    con.close()

