import os
import sys
import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import ctypes
import threading
import time
from CTkToolTip import CTkToolTip

# Lista de resoluciones disponibles por el momento
calidad_dict = {
        "Original": "original", # Mantener resolucion del video
        "QHD": "2560x1440", #1440p
        "Alta": "1920x1080", #1080p
        "Media": "1280x720", #720p
        "Baja": "854x480", #480p
        "Muy Baja": "640x360", #360p
        "TikTok": "1080x1920", #TikTok
}


def set_app_icon(window):
    if os.name == "nt":
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "icono.ico")
        else:
            icon_path = os.path.join(os.path.dirname(__file__), "icono.ico")
        if os.path.exists(icon_path):
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("CompVi-VC26")
            window.iconbitmap(icon_path)

# --- Variable Global para la lista de archivos ---
lista_archivos_entrada = []

# CPU PRESETS
cpu_preset_map = {
    "Ultra Rápido": "ultrafast",
    "Muy Rápido": "superfast",
    "Rápido": "fast",
    "Medio": "medium", # Default CPU
    "Lento": "slow",
    "Muy Lento": "slower",
    "Ultra Lento": "veryslow"
}
# GPU PRESETS
gpu_preset_map = {
    "P1 (Más Rápido)": "p1",
    "P2": "p2",
    "P3": "p3",
    "P4": "p4",
    "P5 (Equilibrado)": "p5",
    "P6 (Calidad)": "p6", # Default GPU
    "P7 (Mejor Calidad)": "p7"
}


def comprimir_video(input_file, output_directory, calidad_key, audio_bitrate, video_quality_value, video_preset): # Renombrado 'calidad' a 'calidad_key'
    try:
        if not os.path.exists(input_file):
            messagebox.showerror("Error", f"El archivo {input_file} no existe.")
            return
        if not os.path.isdir(output_directory):
            messagebox.showerror("Error", f"El directorio {output_directory} no es válido.")
            return

        if getattr(sys, 'frozen', False):
            
            base_path = sys._MEIPASS # Directorio temporal creado por PyInstaller
            ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")
        else:
           
            ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg.exe")

      

        base_name = os.path.basename(input_file)
        # Usar la clave 'calidad_key' para el nombre, no la resolución
        output_file = os.path.join(output_directory, f"{os.path.splitext(base_name)[0]}_{calidad_key}_comprimido.mp4")

        cmd = [
            ffmpeg_path, "-y", "-i", input_file,
        ]

        # --- Añadir escala solo si no es 'Original' ---
        if calidad_key != "Original":
            resolucion = calidad_dict.get(calidad_key) 
            if resolucion:
                 cmd.extend(["-vf", f"scale={resolucion}"])
            else:
                 # Manejar caso improbable de clave inválida (opcional)
                 print(f"Advertencia: Clave de calidad '{calidad_key}' no encontrada en calidad_dict. No se aplicará escala.")


        if usar_gpu.get():
            # NVENC (GPU) NVIDIA - 
            cmd.extend([
                "-c:v", "hevc_nvenc",
                "-preset", video_preset, 
                "-tune", "hq",
                "-rc", "vbr", "-cq", str(video_quality_value),
                "-rc-lookahead", "32", "-b:v", "0",
            ])
        else:
            # libx265 (CPU) - Usar -crf y -preset
            cmd.extend([
                "-c:v", "libx265",
                "-crf", str(video_quality_value),
                "-preset", video_preset, # Usa el valor FFmpeg pasado
            ])
       
        # CALIDAD DE AUDIO - 
        cmd.extend([
             "-c:a", "aac", "-b:a", audio_bitrate, 
             output_file
        ])

        # Ocultar la ventana de la consola de FFmpeg en Windows
        startupinfo = None
        creationflags = 0
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE # Oculta la ventana
            creationflags = subprocess.CREATE_NO_WINDOW # Asegura que no se cree ventana

        subprocess.run(cmd, check=True, capture_output=True, startupinfo=startupinfo, creationflags=creationflags) # Añadido capture_output y ocultar ventana

        return True

    except subprocess.CalledProcessError as e:
         error_msg = f"Error al comprimir el archivo (código {e.returncode})"
         stderr_output = ""
         if e.stderr:
             try:
                 # Intentar decodificar stderr
                 stderr_output = e.stderr.decode('utf-8', errors='replace')
                 # Limitar la longitud del mensaje de error
                 stderr_preview = stderr_output.strip()[-500:] # Últimos 500 caracteres
                 error_msg += f":\n...\n{stderr_preview}"
             except Exception:
                 error_msg += ": No se pudo decodificar el mensaje de error de FFmpeg."
         else:
             error_msg += f": {e}"
         messagebox.showerror("Error", error_msg)
    except Exception as e: # Capturar otros posibles errores
         messagebox.showerror("Error", f"Error inesperado: {e}")

#Seleccionar archivo(s) de video
def seleccionar_archivo():
    global lista_archivos_entrada # Indicar que usamos la variable global
    # Usar askopenfilenames para obtener una tupla de archivos
    archivos = filedialog.askopenfilenames(
        title="Seleccionar archivo(s) de video",
        filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv")]
    )
    if archivos: # Si el usuario seleccionó archivos
        lista_archivos_entrada = list(archivos) 
        if len(lista_archivos_entrada) == 1:
            entrada.set(lista_archivos_entrada[0]) # Mostrar ruta si es solo uno
        else:
            entrada.set(f"{len(lista_archivos_entrada)} archivos seleccionados") # Mostrar cantidad si son varios
    # else: # Opcional: limpiar si el usuario cancela
        # lista_archivos_entrada = []
        # entrada.set("")


def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta donde quieres que se guarde el archivo.")
    if carpeta:
        salida.set(carpeta)

# INTERFAZ
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ventana = ctk.CTk()
ventana.title("CompVi-VC26")
set_app_icon(ventana)
#Ventana principal, tamaño fijo
ventana.geometry("700x500") 
ventana.resizable(False, False)

entrada = ctk.StringVar()
salida = ctk.StringVar()
calidad_seleccionada = ctk.StringVar(value="Alta") #Calidad por defecto
audio_bitrate_seleccionado = ctk.StringVar(value="128k") #Calidad por defecto
usar_gpu = ctk.BooleanVar(value=False) #Valor de gpu por defdecto
video_quality_slider_value = ctk.IntVar(value=27) #Valor del slider por defecto 27, que es algo "medio" por asi decirlo.
#Variable para el preset seleccionado
video_preset_seleccionado_es = ctk.StringVar()

main_frame = ctk.CTkFrame(ventana)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)
main_frame.grid_columnconfigure(1, weight=1)

# Archivo(s) de video (Fila 0) 
ctk.CTkLabel(main_frame, text="Archivo(s) de video:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
ctk.CTkEntry(main_frame, textvariable=entrada, width=280, state="readonly").grid(row=0, column=1, padx=10, pady=5) # Ancho reducido
ctk.CTkButton(main_frame, text="Seleccionar Archivo(s)", command=seleccionar_archivo, width=140).grid(row=0, column=2, padx=10, pady=5) # Ancho reducido

# Carpeta de salida (Fila 1) 
ctk.CTkLabel(main_frame, text="Carpeta de salida:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
ctk.CTkEntry(main_frame, textvariable=salida, width=280).grid(row=1, column=1, padx=10, pady=5) # Ancho reducido
ctk.CTkButton(main_frame, text="Seleccionar Carpeta", command=seleccionar_carpeta, width=140).grid(row=1, column=2, padx=10, pady=5) # Ancho reducido

# Calidad video (Resolución) (Fila 2)
ctk.CTkLabel(main_frame, text="Resolución Video:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
calidad_combobox = ctk.CTkComboBox(main_frame, values=list(calidad_dict.keys()), variable=calidad_seleccionada, width=150, state= "readonly", justify="center")
calidad_combobox.grid(row=2, column=1, padx=(10, 0), pady=5) 
resolucion_label = ctk.CTkLabel(main_frame, text=calidad_dict[calidad_seleccionada.get()], width=100) # Ancho fijo
resolucion_label.grid(row=2, column=2, padx=(5, 10), pady=5, sticky="w") # Moved to column 2, adjusted padx, sticky="w"

# Calidad Audio (Bitrate) (Fila 3)
ctk.CTkLabel(main_frame, text="Calidad Audio:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
audio_bitrate_combobox = ctk.CTkComboBox(main_frame, values=["64k", "96k", "128k", "192k", "256k", "320k"], variable=audio_bitrate_seleccionado, width=150, state="readonly", justify="center")
audio_bitrate_combobox.grid(row=3, column=1, padx=(10,0), pady=5) 


# Calidad Video (CRF/CQ) (Fila 4)
label_crf_cq = ctk.CTkLabel(main_frame, text="Calidad Vídeo (CRF/CQ):")
label_crf_cq.grid(row=4, column=0, padx=10, pady=5, sticky="w")
CTkToolTip(label_crf_cq, message="Menor valor (18) = Mejor calidad del video, mayor tamaño del archivo\nMayor valor (35) = Peor calidad del video, menor tamaño del archivo")

quality_value_label = ctk.CTkLabel(main_frame, text=str(video_quality_slider_value.get()), width=30)
quality_value_label.grid(row=4, column=2, padx=(5, 10), pady=5, sticky="w") 
quality_slider = ctk.CTkSlider(main_frame, from_=18, to=35, number_of_steps=17, variable=video_quality_slider_value, command=lambda value: quality_value_label.configure(text=f"{int(value)}"))
quality_slider.grid(row=4, column=1, padx=(10, 0), pady=5, sticky="ew")

# Preset Compresión (Fila 5)
label_preset = ctk.CTkLabel(main_frame, text="Velocidad Compresión (Preset):")
label_preset.grid(row=5, column=0, padx=10, pady=5, sticky="w")
CTkToolTip(label_preset, message="Más rápido (ULTRA RAPIDO / P1)= Menos compresion, por lo tanto mas tamaño del archivo misma calidad\nMás lento (ULTRA LENTO / P7) = Más compresion, por lo tanto menor tamaño de archivo y misma calidad \n Ejemplo ficticio: \n P1/UltraRapido arhivo inicial 5gb tamaño final 1gb \n  P7/UltraLento, archivo inicial 5gb tamaño final 300mb")

preset_combobox = ctk.CTkComboBox(main_frame, variable=video_preset_seleccionado_es, width=180, state="readonly", justify="center")
preset_combobox.grid(row=5, column=1, padx=(10, 0), pady=5) # Removed sticky
CTkToolTip(preset_combobox, message="CPU: Ultra Rápido (peor compresión) a Ultra Lento (mejor compresión).\nGPU: P1 (más rápido) a P7 (mejor calidad/compresión).")

# Checkbox GPU (Fila 6)
gpu_checkbox = ctk.CTkCheckBox(main_frame, text="Usar GPU", variable=usar_gpu, onvalue=True, offvalue=False, command=lambda: actualizar_presets())
gpu_checkbox.grid(row=6, column=1, padx=(10,0), pady=5) # Removed sticky
CTkToolTip(gpu_checkbox, message="Utiliza la tarjeta gráfica NVIDIA para acelerar la compresión (requiere NVENC). Puede ser más rápido pero menos eficiente en tamaño que la CPU.")

# Función para actualizar presets 
def actualizar_presets():
    current_selection_es = video_preset_seleccionado_es.get()
    if usar_gpu.get():
        preset_combobox.configure(values=list(gpu_preset_map.keys()))
        # Si la selección actual no está en los presets de GPU, o no hay selección, poner default GPU
        if current_selection_es not in gpu_preset_map:
             video_preset_seleccionado_es.set("P6 (Calidad)") # Default GPU
    else:
        preset_combobox.configure(values=list(cpu_preset_map.keys()))
        # Si la selección actual no está en los presets de CPU, o no hay selección, poner default CPU
        if current_selection_es not in cpu_preset_map:
             video_preset_seleccionado_es.set("Medio") # Default CPU en Español

# Llamar una vez al inicio para establecer los presets iniciales (CPU por defecto)
actualizar_presets()

def actualizar_resolucion(*args):
    resolucion_label.configure(text=calidad_dict.get(calidad_seleccionada.get(), ""))
calidad_seleccionada.trace_add("write", actualizar_resolucion)

# Función de compresión principal
def comprimir_con_calidad_seleccionada():
    # Validar entradas antes de empezar
    if not lista_archivos_entrada:
        messagebox.showwarning("Advertencia", "Por favor, selecciona uno o más archivos de video.")
        return
    if not salida.get() or not os.path.isdir(salida.get()):
        messagebox.showwarning("Advertencia", "Por favor, selecciona una carpeta de salida válida.")
        return

    boton_comprimir.configure(state="disabled")
    spinner_label.configure(text="⏳ Preparando...")
    tiempo_label.configure(text="Tiempo transcurrido: 00:00")
    ventana.update_idletasks()

    def tarea():
        start_time = time.time()
        tarea_terminada = [False]
        archivos_procesados = 0
        archivos_fallidos = 0
        total_archivos = len(lista_archivos_entrada)

        # Obtener valores ANTES del bucle 
        current_video_quality = video_quality_slider_value.get()
        # Obtener el nombre del preset
        preset_es = video_preset_seleccionado_es.get()
        # TRADUCIR preset español a valor FFmpeg
        if usar_gpu.get():
            current_preset_ffmpeg = gpu_preset_map.get(preset_es, "p6") # Default a p6 si hay error
        else:
            current_preset_ffmpeg = cpu_preset_map.get(preset_es, "medium") # Default a medium si hay error

        # Hilos para animación y tiempo
        spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        spinner_index = [0]

        #Animacion spinner
        def actualizar_animacion(texto_base="En proceso..."):
            while not tarea_terminada[0]:
                 current_text = spinner_label.cget("text").split(" ", 1)[1] if " " in spinner_label.cget("text") else texto_base
                 spinner_label.configure(text=f"{spinner_frames[spinner_index[0] % len(spinner_frames)]} {current_text}")
                 spinner_index[0] += 1
                 time.sleep(0.1)
            
            final_text = spinner_label.cget("text").split(" ", 1)[1] if " " in spinner_label.cget("text") else ""
            if "✅" not in final_text and "❌" not in final_text:
                 spinner_label.configure(text=final_text)
        #Actualizacion tiempo
        def actualizar_tiempo():
            while not tarea_terminada[0]:
                 elapsed = int(time.time() - start_time)
                 minutes = elapsed // 60
                 seconds = elapsed % 60
                 tiempo_label.configure(text=f"Tiempo transcurrido: {minutes:02d}:{seconds:02d}")
                 time.sleep(1)
            

            elapsed = int(time.time() - start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60 # Calcular segundos finales
            tiempo_label.configure(text=f"Tiempo total: {minutes:02d}:{seconds:02d}") # Mostrar tiempo total
            

        hilo_spinner = threading.Thread(target=actualizar_animacion, daemon=True)
        hilo_tiempo = threading.Thread(target=actualizar_tiempo, daemon=True)
        hilo_spinner.start()
        hilo_tiempo.start()

        # Bucle para procesar cada archivo 
        for i, archivo_in in enumerate(lista_archivos_entrada):
            nombre_corto = os.path.basename(archivo_in)
            spinner_label.configure(text=f"⏳ Procesando {i+1}/{total_archivos}: {nombre_corto}...")
            ventana.update_idletasks()

            #  Llamar a comprimir_video con el valor de calidad y el preset FFmpeg 
            exito = comprimir_video(
                archivo_in,
                salida.get(),
                calidad_seleccionada.get(),
                audio_bitrate_seleccionado.get(),
                current_video_quality,
                current_preset_ffmpeg # Pasar el valor FFmpeg 
            )

            if exito:
                archivos_procesados += 1
            else:
                archivos_fallidos += 1
                print(f"Fallo al procesar: {nombre_corto}")

        # --- Finalización ---
        tarea_terminada[0] = True
        # Esperar un poquito para que los hilos de UI terminen limpiamente (opcional)
        # time.sleep(0.2)

        # Mensaje final
        if archivos_fallidos == 0:
             spinner_label.configure(text=f"✅ Completado ({archivos_procesados} archivos)")
             messagebox.showinfo("Completado", f"Se han comprimido {archivos_procesados} archivo(s) correctamente.")
        elif archivos_procesados > 0:
              spinner_label.configure(text=f"⚠️ Completado con errores ({archivos_procesados} éxito, {archivos_fallidos} fallos)")
              messagebox.showwarning("Completado con errores", f"Se completaron {archivos_procesados} archivo(s).\nFallaron {archivos_fallidos} archivo(s).\nRevisa la consola para más detalles si hubo errores.")
        else:
              spinner_label.configure(text=f"❌ Fallo total ({archivos_fallidos} archivos)")
              messagebox.showerror("Error", f"No se pudo comprimir ninguno de los {archivos_fallidos} archivo(s).")


        boton_comprimir.configure(state="normal")

    threading.Thread(target=tarea, daemon=True).start()

# --- Botón Comprimir (Fila 7) --- Ajustar fila y ancho
boton_comprimir = ctk.CTkButton(main_frame, text="Comprimir", command=comprimir_con_calidad_seleccionada, fg_color="green", width=180) # Ancho aumentado
boton_comprimir.grid(row=7, column=1, padx=10, pady=20) # Movido a fila 7

# --- Labels de estado/tiempo (Filas 8 y 9)
spinner_label = ctk.CTkLabel(main_frame, text="")
spinner_label.grid(row=8, column=0, columnspan=3, pady=5) # Movido a fila 8
tiempo_label = ctk.CTkLabel(main_frame, text="")
tiempo_label.grid(row=9, column=0, columnspan=3, pady=5) # Movido a fila 9


ventana.mainloop()