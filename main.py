import os
import threading
from pytube import YouTube
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def download_video():
    video_url = entry_url.get()
    output_path = r"D:\Programas_Carlos\Download_Mp4\Descargas"
    
    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        progress_var.set(percentage)
        root.update_idletasks()  # Asegura que la GUI se actualice inmediatamente

    def download_thread():
        try:
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            
            yt = YouTube(video_url, on_progress_callback=on_progress)
            stream = yt.streams.filter(res="720p", file_extension='mp4').first()
            if not stream:
                raise Exception("No hay streams disponibles en 720p para este video.")
            
            title = yt.title
            artist = yt.author
            
            update_status(f"{title} - {artist}: Descargando...")
            
            # Modifica la línea siguiente para incluir el nombre del artista en el nombre del archivo
            filepath = os.path.join(output_path, f"{title} - {artist}.mp4")
            stream.download(output_path=output_path, filename=f"{title} - {artist}.mp4")
            
            update_status(f"{title} - {artist}: Descargado")
            progress_var.set(0)  # Reinicia la barra de progreso
            update_treeview(filepath, "Descargado")  # Actualiza la Treeview
            messagebox.showinfo("Información", "Descarga completada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    threading.Thread(target=download_thread).start()

def update_status(message):
    label_status.config(text=message)
    root.update_idletasks()  # Asegura que la GUI se actualice inmediatamente

def update_treeview(filename, status):
    file_name = os.path.basename(filename)  # Obtener solo el nombre del archivo
    treeview.insert("", "end", values=(file_name, status))  # Insertar una nueva fila en la Treeview
    treeview.column("Name", width=400, anchor="center")  # Configurar el ancho de la columna "Name" y centrar el texto
    treeview.column("Status", width=150, anchor="center")  # Configurar el ancho de la columna "Status" y centrar el texto
    treeview.heading("Name", text="Nombre", anchor="center")  # Centrar el texto en la columna "Name"
    treeview.heading("Status", text="Estado", anchor="center")  # Centrar el texto en la columna "Status"

# Crear ventana principal
root = tk.Tk()
root.title("Descargador de videos MP4 desde YouTube")

# Ajustar tamaño de la ventana
root.geometry("1000x550")

# Cambiar el color de fondo de la ventana
root.configure(bg="#BEC8C9")

# Crear elementos de la interfaz
label_url = tk.Label(root, text="Introduce el enlace del video:", font=("Arial", 20), bg="#BEC8C9")
label_url.pack(pady=20)

entry_url = tk.Entry(root, width=50, font=("Arial", 16))
entry_url.pack(pady=10)

button_download = tk.Button(root, text="Descargar", command=download_video, font=("Arial", 20))
button_download.pack(pady=20)

# Crear Label para mostrar el estado de las descargas
label_status = tk.Label(root, text="", font=("Arial", 16), bg="#BEC8C9")
label_status.pack(pady=20)

# Crear Progressbar para mostrar el progreso de la descarga
progress_var = tk.DoubleVar()
style = ttk.Style()
style.configure("TProgressbar", thickness=30)  # Cambiar grosor de la barra de progreso
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=500, style="TProgressbar")
progress_bar.pack(pady=20, padx=20)

# Crear Treeview para mostrar los archivos descargados
treeview = ttk.Treeview(root, columns=("Name", "Status"), height=10, show="headings")
treeview.heading("Name", text="Nombre")
treeview.heading("Status", text="Estado")
treeview.pack(pady=20)

# Ejecutar el bucle principal de la ventana
root.mainloop()
