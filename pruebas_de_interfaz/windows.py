import tkinter as tk
import os
import subprocess

def iniciar_captura():

    estado_label.config(text="Capturando datos...")


def detener_captura():

    estado_label.config(text="Deteniendo proceso...")
    

def descargar_datos():

    estado_label.config(text="Descargando datos...")
    

# Crear una ventana
ventana = tk.Tk()
ventana.title("Aplicación de Captura de Datos")

# Cambiar el tamaño de la ventana
ventana.geometry("800x400")

# Personalizar los botones
boton_iniciar = tk.Button(ventana, text="Iniciar captura de datos", command=iniciar_captura, width=40, height=4, bg="green")
boton_iniciar.pack()

boton_detener = tk.Button(ventana, text="Detener proceso", command=detener_captura, width=40, height=4, bg="red")
boton_detener.pack()

boton_descargar = tk.Button(ventana, text="Descargar datos", command=descargar_datos, width=40, height=4, bg="blue")
boton_descargar.pack()

# Etiqueta para mostrar el estado
estado_label = tk.Label(ventana, text="", height=2)
estado_label.pack()

ventana.mainloop()

