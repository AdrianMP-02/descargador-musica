# Descargador Fácil

Una aplicación sencilla para Windows que permite descargar música (MP3) y vídeo (MP4) de YouTube. Diseñada específicamente para ser intuitiva y fácil de usar.

## Características

- **Interfaz Simple**: Botones grandes y claros.
- **Portátil**: No requiere instalación.
- **Actualizaciones Automáticas**: Se conecta con GitHub para avisarte si hay una nueva versión.
- **Formato MP3 y MP4**: Elige entre solo audio o vídeo completo.
- **Automatización**: GitHub Actions integrado para crear releases automáticamente en cada commit a `main`.

## Integración con GitHub

Para subir el proyecto y activar las actualizaciones automáticas:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/AdrianMP-02/descargador-musica.git
git push -u origin main
```

1. Abre la aplicación `Descargador-Musica.exe`.
2. Copia el enlace del vídeo de YouTube que quieras descargar.
3. Pégalo en el cuadro de texto central.
4. Haz clic en el botón rojo **"Escuchar (MP3)"** si quieres la canción, o en el botón azul **"Ver (MP4)"** si quieres el vídeo.
5. ¡Listo! El archivo se guardará en la carpeta `Musica Descargada` junto al programa.

### Si algún vídeo no descarga (verificación de YouTube)

YouTube cambia con frecuencia cómo protege sus vídeos, lo que a veces hace que `yt-dlp` deje de funcionar hasta que se actualiza. Este proyecto ya usa la versión más reciente de `yt-dlp` (sin fijar una versión concreta en `requirements.txt`) y prueba varios "clientes" de YouTube automáticamente para esquivar estos bloqueos.

Si aun así algún vídeo pide iniciar sesión o da error de verificación, puedes crear un archivo `cookies.txt` (formato Netscape, exportado con una extensión del navegador como "Get cookies.txt") en la misma carpeta que `Descargador-Musica.exe`. La app lo detectará automáticamente y lo usará para autenticarse.

## Desarrollo con Docker

Si eres desarrollador y quieres modificar la app:

1. Asegúrate de tener Docker instalado.
2. Ejecuta `docker-compose up -d --build`.
3. Entra en el contenedor: `docker-compose exec app bash`.
4. Ejecuta la app (se abrirá automáticamente en modo web):
   ```bash
   python src/main.py
   ```
5. Abre en tu navegador: `http://localhost:8550`

### Empaquetado

Para crear el ejecutable de Windows (ejecutar en un entorno Windows):

```bash
pip install -r requirements.txt
python -m PyInstaller --noconsole --onefile --name "Descargador-Musica" --add-data "src;src" src/main.py
```

