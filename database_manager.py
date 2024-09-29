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

