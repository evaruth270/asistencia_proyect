import requests
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime, timedelta
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

# Función para crear la base de datos y la tabla personas
def crear_base_de_datos():
    conexion = sqlite3.connect('nueva_base_de_datos.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido_paterno TEXT,
            apellido_materno TEXT,
            dni TEXT UNIQUE,
            lugar_procedencia TEXT,
            fecha TEXT,
            hora TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

# Función para guardar personas en la base de datos
def guardar_persona(nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia):
    if not verificar_existencia_dni(dni):
        conexion = sqlite3.connect('nueva_base_de_datos.db')
        cursor = conexion.cursor()
        fecha = datetime.now().strftime('%Y-%m-%d')
        hora = datetime.now().strftime('%H:%M:%S')
        cursor.execute('''
            INSERT INTO personas (nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia, fecha, hora) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia, fecha, hora))
        conexion.commit()
        conexion.close()
    else:
        messagebox.showerror("Error", "El DNI ya está registrado.")

# Función para actualizar personas en la base de datos
def actualizar_persona(id, nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia):
    conexion = sqlite3.connect('nueva_base_de_datos.db')
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE personas
        SET nombre = ?, apellido_paterno = ?, apellido_materno = ?, dni = ?, lugar_procedencia = ?
        WHERE id = ?
    ''', (nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia, id))
    conexion.commit()
    conexion.close()

# Función para buscar personas en la base de datos
def obtener_personas(filtro=None):
    conexion = sqlite3.connect('nueva_base_de_datos.db')
    cursor = conexion.cursor()
    if filtro:
        cursor.execute(filtro)
    else:
        cursor.execute('SELECT * FROM personas')
    personas = cursor.fetchall()
    conexion.close()
    return personas

# Función para verificar si un DNI ya está registrado en la base de datos
def verificar_existencia_dni(dni):
    conexion = sqlite3.connect('nueva_base_de_datos.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM personas WHERE dni = ?', (dni,))
    existe = cursor.fetchone()
    conexion.close()
    return existe is not None

<<<<<<< HEAD







# Función para mostrar los datos consultados y permitir guardar
def consultar_y_mostrar_datos():
    dni = dni_entry.get()
    if not dni or len(dni) != 8 or not dni.isdigit():
        messagebox.showerror("Error", "Ingrese un DNI válido de 8 dígitos.")
        return

    if verificar_existencia_dni(dni):
        messagebox.showerror("Error", "El DNI ya está registrado.")
        return

    global datos_persona
    datos_persona = consultar_persona_por_dni(dni)
    if datos_persona:
        nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia = datos_persona
        info = f"Nombre Completo: {nombre} {apellido_paterno} {apellido_materno}\nDNI: {dni}\nLugar de Procedencia: {lugar_procedencia}"
        datos_consultados_label.config(text=info)
        boton_guardar.config(state=tk.NORMAL)  # Habilitar el botón de guardar
    else:
        datos_consultados_label.config(text="No se pudo obtener datos de la persona. Ingrese los datos manualmente.")
        abrir_formulario_manual(dni)
        boton_guardar.config(state=tk.DISABLED)  # Deshabilitar el botón de guardar

# Función para guardar los datos consultados
def guardar_datos():
    global datos_persona
    if datos_persona:
        nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia = datos_persona
        guardar_persona(nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia)
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        boton_guardar.config(state=tk.DISABLED)  # Deshabilitar el botón de guardar
        actualizar_lista_personas()
        datos_consultados_label.config(text="")

# Función para actualizar la lista de personas guardadas
def actualizar_lista_personas():
    personas = obtener_personas()
    lista_personas.delete(0, tk.END)
    if personas:
        for persona in personas:
            info = f"ID: {persona[0]} - {persona[1]} {persona[2]} {persona[3]}, DNI: {persona[4]}, {persona[5]}, {persona[6]}, {persona[7]}"
            lista_personas.insert(tk.END, info)
    else:
        lista_personas.insert(tk.END, "No hay personas guardadas.")

# Función para exportar datos a Excel
def exportar_excel(personas, tipo):
    df = pd.DataFrame(personas, columns=["ID", "Nombre", "Apellido Paterno", "Apellido Materno", "DNI", "Lugar Procedencia", "Fecha", "Hora"])
    df.to_excel(f"reporte_{tipo}.xlsx", index=False)
    messagebox.showinfo("Exportar a Excel", f"Reporte {tipo} exportado a Excel exitosamente.")

# Función para exportar datos a PDF
def exportar_pdf(personas, tipo):
    c = canvas.Canvas(f"reporte_{tipo}.pdf", pagesize=letter)
    width, height = letter
    c.drawString(100, height - 40, f"Reporte {tipo.capitalize()}")
    c.drawString(100, height - 60, "ID   DNI        Apellido Paterno   Apellido Materno   Nombre   Fecha       Hora")

    y = height - 80
    for persona in personas:
        c.drawString(100, y, f"{persona[0]}   {persona[4]}   {persona[2]}   {persona[3]}   {persona[1]}   {persona[6]}   {persona[7]}")
        y -= 20

    c.save()
    messagebox.showinfo("Exportar a PDF", f"Reporte {tipo} exportado a PDF exitosamente.")

# Función para generar reportes
def generar_reporte(tipo):
    hoy = datetime.now().date()
    filtro = ""
    if tipo == "diario":
        filtro = f"SELECT * FROM personas WHERE fecha = '{hoy}'"
    elif tipo == "semanal":
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        filtro = f"SELECT * FROM personas WHERE fecha BETWEEN '{inicio_semana}' AND '{hoy}'"
    elif tipo == "mensual":
        inicio_mes = hoy.replace(day=1)
        filtro = f"SELECT * FROM personas WHERE fecha BETWEEN '{inicio_mes}' AND '{hoy}'"

    personas = obtener_personas(filtro)
    reporte_window = tk.Toplevel()
    reporte_window.title(f"Reporte {tipo.capitalize()}")
    reporte_window.geometry("700x400")

    columns = ("ID", "DNI", "Apellido Paterno", "Apellido Materno", "Nombre", "Fecha", "Hora")
    tree = ttk.Treeview(reporte_window, columns=columns, show='headings')
    tree.heading("ID", text="ID")
    tree.heading("DNI", text="DNI")
    tree.heading("Apellido Paterno", text="Apellido Paterno")
    tree.heading("Apellido Materno", text="Apellido Materno")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Hora", text="Hora")

    for persona in personas:
        tree.insert("", tk.END, values=(persona[0], persona[4], persona[2], persona[3], persona[1], persona[6], persona[7]))

    tree.pack(fill=tk.BOTH, expand=True)

    ttk.Button(reporte_window, text="Exportar a Excel", command=lambda: exportar_excel(personas, tipo)).pack(side=tk.LEFT, padx=10, pady=10)
    ttk.Button(reporte_window, text="Exportar a PDF", command=lambda: exportar_pdf(personas, tipo)).pack(side=tk.LEFT, padx=10, pady=10)

# Función para cargar datos desde un archivo Excel y mostrar vista previa
def cargar_datos_desde_excel():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de Excel", "*.xlsx")])
    if archivo:
        df = pd.read_excel(archivo)
        preview_window = tk.Toplevel()
        preview_window.title("Vista Previa de Datos")
        preview_window.geometry("700x400")

        columns = df.columns.tolist()
        tree = ttk.Treeview(preview_window, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)

        for _, row in df.iterrows():
            tree.insert("", tk.END, values=row.tolist())

        tree.pack(fill=tk.BOTH, expand=True)

        def guardar_datos_excel():
            for _, row in df.iterrows():
                guardar_persona(row['Nombre'], row['Apellido Paterno'], row['Apellido Materno'], row['DNI'], row['Lugar Procedencia'])
            messagebox.showinfo("Cargar Datos", "Datos cargados exitosamente desde el archivo Excel.")
            actualizar_lista_personas()
            preview_window.destroy()

        ttk.Button(preview_window, text="Guardar Datos", command=guardar_datos_excel).pack(pady=10)
=======


