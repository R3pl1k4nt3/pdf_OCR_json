import tkinter as tk
from tkinter import messagebox  # Import the messagebox module
import subprocess

def ejecutar_script():
    texto_buscar = entry_texto_buscar.get()
    if texto_buscar:
        # Ejecutar el script bash con el texto ingresado como argumento
        comando_bash = f'buscarEnPdf "{texto_buscar}"'
        subprocess.run(comando_bash, shell=True)
        # Mostrar mensaje de ejecución completada
        messagebox.showinfo("Ejecución completada", "El comando se ha ejecutado correctamente.")
        # Cerrar la ventana
        ventana.destroy()
    else:
        messagebox.showerror("Error", "Por favor, ingresa un valor a buscar.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Búsqueda de Texto")

# Centrar la ventana
ancho_ventana = 300
alto_ventana = 100
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
posicion_x = int((ancho_pantalla - ancho_ventana) / 2)
posicion_y = int((alto_pantalla - alto_ventana) / 2)
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

# Etiqueta y campo de entrada para el texto a buscar
label_texto_buscar = tk.Label(ventana, text="Ingrese el texto a buscar:")
label_texto_buscar.pack()

entry_texto_buscar = tk.Entry(ventana)
entry_texto_buscar.pack()

# Botón para ejecutar el script
boton_ejecutar = tk.Button(ventana, text="Buscar y ejecutar", command=ejecutar_script)
boton_ejecutar.pack()

# Iniciar el bucle principal de la interfaz
ventana.mainloop()