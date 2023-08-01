import tkinter as tk
from tkinter import messagebox  # Import the messagebox module
import subprocess

def ejecutar_script():
    texto_buscar_1 = entry_texto_buscar_1.get()
    texto_buscar_2 = entry_texto_buscar_2.get()
    if texto_buscar_1 and texto_buscar_2:
        # Ejecutar el script bash con los textos ingresados como argumentos
        comando_bash = f'buscarEnPdf "{texto_buscar_1}" "{texto_buscar_2}"'
        subprocess.run(comando_bash, shell=True)
        # Contar las líneas del archivo CSV
        archivo_csv = f"resultados{texto_buscar_1}_{texto_buscar_2}.csv"
        lineas_csv = contar_lineas_csv(archivo_csv)
        # Mostrar mensaje con el resultado
        if lineas_csv == 0:
            mensaje = "No hay coincidencias."
        else:
            mensaje = f"Existen coincidencias. El archivo contiene {lineas_csv} línea(s)."
        messagebox.showinfo("Ejecución completada", mensaje)
    else:
        messagebox.showerror("Error", "Por favor, ingresa ambos valores a buscar.")

def contar_lineas_csv(archivo_csv):
    try:
        with open(archivo_csv, 'r') as archivo:
            return sum(1 for linea in archivo)
    except FileNotFoundError:
        return 0

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Búsqueda de Texto")

# Centrar la ventana
ancho_ventana = 400
alto_ventana = 150
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
posicion_x = int((ancho_pantalla - ancho_ventana) / 2)
posicion_y = int((alto_pantalla - alto_ventana) / 2)
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

# Etiqueta y campo de entrada para el primer texto a buscar
label_texto_buscar_1 = tk.Label(ventana, text="Ingrese el primer texto a buscar:")
label_texto_buscar_1.pack()

entry_texto_buscar_1 = tk.Entry(ventana)
entry_texto_buscar_1.pack()

# Etiqueta y campo de entrada para el segundo texto a buscar
label_texto_buscar_2 = tk.Label(ventana, text="Ingrese el segundo texto a buscar:")
label_texto_buscar_2.pack()

entry_texto_buscar_2 = tk.Entry(ventana)
entry_texto_buscar_2.pack()

# Botón para ejecutar el script
boton_ejecutar = tk.Button(ventana, text="Buscar y ejecutar", command=ejecutar_script)
boton_ejecutar.pack()

# Iniciar el bucle principal de la interfaz
ventana.mainloop()