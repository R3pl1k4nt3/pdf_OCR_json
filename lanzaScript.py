import tkinter as tk
from tkinter import messagebox  # Import the messagebox module
import subprocess
import os

def ejecutar_script():
    texto_buscar_1 = entry_texto_buscar_1.get()
    texto_buscar_2 = entry_texto_buscar_2.get()

    if texto_buscar_1:
        # Construir el comando para ejecutar el script bash
        comando_bash = f'buscarEnPdf "{texto_buscar_1}"'
        if texto_buscar_2:
            comando_bash += f' "{texto_buscar_2}"'

        # Ejecutar el script bash con los textos ingresados como argumentos
        resultado = subprocess.run(comando_bash, shell=True, capture_output=True, text=True)

        # Mostrar mensaje con la salida del comando grep
        mensaje = f"Se ha ejecutado el comando grep con los valores ingresados.\n"
        mensaje += resultado.stdout.strip()  # Agregar la salida del comando grep al mensaje

        # Obtener el nombre del archivo CSV generado
        nombre_archivo = obtener_nombre_archivo(texto_buscar_1, texto_buscar_2)

        # Contar las líneas del archivo CSV
        lineas_csv = contar_lineas_csv(nombre_archivo)

        # Mostrar mensaje con el resultado
        if lineas_csv == 0:
            mensaje += "No hay coincidencias."
        else:
            mensaje += f"Existen coincidencias. El archivo contiene {lineas_csv} línea(s)."
        messagebox.showinfo("Ejecución completada", mensaje)

    else:
        messagebox.showerror("Error", "Por favor, ingresa al menos el primer valor a buscar.")

def obtener_nombre_archivo(texto_buscar_1, texto_buscar_2):
    carpeta_resultados = "/home/alex/resultados"
    if texto_buscar_2:
        return f"resultados{texto_buscar_1}_{texto_buscar_2}.csv"
    else:
        # Buscar el último archivo que coincida con el primer valor en la carpeta "resultados"
        archivos_en_carpeta = os.listdir(carpeta_resultados)
        archivos_coincidentes = [archivo for archivo in archivos_en_carpeta if archivo.startswith(f"resultados{texto_buscar_1}")]
        archivos_coincidentes.sort(reverse=True)  # Ordenar para obtener el más reciente primero
        if archivos_coincidentes:
            return archivos_coincidentes[0]
        else:
            return f"resultados{texto_buscar_1}.csv"

def contar_lineas_csv(archivo_csv):
    carpeta_resultados = "/home/alex/resultados"
    try:
        with open(os.path.join(carpeta_resultados, archivo_csv), 'r') as archivo:
            lineas = archivo.readlines()
            return len(lineas)
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

# Etiqueta y campo de entrada para el segundo texto a buscar (opcional)
label_texto_buscar_2 = tk.Label(ventana, text="Ingrese el segundo texto a buscar (opcional):")
label_texto_buscar_2.pack()

entry_texto_buscar_2 = tk.Entry(ventana)
entry_texto_buscar_2.pack()

# Botón para ejecutar el script
boton_ejecutar = tk.Button(ventana, text="Buscar y ejecutar", command=ejecutar_script)
boton_ejecutar.pack()

# Iniciar el bucle principal de la interfaz
ventana.mainloop()