# Play in VLC Server

Este proyecto te permite reproducir videos de YouTube directamente en VLC a través de un servidor local, usando `yt-dlp` y `Flask`. También incluye una extensión de navegador que agrega un botón en los videos de YouTube para enviarlos a VLC fácilmente.

---

## Requisitos Previos

1. **Software Necesario**:
   - [Python 3.10+](https://www.python.org/downloads/)
   - [VLC Media Player](https://www.videolan.org/vlc/index.html)
   - [yt-dlp](https://github.com/yt-dlp/yt-dlp)
   - [FFmpeg](https://ffmpeg.org/download.html)

2. **Extensiones del Navegador**:
   - [Tampermonkey](https://www.tampermonkey.net/) para gestionar scripts personalizados.

---

## Instalación

### 1. Descarga del Proyecto
Clona este repositorio o descárgalo como archivo ZIP:

```bash
git clone https://github.com/tu_usuario/play_in_vlc_server.git
cd play_in_vlc_server
```

### 2. Instala las Dependencias
Ejecuta el siguiente comando para instalar las dependencias necesarias:

```bash
pip install -r requirements.txt

```


### 3. Configura las rutas:

Edita el archivo play_in_vlc_server.py y asegúrate de que las rutas a los ejecutables de yt-dlp, vlc y ffmpeg sean correctas. Por ejemplo:

```
yt_dlp_path = r"C:\Program Files\VideoLAN\VLC\yt-dlp.exe"
vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
ffmpeg_path = r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"

```

Notas:
Si yt-dlp no está en la carpeta C:\Program Files\VideoLAN\VLC\
descárgalo desde su página oficial, crea la carpeta y colócalo allí.

Descarga FFmpeg desde su página oficial, descomprímelo y coloca sus binarios en la carpeta C:\Program Files\ffmpeg\bin.



### 4. Instalación de la Extensión de Navegador:
Para automatizar el envío de videos desde YouTube a VLC, necesitas un script personalizado gestionado por Tampermonkey.

1. Instala Tampermonkey
Ve a https://www.tampermonkey.net/.
Descarga e instala la extensión para tu navegador (Chrome, Firefox, Edge, etc.).
2. Añade el Script
Haz clic en el ícono de Tampermonkey en tu navegador.
Selecciona Crear un nuevo script.
Copia y pega el siguiente código:

```javascript
// ==UserScript==
// @name         Enviar a VLC
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Añade un botón para enviar videos de YouTube a VLC
// @author       farwebsite
// @match        *://*.youtube.com/watch*
// @grant        GM_xmlhttpRequest
// @connect      localhost
// ==/UserScript==

(function () {
    'use strict';

    // Crear el botón para enviar a VLC
    const addButton = () => {
        const controls = document.querySelector('.ytd-video-primary-info-renderer');
        if (!controls) return;

        // Evitar botones duplicados
        if (document.getElementById('send-to-vlc')) return;

        const button = document.createElement('button');
        button.id = 'send-to-vlc';
        button.textContent = 'Enviar a VLC';
        button.style.marginLeft = '10px';
        button.onclick = () => {
            const videoUrl = window.location.href;
            GM_xmlhttpRequest({
                method: 'GET',
                url: `http://localhost:5000/?url=${encodeURIComponent(videoUrl)}`,
                onload: function () {
                    console.log("Video enviado a VLC");
                },
                onerror: function () {
                    alert("Error al enviar el video al servidor. ¿Está el servidor en ejecución?");
                }
            });
        };
        controls.appendChild(button);
    };

    // Detectar cambios en la URL para actualizar el botón
    const observer = new MutationObserver(addButton);
    observer.observe(document.body, { childList: true, subtree: true });

    // Añadir el botón en la carga inicial
    addButton();
})();

```

### 4. Instalación de la Extensión de Navegador:

### 4. Uso del Servidor :
Ejecuta el Servidor:

```bash
python play_in_vlc_server.py

```
Esto iniciará el servidor en http://localhost:5000.

Envía Videos a VLC: Accede a cualquier video de YouTube o en la página principal y haz clic en el botón derecho y despues selecciona "Enviar a VLC". El video se reproducirá automáticamente en VLC.


###  Contribución:

Realiza un fork del proyecto.

Crea una rama para tus cambios:
```
git checkout -b mi_nueva_funcion
```

Envía tus cambios:

```
git add .
git commit -m "Añadí una nueva función"
git push origin mi_nueva_funcion
```
Abre un pull request en GitHub.

### Licencia
Este proyecto está licenciado bajo la [MIT License]((https://opensource.org/license/mit)


