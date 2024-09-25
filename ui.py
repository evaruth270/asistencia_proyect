import tkinter as tk
from tkinter import messagebox, ttk
import database_manager

def save_entry():
    # Recolectar datos de los campos de entrada
    student_name = name_entry.get()
    student_id = id_entry.get()
    course = course_var.get()
    date = date_entry.get()
    status = status_var.get()
    
    # Crear un registro para añadir a la base de datos
    record = {
        'StudentName': student_name,
        'StudentID': student_id,
        'Course': course,
        'Date': date,
        'AttendanceStatus': status
    }
    
    # Añadir el registro a la base de datos y guardar
    df = database_manager.load_data()
    df = database_manager.add_record(df, record)
    database_manager.save_data(df)
    
    messagebox.showinfo("Registro Guardado", "La entrada de asistencia ha sido guardada con éxito")

def run_app():
    root = tk.Tk()
    root.title("Sistema de Registro de Asistencia Universitaria")

    global name_entry, id_entry, course_var, date_entry, status_var
    
    tk.Label(root, text="Nombre del Estudiante:").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()
    
    tk.Label(root, text="ID del Estudiante:").pack()
    id_entry = tk.Entry(root)
    id_entry.pack()

    tk.Label(root, text="Curso:").pack()
    course_var = ttk.Combobox(root, values=["Curso 1", "Curso 2", "Curso 3"])
    course_var.pack()

    tk.Label(root, text="Fecha (YYYY-MM-DD):").pack()
    date_entry = tk.Entry(root)
    date_entry.pack()

    tk.Label(root, text="Estado de Asistencia:").pack()
    status_var = ttk.Combobox(root, values=["Presente", "Ausente", "Tardío"])
    status_var.pack()

    tk.Button(root, text="Guardar Entrada", command=save_entry).pack(pady=20)

    root.mainloop()