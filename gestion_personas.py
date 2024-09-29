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



#yorch debe continuar...








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
