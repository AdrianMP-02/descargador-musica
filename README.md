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

1. Abre la aplicación `DescargadorFacil.exe`.
2. Copia el enlace del vídeo de YouTube que quieras descargar.
3. Pégalo en el cuadro de texto central.
4. Haz clic en el botón rojo **"Escuchar (MP3)"** si quieres la canción, o en el botón azul **"Ver (MP4)"** si quieres el vídeo.
5. ¡Listo! El archivo se guardará en la carpeta `downloads` junto al programa.

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
python -m PyInstaller --noconsole --onefile --name "DescargadorFacil" --add-data "src;src" src/main.py
```

