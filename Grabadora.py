import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
from scipy.io.wavfile import write
import simpleaudio as sa
import os
import numpy as np  # Para manejo de arrays y conversión de tipos

# Frecuencia de muestreo estándar para audio (Hz)
fs = 44100

def grabar_audio():
    
    #Graba audio desde el micrófono durante la duración indicada por el usuario,
    #normaliza y convierte la señal a formato int16,
    #y guarda el archivo en formato WAV con el nombre ingresado.
    
    try:
        # Obtener duración y nombre del archivo desde la interfaz
        duracion = int(entry_duracion.get())
        nombre_archivo = entry_nombre.get().strip()

        # Validaciones básicas
        if not nombre_archivo:
            messagebox.showerror("Error", "Por favor ingresa un nombre para el archivo.")
            return
        if any(c in nombre_archivo for c in r'\/:*?"<>|'):
            messagebox.showerror("Error", "El nombre contiene caracteres inválidos: \\ / : * ? \" < > |")
            return
        if duracion <= 0:
            messagebox.showerror("Error", "La duración debe ser un número entero positivo.")
            return

        filename = f"{nombre_archivo}.wav"

        # Si el archivo existe, eliminarlo para evitar conflictos
        if os.path.exists(filename):
            os.remove(filename)

        # Informar inicio de grabación
        messagebox.showinfo("Grabando", f"Grabando por {duracion} segundos...")

        # Grabar audio estéreo
        audio = sd.rec(int(duracion * fs), samplerate=fs, channels=2)
        sd.wait()  # Esperar a que termine la grabación

        # Normalizar el audio para que esté en rango [-1, 1]
        audio_normalizado = audio / np.max(np.abs(audio))

        # Convertir a int16 para formato WAV estándar
        audio_int16 = (audio_normalizado * 32767).astype(np.int16)

        # Guardar archivo WAV
        write(filename, fs, audio_int16)

        # Confirmar guardado
        messagebox.showinfo("Grabación terminada", f"Archivo guardado como {filename}")

    except ValueError:
        messagebox.showerror("Error", "Duración inválida. Debe ser un número entero.")
    except Exception as e:
        messagebox.showerror("Error inesperado", str(e))


def reproducir_audio():
    
    #Reproduce el archivo WAV cuyo nombre ingresa el usuario.
    #Muestra mensajes de error si no encuentra el archivo o si no puede reproducirlo.

    try:
        nombre_archivo = entry_nombre.get().strip()
        if not nombre_archivo:
            messagebox.showerror("Error", "Por favor ingresa el nombre del archivo a reproducir.")
            return

        filename = f"{nombre_archivo}.wav"

        # Verificar existencia del archivo
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"No se encontró el archivo {filename}.")
            return

        # Cargar y reproducir audio
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    except Exception as e:
        messagebox.showerror("Error al reproducir", f"No se pudo reproducir el archivo.\nDetalles: {str(e)}")
        print(f"Error al reproducir {filename}: {e}")


# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Grabadora de Audio")
ventana.geometry("350x220")

# Interfaz gráfica: etiquetas y campos de entrada
tk.Label(ventana, text="Nombre del archivo (sin extensión):").pack(pady=5)
entry_nombre = tk.Entry(ventana)
entry_nombre.pack(pady=5)

tk.Label(ventana, text="Duración (segundos):").pack(pady=5)
entry_duracion = tk.Entry(ventana)
entry_duracion.pack(pady=5)

# Botones para grabar y reproducir
boton_grabar = tk.Button(ventana, text="Grabar", command=grabar_audio)
boton_grabar.pack(pady=10)

boton_reproducir = tk.Button(ventana, text="Reproducir", command=reproducir_audio)
boton_reproducir.pack(pady=5)

# Ejecutar la ventana
ventana.mainloop()
