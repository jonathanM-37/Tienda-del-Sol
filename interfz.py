import flet as ft
import os
import shutil
from crud_connector import (
    insertar_articulo, insertar_cliente, insertar_empleado, leer_articulos, 
    leer_clientes, leer_empleados, eliminar_articulo, eliminar_cliente, 
    eliminar_empleado, actualizar_articulo, actualizar_cliente, actualizar_empleado,
    insertar_categoria, leer_categorias, actualizar_categoria, eliminar_categoria,
    insertar_venta, insertar_detalle_venta, actualizar_existencia_articulo 
)
data_fields = []
tabla_actual = None
imagen_subida = None

def limpiar_contenido(page):
    page.controls.clear()
    page.update()

def crear_formulario(page, tabla):
    limpiar_contenido(page)

    global data_fields, tabla_actual
    data_fields.clear()
    tabla_actual = tabla

    titulo = ft.Text(f"Formulario: {tabla.capitalize()}", size=24, weight="bold")

    if tabla == "articulos":
        etiquetas = ["Código", "Nombre", "Precio", "Costo", "Existencia", "Unidad", "Descripción", "ID Categoría"]
    elif tabla == "clientes":
        etiquetas = ["ID Cliente", "Teléfono", "Nombre", "Dirección", "RFC", "Correo"]
    elif tabla == "empleados":
        etiquetas = ["ID Empleado", "Nombre", "Cargo", "Teléfono", "Correo"]
    elif tabla == "categorias":
        etiquetas = ["ID Categoría", "Nombre"]

    mitad = len(etiquetas) // 2 + len(etiquetas) % 2
    campos_col1 = []
    campos_col2 = []

    for i, etiqueta in enumerate(etiquetas):
        campo = ft.TextField(label=etiqueta, width=400)
        if i < mitad:
            campos_col1.append(campo)
        else:
            campos_col2.append(campo)
        data_fields.append(campo)

    formulario_filas = ft.Row([
        ft.Column(campos_col1, spacing=10),
        ft.Column(campos_col2, spacing=10)
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

    botones_crud = ft.Row([
        ft.ElevatedButton("Insertar", on_click=lambda e: finalizar_formulario()),
        ft.ElevatedButton("Leer", on_click=lambda e: leer_datos(page)),
        ft.ElevatedButton("Actualizar", on_click=lambda e: actualizar_registro()),
        ft.ElevatedButton("Eliminar", on_click=lambda e: eliminar_registro())
    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)

    botones_finales = ft.Row([
        ft.ElevatedButton("Cancelar", on_click=lambda e: cancelar_formulario(page)),
        ft.ElevatedButton("Regresar", on_click=lambda e: mostrar_botones_registro(page))
    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)

    scrollable_view = ft.Column([
        titulo,
        formulario_filas,
        ft.Divider(),
        botones_crud,
        botones_finales
    ], spacing=20, scroll=ft.ScrollMode.AUTO)

    page.controls.append(scrollable_view)
    page.update()

def finalizar_formulario():
    valores = [campo.value for campo in data_fields]
    if tabla_actual == "articulos":
        insertar_articulo(*valores)
    elif tabla_actual == "clientes":
        insertar_cliente(*valores[1:])  
    elif tabla_actual == "empleados":
        insertar_empleado(*valores[1:]) 
    elif tabla_actual == "categorias":
        insertar_categoria(valores[1]) 

def actualizar_registro():
    valores = [campo.value for campo in data_fields]
    
    if tabla_actual == "articulos":
        actualizar_articulo(*valores)
    elif tabla_actual == "clientes":
        actualizar_cliente(valores[0], *valores[1:])
    elif tabla_actual == "empleados":
        actualizar_empleado(valores[0], *valores[1:])
    elif tabla_actual == "categorias":
        actualizar_categoria(valores[0], valores[1])

def eliminar_registro():
    pk = data_fields[0].value
    if tabla_actual == "articulos":
        eliminar_articulo(pk)
    elif tabla_actual == "clientes":
        eliminar_cliente(pk)
    elif tabla_actual == "empleados":
        eliminar_empleado(pk)
    elif tabla_actual == "categorias":
        eliminar_categoria(pk)

def leer_datos(page):
    limpiar_contenido(page)

    resultados = []
    if tabla_actual == "articulos":
        resultados = leer_articulos()
    elif tabla_actual == "clientes":
        resultados = leer_clientes()
    elif tabla_actual == "empleados":
        resultados = leer_empleados()
    elif tabla_actual == "categorias":
        resultados = leer_categorias()

    elementos = [ft.Text(f"Registros de {tabla_actual.capitalize()}", size=20, weight="bold")]

    for fila in resultados:
        elementos.append(ft.Text(str(fila)))

    elementos.append(ft.ElevatedButton("Regresar", on_click=lambda e: crear_formulario(page, tabla_actual)))

    page.controls.append(
        ft.Column(elementos, scroll=ft.ScrollMode.AUTO, spacing=10)
    )
    page.update()

def cancelar_formulario(page):
    for campo in data_fields:
        campo.value = ""
    page.update()

def mostrar_botones_registro(page):
    limpiar_contenido(page)
    page.controls.append(
        ft.Column([
            ft.Text("Registros disponibles", size=24, weight="bold"),
            ft.Row([
                ft.ElevatedButton("Clientes", on_click=lambda e: crear_formulario(page, "clientes")),
                ft.ElevatedButton("Categorías", on_click=lambda e: crear_formulario(page, "categorias")),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ft.Row([
                ft.ElevatedButton("Empleados", on_click=lambda e: crear_formulario(page, "empleados")),
                ft.ElevatedButton("Artículos", on_click=lambda e: crear_formulario(page, "articulos")),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ft.ElevatedButton("Regresar", on_click=lambda e: menu_principal(page))
        ], spacing=20)
    )
    page.update()
    
def menu_principal(page):
    limpiar_contenido(page)
    columna_izquierda = ft.Column([
        ft.Text("Tienda del Sol", size=70, weight="bold", text_align=ft.TextAlign.CENTER),
        ft.ElevatedButton("Registros", on_click=lambda e: mostrar_botones_registro(page)),
        ft.ElevatedButton("Compras", on_click=lambda e: pantalla_compras(page))
    ], spacing=20, alignment=ft.MainAxisAlignment.START)

    imagen_derecha = ft.Image(
        #-----> cambiar la ruta
        src="C/su/ruta/propia//tiendadelsol/imagenes/sol.jpeg",  
        width=450,
        height=450,
        fit=ft.ImageFit.CONTAIN
    )
    try:
        articulos = leer_articulos()
    except:
        articulos = []

    encabezados = ["Código", "Nombre", "Precio", "Costo", "Existencia", "Unidad", "Descripción", "ID Categoría"]
    columnas = [ft.DataColumn(ft.Text(col)) for col in encabezados]

    filas = []
    for art in articulos:
        fila = ft.DataRow([
            ft.DataCell(ft.Text(str(art.get("codigo", "")))),
            ft.DataCell(ft.Text(str(art.get("nombre", "")))),
            ft.DataCell(ft.Text(str(art.get("precio", "")))),
            ft.DataCell(ft.Text(str(art.get("costo", "")))),
            ft.DataCell(ft.Text(str(art.get("existencia", "")))),
            ft.DataCell(ft.Text(str(art.get("unidad", "")))),
            ft.DataCell(ft.Text(str(art.get("descripcion", "")))),
            ft.DataCell(ft.Text(str(art.get("id_categoria", ""))))
        ])
        filas.append(fila)
    tabla_articulos = ft.DataTable(columns=columnas, rows=filas)

    page.controls.append(
    ft.Container(
        content=ft.Column([
            ft.Row([columna_izquierda, imagen_derecha], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ft.Divider(),
            ft.Text("Productos", size=20, weight="bold"),
            tabla_articulos
        ], scroll=ft.ScrollMode.AUTO),
        height=500 
    )
)

    page.update()

def pantalla_compras(page):
    limpiar_contenido(page)

    clientes = leer_clientes()
    opciones_clientes = [
        ft.dropdown.Option(f"{cliente['id_cliente']} - {cliente['nombre']}")
        for cliente in clientes
    ]
    dropdown_clientes = ft.Dropdown(
        label="Seleccionar cliente",
        options=opciones_clientes,
        width=400
    )
    campo_busqueda = ft.TextField(label="Buscar artículo por código o nombre", width=400)
    tabla_resultados = ft.Column()

    def buscar_articulo(e):
        termino = campo_busqueda.value.lower()
        articulos = leer_articulos()
        resultados = []

        for art in articulos:
            if termino in str(art.get("codigo", "")).lower() or termino in str(art.get("nombre", "")).lower():
                resultados.append(art)

        tabla_resultados.controls.clear()

        if resultados:
            for art in resultados:
                cantidad_field = ft.TextField(label="Cantidad", width=100)

                def realizar_venta(evt, art=art, cantidad_field=cantidad_field):
                    seleccion = dropdown_clientes.value
                    if not seleccion:
                        page.dialog = ft.AlertDialog(title=ft.Text("Seleccione un cliente"))
                        page.dialog.open = True
                        page.update()
                        return

                    id_cliente = int(seleccion.split(" - ")[0])
                    try:
                        cantidad = int(cantidad_field.value)
                        existencia = int(art["existencia"])
                        if cantidad <= 0 or cantidad > existencia:
                            raise ValueError
                    except:
                        page.dialog = ft.AlertDialog(title=ft.Text("Cantidad inválida o excede existencia"))
                        page.dialog.open = True
                        page.update()
                        return

                    id_venta = insertar_venta(id_cliente)
                    insertar_detalle_venta(id_venta, art["codigo"], cantidad, art["precio"])
                    nueva_existencia = existencia - cantidad
                    actualizar_existencia_articulo(art["codigo"], nueva_existencia)

                    page.dialog = ft.AlertDialog(title=ft.Text("Venta registrada exitosamente"))
                    page.dialog.open = True
                    page.update()

                fila = ft.Row([
                    ft.Text(f"{art['codigo']} - {art['nombre']} | ${art['precio']} | Stock: {art['existencia']}"),
                    cantidad_field,
                    ft.ElevatedButton("Vender", on_click=lambda evt, a=art, c=cantidad_field: realizar_venta(evt, a, c))
                ])
                tabla_resultados.controls.append(fila)
        else:
            tabla_resultados.controls.append(ft.Text("No se encontraron artículos."))

        page.update()
  
    boton_buscar = ft.ElevatedButton("Buscar artículo", on_click=buscar_articulo)

    boton_regresar = ft.ElevatedButton("Regresar", on_click=lambda e: menu_principal(page))

    # Vista principal
    page.controls.append(
        ft.Column([
            ft.Text("Módulo de Compras", size=24, weight="bold"),
            dropdown_clientes,
            campo_busqueda,
            boton_buscar,
            ft.Divider(),
            ft.Text("Resultados de artículos:", size=18, weight="bold"),
            tabla_resultados,
            ft.Divider(),
            boton_regresar
        ], spacing=20, scroll=ft.ScrollMode.AUTO)
    )

    page.update()


def main(page: ft.Page):
    page.title = "CRUD Tienda del Sol"
    page.window_width = 1000
    page.window_height = 800
    page.bgcolor = ft.colors.BLACK
    page.theme_mode = ft.ThemeMode.DARK
    menu_principal(page)


if __name__ == "__main__":
    ft.app(target=main)

