# 🎬 CompVi-VC26 - Compresor de Vídeo Fácil 🎬

¡Bienvenido/a a **CompVi-VC26**! 🎉

Esta es una aplicación de escritorio sencilla, creada con Python y `customtkinter`, diseñada para ayudarte a **comprimir tus vídeos** de forma rápida y eficiente usando el poder de FFmpeg. ¡Reduce el tamaño de tus archivos sin complicaciones!

## ✨ Características Principales ✨

*   🖼️ **Interfaz Gráfica Intuitiva:** Fácil de usar gracias a `customtkinter`.
*   📂 **Selección Múltiple:** Comprime varios vídeos a la vez.
*   🎯 **Carpeta de Destino:** Elige dónde guardar los vídeos resultantes.
*   📏 **Calidad de Compresión (Resolución):** Opciones predefinidas (Original, QHD, 1080p, 720p, 480p, 360p, TikTok).
*   🔊 **Calidad de Audio:** Ajusta el bitrate del audio (ej: 128k, 192k).
*   🎞️ **Calidad de Vídeo (CRF/CQ):** Control preciso sobre la calidad visual y el tamaño del archivo.
*   ⚡ **Presets de Codificación:** Elige entre velocidad y eficiencia de compresión (CPU y GPU).
*   🚀 **Aceleración por GPU (Opcional):** Usa tu tarjeta NVIDIA (NVENC) para comprimir más rápido.
*   ⏳ **Proceso en Segundo Plano:** La interfaz no se bloquea mientras comprime.
*   📊 **Progreso y Tiempo:** Barra de progreso y estimación del tiempo restante.
*   🚦 **Indicador de Estado:** Ve si está Listo, Comprimiendo, Completado o si hubo un Error.
*   🎨 **Icono Personalizado:** Identifica fácilmente la aplicación.
*   📦 **Ejecutable para Windows:** Creado con PyInstaller para usar sin instalar Python.

## ⚙️ Requisitos Previos si vas a clonar directamente el directorio, si no en release esta el .exe⚙️

*   🐍 **Python 3.x:** Necesario si ejecutas el script `.py`.
*   🎬 **FFmpeg:** **¡Imprescindible!** Descarga `ffmpeg.exe` desde [ffmpeg.org](https://ffmpeg.org/download.html) y colócalo en la **misma carpeta** que el script o el `.exe`. (Te dejo incluida la version que yo utilizo aqui, pero puedes bajar la mas actual si lo necesitas)
*   💨 **(Opcional) GPU NVIDIA:** Si quieres usar la opción "Usar GPU", necesitas una tarjeta compatible con NVENC y los drivers actualizados.

## 🛠️ Instalación (Si usas el script .py) 🛠️

Abre una terminal o CMD y ejecuta:

pip install customtkinter CTkToolTip packaging darkdetect

📁 Estructura del Proyecto 📁
├── 🐍 CompVi-VC26.py              # El corazón de la aplicación (script Python)
├── 🚀 ffmpeg.exe                  # ¡Fundamental! El motor de compresión
├── 🎨 icono.ico                   # El icono de la app
├── 🖼️ customtkinter/              # Librería para la interfaz gráfica
├── ℹ️ CTkToolTip/                 # Librería para las ayudas flotantes (tooltips)
└── 🌓 darkdetect/                 # Dependencia de customtkinter

## ▶️ Cómo Usar la Aplicación ▶️
1. Ejecuta CompVi-VC26.py (si tienes Python) o el CompVi-VC26.exe .
2. 🖱️ Haz clic en "Seleccionar Archivo(s)" y elige los vídeos que quieres comprimir.
3. 🖱️ Haz clic en "Seleccionar Carpeta" y elige dónde guardar los resultados.
4. 👇 Selecciona la "Resolución Video" que prefieras.
5. 🎧 Ajusta la "Calidad Audio" (bitrate).
6. ✅ Marca "Usar GPU" si tienes una NVIDIA compatible y quieres ir más rápido (puede que el archivo final sea un poco más grande que con CPU).
7. 📊 Mueve el deslizador de "Calidad Vídeo (CRF/CQ)" :
   - 📉 Menor valor (izquierda, ej: 18): Mejor calidad, archivo más grande.
   - 📈 Mayor valor (derecha, ej: 35): Menor calidad, archivo más pequeño.
8. ⏱️ Elige la "Velocidad Compresión (Preset)" :
   - 🐢 Más lento: Mejor compresión (archivo más pequeño), tarda más.
   - 🐇 Más rápido: Menos compresión (archivo más grande), tarda menos.
9. 🟩 Haz clic en el botón verde "Comprimir" .
10. 👀 ¡Observa el progreso! La aplicación te informará cuando termine.

## 📜 Licencia 📜
Este proyecto es de código abierto. ¡Úsalo, modifícalo y compártelo como quieras! 😊
