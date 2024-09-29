#git clone https://github.com/evaruth270/asistencia_proyect.git

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
#print("hola nena")
