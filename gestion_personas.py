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

# Función para consultar datos de la API de apis.net.pe
def consultar_persona_por_dni(dni):
    url = f"https://api.apis.net.pe/v1/dni?numero={dni}"
    headers = {
        'Authorization': 'Bearer TU_TOKEN_DE_ACCESO'  # Reemplaza 'TU_TOKEN_DE_ACCESO' con tu token real
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'nombres' in data and 'apellidoPaterno' in data and 'apellidoMaterno' in data:
                nombre = data['nombres']
                apellido_paterno = data['apellidoPaterno']
                apellido_materno = data['apellidoMaterno']
                lugar_procedencia = 'No disponible'  # Puedes ajustar esto si la API proporciona esta información
                return (nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia)
            else:
                return None
        else:
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Error al acceder a la API: {e}")
        return None


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
        
        
# Función para abrir el formulario manual
def abrir_formulario_manual(dni):
    if verificar_existencia_dni(dni):
        messagebox.showerror("Error", "El DNI ya está registrado.")
        return

    formulario_window = tk.Toplevel()
    formulario_window.title("Formulario Manual")
    formulario_window.geometry("400x400")

    ttk.Label(formulario_window, text="DNI").pack(pady=5)
    dni_entry_manual = ttk.Entry(formulario_window)
    dni_entry_manual.pack(pady=5)
    dni_entry_manual.insert(0, dni)
    dni_entry_manual.config(state='disabled')

    ttk.Label(formulario_window, text="Apellido Paterno").pack(pady=5)
    apellido_paterno_entry_manual = ttk.Entry(formulario_window)
    apellido_paterno_entry_manual.pack(pady=5)

    ttk.Label(formulario_window, text="Apellido Materno").pack(pady=5)
    apellido_materno_entry_manual = ttk.Entry(formulario_window)
    apellido_materno_entry_manual.pack(pady=5)

    ttk.Label(formulario_window, text="Nombre").pack(pady=5)
    nombre_entry_manual = ttk.Entry(formulario_window)
    nombre_entry_manual.pack(pady=5)

    ttk.Label(formulario_window, text="Lugar de Procedencia").pack(pady=5)
    lugar_procedencia_entry_manual = ttk.Entry(formulario_window)
    lugar_procedencia_entry_manual.pack(pady=5)

    def guardar_datos_manual():
        nombre = nombre_entry_manual.get()
        apellido_paterno = apellido_paterno_entry_manual.get()
        apellido_materno = apellido_materno_entry_manual.get()
        lugar_procedencia = lugar_procedencia_entry_manual.get()

        if not nombre or not apellido_paterno or not apellido_materno:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        guardar_persona(nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia)
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        formulario_window.destroy()
        actualizar_lista_personas()

    ttk.Button(formulario_window, text="Guardar", command=guardar_datos_manual).pack(pady=20)


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

# Función para editar un registro existente
def editar_registro():
    selected_item = lista_personas.curselection()
    if not selected_item:
        messagebox.showerror("Error", "Seleccione un registro para editar.")
        return

    index = selected_item[0]
    item = lista_personas.get(index)
    parts = item.split(" - ")
    id = parts[0].split(": ")[1]
    nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia, fecha, hora = parts[1].split(", ")

    edit_window = tk.Toplevel()
    edit_window.title("Editar Registro")

    ttk.Label(edit_window, text="DNI").pack(pady=5)
    dni_entry_edit = ttk.Entry(edit_window)
    dni_entry_edit.pack(pady=5)
    dni_entry_edit.insert(0, dni)
    dni_entry_edit.config(state='disabled')

    ttk.Label(edit_window, text="Apellido Paterno").pack(pady=5)
    apellido_paterno_entry_edit = ttk.Entry(edit_window)
    apellido_paterno_entry_edit.pack(pady=5)
    apellido_paterno_entry_edit.insert(0, apellido_paterno)

    ttk.Label(edit_window, text="Apellido Materno").pack(pady=5)
    apellido_materno_entry_edit = ttk.Entry(edit_window)
    apellido_materno_entry_edit.pack(pady=5)
    apellido_materno_entry_edit.insert(0, apellido_materno)

    ttk.Label(edit_window, text="Nombre").pack(pady=5)
    nombre_entry_edit = ttk.Entry(edit_window)
    nombre_entry_edit.pack(pady=5)
    nombre_entry_edit.insert(0, nombre)

    ttk.Label(edit_window, text="Lugar de Procedencia").pack(pady=5)
    lugar_procedencia_entry_edit = ttk.Entry(edit_window)
    lugar_procedencia_entry_edit.pack(pady=5)
    lugar_procedencia_entry_edit.insert(0, lugar_procedencia)

    def guardar_datos_editados():
        nombre = nombre_entry_edit.get()
        apellido_paterno = apellido_paterno_entry_edit.get()
        apellido_materno = apellido_materno_entry_edit.get()
        lugar_procedencia = lugar_procedencia_entry_edit.get()

        if not nombre or not apellido_paterno or not apellido_materno:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        actualizar_persona(id, nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia)
        messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
        edit_window.destroy()
        actualizar_lista_personas()

    ttk.Button(edit_window, text="Guardar", command=guardar_datos_editados).pack(pady=20)

# Función para mostrar la pantalla de administrador
def mostrar_pantalla_administrador():
    admin_window = tk.Toplevel()
    admin_window.title("Administrador")

    menubar = tk.Menu(admin_window)
    report_menu = tk.Menu(menubar, tearoff=0)
    report_menu.add_command(label="Reportes Diarios", command=lambda: generar_reporte("diario"))
    report_menu.add_command(label="Reportes Semanales", command=lambda: generar_reporte("semanal"))
    report_menu.add_command(label="Reportes Mensuales", command=lambda: generar_reporte("mensual"))
    menubar.add_cascade(label="Reportes", menu=report_menu)
    menubar.add_command(label="Cargar Datos", command=cargar_datos_desde_excel)
    menubar.add_command(label="Salir", command=admin_window.destroy)
    admin_window.config(menu=menubar)

# Función para validar el login del administrador
def validar_login(usuario, contrasena):
    if usuario == "yorchflrs" and contrasena == "george777":
        mostrar_pantalla_administrador()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
