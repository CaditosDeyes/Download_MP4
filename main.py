import os
import threading
import yt_dlp
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk

# Cargar última carpeta seleccionada
def load_last_folder():
    try:
        with open("config.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "D:\\Programas_Carlos\\Download_Mp4\\Descargas"  # Ruta por defecto

# Guardar carpeta seleccionada
def save_last_folder(path):
    with open("config.txt", "w") as f:
        f.write(path)

# Seleccionar carpeta de descarga
def select_download_folder():
    global output_path
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_path = folder_selected
        save_last_folder(output_path)
        label_folder.config(text=f"Carpeta seleccionada: {output_path}")

# Descargar video
def download_video():
    video_url = entry_url.get()
    if not video_url:
        messagebox.showwarning("Advertencia", "Por favor, introduce un enlace de YouTube.")
        return
    
    def on_progress(progress_data):
        if 'downloaded_bytes' in progress_data and 'total_bytes' in progress_data:
            bytes_downloaded = progress_data['downloaded_bytes']
            total_size = progress_data['total_bytes']
            percentage = (bytes_downloaded / total_size) * 100
            progress_var.set(percentage)
            root.update_idletasks()

    def download_thread():
        try:
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            ydl_opts_info = {
                'quiet': True,  # Suprime la salida en consola
                'skip_download': True,  # No descargar, solo obtener información
            }

            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                title = info_dict.get('title', 'Desconocido')
            
            # Mostrar el título en la interfaz antes de descargar
            update_status(f"Descargando: {title}")

            ydl_opts_download = {
                'format': 'bestvideo[ext=mp4][height<=?1080]+bestaudio[ext=m4a]/best[ext=mp4]',
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'progress_hooks': [on_progress],
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
                ydl.download([video_url])

            update_status(f"Descarga finalizada: {title}")
            progress_var.set(0)

            update_treeview(title, "Descargado")
            messagebox.showinfo("Información", f"Descarga finalizada correctamente: {title}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    threading.Thread(target=download_thread).start()

# Actualizar estado
def update_status(message):
    label_status.config(text=message)
    root.update_idletasks()

# Actualizar Treeview
def update_treeview(filename, status):
    file_name = os.path.basename(filename)
    treeview.insert("", "end", values=(file_name, status))
    treeview.column("Name", width=900, anchor="center")
    treeview.column("Status", width=200, anchor="center")
    treeview.heading("Name", text="Nombre", anchor="center")
    treeview.heading("Status", text="Estado", anchor="center")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Descargador de videos desde YouTube")
root.geometry("1000x600")
root.configure(bg="#BEC8C9")

frame_folder = tk.Frame(root, bg="#BEC8C9")
frame_folder.pack(pady=10)

output_path = load_last_folder()
label_folder = tk.Label(frame_folder, text=f"Carpeta seleccionada: {output_path}", font=("Roboto", 12), bg="#BEC8C9")
label_folder.pack(side="left", padx=5)
button_select_folder = tk.Button(frame_folder, text="Seleccionar Carpeta", command=select_download_folder, font=("Roboto", 12))
button_select_folder.pack(side="right")

# Elementos de la interfaz
tk.Label(root, text="Introduce el enlace del video:", font=("Roboto", 16), bg="#BEC8C9").pack(pady=10)
entry_url = tk.Entry(root, width=50, font=("Roboto", 14))
entry_url.pack(pady=5)

button_download = tk.Button(root, text="Descargar", command=download_video, font=("Roboto", 16))
button_download.pack(pady=20)

label_status = tk.Label(root, text="", font=("Roboto", 14), bg="#BEC8C9")
label_status.pack(pady=10)

progress_var = tk.DoubleVar()
style = ttk.Style()
style.configure("TProgressbar", thickness=30)
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=500, style="TProgressbar")
progress_bar.pack(pady=10, padx=20)

treeview = ttk.Treeview(root, columns=("Name", "Status"), height=10, show="headings")
treeview.heading("Name", text="Nombre")
treeview.heading("Status", text="Estado")
treeview.pack(pady=10)

root.mainloop()
