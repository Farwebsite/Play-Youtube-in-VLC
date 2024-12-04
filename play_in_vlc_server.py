import os
import subprocess
from flask import Flask, request
import platform
import getpass

app = Flask(__name__)

# Configuración de rutas
YT_DLP_PATH = r"C:\Program Files\VideoLAN\VLC\yt-dlp.exe"
VLC_PATH = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
FFMPEG_PATH = r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"
TEMP_VIDEO = os.path.join(os.environ.get("TEMP", "/tmp"), "video_temp.mp4")

@app.route('/')
def play_in_vlc():
    url = request.args.get('url')
    if not url:
        return "No se proporcionó una URL", 400

    # Comando por defecto: transmisión directa
    direct_stream_command = [
        YT_DLP_PATH,
        "-f", "bestvideo+bestaudio/best",
        "--ffmpeg-location", FFMPEG_PATH,
        "-o", "-",  # Salida directa
        url
    ]

    vlc_command = [
        VLC_PATH,
        "-",  # VLC toma la entrada desde stdin
        "--play-and-exit",
        "--video-on-top"  # Mantiene VLC siempre en primer plano
    ]

    try:
        print(f"Ejecutando transmisión directa: {' '.join(direct_stream_command)}")
        with subprocess.Popen(direct_stream_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as yt_dlp_process:
            subprocess.run(vlc_command, stdin=yt_dlp_process.stdout)

        return "Reproduciendo en VLC en transmisión directa", 200

    except Exception as e:
        print(f"Error en transmisión directa: {e}")
        print("Intentando con archivo temporal...")

        # Intentar con archivo temporal
        temp_command = [
            YT_DLP_PATH,
            "-f", "bestvideo+bestaudio/best",
            "--ffmpeg-location", FFMPEG_PATH,
            "-o", TEMP_VIDEO,
            url
        ]

        try:
            print(f"Descargando video a archivo temporal: {' '.join(temp_command)}")
            temp_result = subprocess.run(temp_command, capture_output=True, text=True)

            if temp_result.returncode != 0:
                print(f"Error al descargar video temporal: {temp_result.stderr}")
                return f"Error al descargar video: {temp_result.stderr}", 500

            # Reproducir el archivo temporal en VLC
            vlc_temp_command = [
                VLC_PATH,
                TEMP_VIDEO,
                "--play-and-exit",
                "--video-on-top"  # Mantiene VLC siempre en primer plano
            ]

            print(f"Ejecutando VLC con archivo temporal: {' '.join(vlc_temp_command)}")
            subprocess.run(vlc_temp_command)

            # Eliminar archivo temporal
            if os.path.exists(TEMP_VIDEO):
                os.remove(TEMP_VIDEO)
                print("Archivo temporal eliminado.")

            return "Reproducción completada", 200

        except Exception as temp_error:
            print(f"Error al manejar archivo temporal: {temp_error}")
            return f"Error general: {temp_error}", 500


if __name__ == '__main__':
    print(f"Sistema Operativo: {platform.system()} {platform.release()}")
    print(f"Usuario Actual: {getpass.getuser()}")
    app.run(host='localhost', port=5000)
