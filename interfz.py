import flet as ft
from crud_connector import (
    insertar_articulo, insertar_cliente, insertar_empleado, leer_articulos, 
    leer_clientes, leer_empleados, eliminar_articulo, eliminar_cliente, 
    eliminar_empleado, actualizar_articulo, actualizar_cliente, actualizar_empleado,
    insertar_categoria, leer_categorias, actualizar_categoria, eliminar_categoria
)
# Variables globales para inputs
data_fields = []
tabla_actual = None

def limpiar_contenido(page):
    page.controls.clear()
    page.update()

def crear_formulario(page, tabla):
    limpiar_contenido(page)

    global data_fields, tabla_actual
    data_fields.clear()
    tabla_actual = tabla

    titulo = ft.Text(f"Formulario: {tabla.capitalize()}", size=24, weight="bold")
    page.controls.append(titulo)

    campos = []

    if tabla == "articulos":
        etiquetas = ["Código", "Nombre", "Precio", "Costo", "Existencia", "Unidad", "Descripción", "ID Categoría"]
    elif tabla == "clientes":
        etiquetas = ["ID Cliente", "Teléfono", "Nombre", "Dirección", "RFC", "Correo"]
    elif tabla == "empleados":
        etiquetas = ["ID Empleado", "Nombre", "Cargo", "Teléfono", "Correo"]
    elif tabla == "categorias":
        etiquetas = ["ID Categoría", "Nombre"]

    for etiqueta in etiquetas:
        campo = ft.TextField(label=etiqueta)
        campos.append(campo)
        page.controls.append(campo)

    data_fields.extend(campos)

    botones_crud = ft.Row([
        ft.ElevatedButton("Insertar", on_click=lambda e: finalizar_formulario()),
        ft.ElevatedButton("Leer", on_click=lambda e: leer_datos(page)),
        ft.ElevatedButton("Actualizar", on_click=lambda e: actualizar_registro()),
        ft.ElevatedButton("Eliminar", on_click=lambda e: eliminar_registro())
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    botones_finales = ft.Row([
        ft.ElevatedButton("Cancelar", on_click=lambda e: cancelar_formulario(page)),
        ft.ElevatedButton("Regresar", on_click=lambda e: menu_principal(page))
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    page.controls.append(ft.Divider())
    page.controls.append(botones_crud)
    page.controls.append(botones_finales)
    page.update()

def finalizar_formulario():
    valores = [campo.value for campo in data_fields]
    if tabla_actual == "articulos":
        insertar_articulo(*valores)
    elif tabla_actual == "clientes":
        insertar_cliente(*valores[1:])  # Ignora ID en insercion
    elif tabla_actual == "empleados":
        insertar_empleado(*valores[1:]) 
    elif tabla_actual == "categorias":
        insertar_categoria(valores[1]) 

def actualizar_registro():
    valores = [campo.value for campo in data_fields]
    
    if tabla_actual == "articulos":
        # Asegúrate de que la lista de valores se pase en el orden correcto
        actualizar_articulo(*valores)
    elif tabla_actual == "clientes":
        # El ID del cliente debe ser el primer valor en la lista
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

    page.controls.append(ft.Text(f"Registros de {tabla_actual.capitalize()}", size=20, weight="bold"))

    for fila in resultados:
        page.controls.append(ft.Text(str(fila)))

    page.controls.append(ft.ElevatedButton("Regresar", on_click=lambda e: crear_formulario(page, tabla_actual)))
    page.update()

def cancelar_formulario(page):
    for campo in data_fields:
        campo.value = ""
    page.update()

def menu_principal(page):
    limpiar_contenido(page)
    
    titulo_principal = ft.Text("Tienda del Sol", size=30, weight="bold", text_align=ft.TextAlign.CENTER)
    page.controls.append(titulo_principal)
    page.controls.append(
        ft.Row([
            ft.ElevatedButton("Articulos", on_click=lambda e: crear_formulario(page, "articulos")),
            ft.ElevatedButton("Clientes", on_click=lambda e: crear_formulario(page, "clientes")),
            ft.ElevatedButton("Empleados", on_click=lambda e: crear_formulario(page, "empleados")),
            ft.ElevatedButton("Categorias", on_click=lambda e: crear_formulario(page, "categorias"))
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
    )
    page.update()


def main(page: ft.Page):
    page.title = "CRUD Tienda del Sol"
    page.window_width = 600
    page.window_height = 600
    menu_principal(page)

ft.app(target=main)

