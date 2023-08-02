import tkinter as tk
from tkinter import Scrollbar, Text, messagebox  # Import the Text widget and Scrollbar module
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

        # Almacenar el resultado del primer grep
        resultado_grep_1 = resultado.stdout

        # Mostrar mensaje con el resultado del contador CSV
        mensaje = f"Se ha ejecutado el comando grep con los valores ingresados.\n"
        mensaje += f"\nContador CSV: {obtener_lineas_csv(texto_buscar_1, texto_buscar_2, resultado_grep_1)}"

        # Mostrar los resultados del comando grep en la interfaz
        if texto_buscar_2:
            resultado_grep_2 = subprocess.run(f'grep -i "{texto_buscar_2}"', input=resultado_grep_1, shell=True, capture_output=True, text=True)
            mensaje += f"\n\nResultados del segundo grep:\n{resultado_grep_2.stdout.strip()}"
        else:
            mensaje += f"\n\nResultados del primer grep:\n{resultado_grep_1.strip()}"
        
        mostrar_resultados(mensaje)

    else:
        messagebox.showerror("Error", "Por favor, ingresa al menos el primer valor a buscar.")

def obtener_lineas_csv(texto_buscar_1, texto_buscar_2, resultado_grep_1):
    nombre_archivo = obtener_nombre_archivo(texto_buscar_1, texto_buscar_2)
    lineas_csv = contar_lineas_csv(nombre_archivo, resultado_grep_1)
    if lineas_csv == 0:
        return "No hay coincidencias."
    else:
        return f"Existen coincidencias. El archivo contiene {lineas_csv} línea(s)."

def obtener_nombre_archivo(texto_buscar_1, texto_buscar_2):
    carpeta_resultados = "/home/alex/resultados"
    if texto_buscar_2:
        return f"resultados{texto_buscar_1}_{texto_buscar_2}.csv"
    else:
        archivos_en_carpeta = os.listdir(carpeta_resultados)
        archivos_coincidentes = [archivo for archivo in archivos_en_carpeta if archivo.startswith(f"resultados{texto_buscar_1}")]
        archivos_coincidentes.sort(reverse=True)
        if archivos_coincidentes:
            return archivos_coincidentes[0]
        else:
            return f"resultados{texto_buscar_1}.csv"

def contar_lineas_csv(archivo_csv, resultado_grep_1):
    carpeta_resultados = "/home/alex/resultados"
    try:
        with open(os.path.join(carpeta_resultados, archivo_csv), 'r') as archivo:
            lineas = archivo.readlines()
            lineas_csv = len(lineas)

            # Si el resultado del primer grep es el mismo archivo CSV, restar 1 al contador de líneas
            if archivo_csv in resultado_grep_1:
                lineas_csv -= 1

            return lineas_csv
    except FileNotFoundError:
        return 0

def mostrar_resultados(mensaje):
    # Crear una nueva ventana para mostrar los resultados
    ventana_resultados = tk.Toplevel(ventana)
    ventana_resultados.title("Resultados de búsqueda")

    # Cuadro de texto para mostrar los resultados
    cuadro_texto_resultados = Text(ventana_resultados, wrap=tk.WORD)
    cuadro_texto_resultados.pack(fill=tk.BOTH, expand=True)

    # Barra de desplazamiento para el cuadro de texto
    scrollbar = Scrollbar(ventana_resultados, command=cuadro_texto_resultados.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    cuadro_texto_resultados.config(yscrollcommand=scrollbar.set)

    # Insertar los resultados en el cuadro de texto
    cuadro_texto_resultados.insert(tk.END, mensaje)

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