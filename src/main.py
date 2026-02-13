import flet as ft
from downloader import Downloader
from updater import Updater
import os

# Configuration
REPO_OWNER = "AdrianMP-02"
REPO_NAME = "descargador-musica"
CURRENT_VERSION = "v1.3.0"

def main(page: ft.Page):
    page.title = "Descargador de Música y Vídeo"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 600
    page.window.height = 500
    page.window.resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 40

    downloader = Downloader()
    updater = Updater(REPO_OWNER, REPO_NAME, CURRENT_VERSION)

    # UI Components
    url_input = ft.TextField(
        label="Pega aquí el enlace de YouTube",
        width=500,
        border_radius=15,
        text_size=20,
        focused_border_color=ft.Colors.RED_400,
    )

    status_text = ft.Text(
        value="Introduce un enlace para comenzar",
        size=16,
        color=ft.Colors.GREY_400,
        text_align=ft.TextAlign.CENTER,
    )

    progress_bar = ft.ProgressBar(
        width=500,
        value=0,
        visible=False,
        color=ft.Colors.RED_400,
    )

    def on_progress(d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                progress_bar.value = float(p) / 100
            except:
                pass
            page.update()

    def download_click(e):
        url = url_input.value
        if not url:
            status_text.value = "❌ Por favor, inserta un enlace."
            status_text.color = ft.Colors.RED_400
            page.update()
            return

        is_mp3 = e.control.data == "mp3"
        status_text.value = f"⏳ Descargando {'Audio' if is_mp3 else 'Vídeo'}..."
        status_text.color = ft.Colors.BLUE_400
        progress_bar.visible = True
        progress_bar.value = 0
        page.update()

        try:
            if is_mp3:
                downloader.download_mp3(url, progress_hooks=[on_progress])
            else:
                downloader.download_mp4(url, progress_hooks=[on_progress])
            
            status_text.value = "✅ ¡Descarga completada!"
            status_text.color = ft.Colors.GREEN_400
            url_input.value = ""
        except Exception as ex:
            status_text.value = f"❌ Error: {str(ex)[:50]}..."
            status_text.color = ft.Colors.RED_400
        
        progress_bar.visible = False
        page.update()

    # Buttons
    btn_mp3 = ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.MUSIC_NOTE, color=ft.Colors.WHITE),
                ft.Text("Escuchar (MP3)", size=22, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click=download_click,
        data="mp3",
        height=70,
        width=240,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED_600,
            shape=ft.RoundedRectangleBorder(radius=15),
        )
    )

    btn_mp4 = ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.VIDEOCAM, color=ft.Colors.WHITE),
                ft.Text("Ver (MP4)", size=22, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click=download_click,
        data="mp4",
        height=70,
        width=240,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            shape=ft.RoundedRectangleBorder(radius=15),
        )
    )

    # Layout
    page.add(
        ft.Column(
            controls=[
                ft.Icon(ft.Icons.ONDEMAND_VIDEO_ROUNDED, size=80, color=ft.Colors.RED_400),
                ft.Text("Descargador Musica", size=32, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                url_input,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    controls=[btn_mp3, btn_mp4],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                progress_bar,
                status_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # Check for updates on startup
    update_info = updater.check_for_updates()
    if update_info:
        def close_banner(e):
            page.banner.open = False
            page.update()

        page.banner = ft.Banner(
            bgcolor=ft.Colors.AMBER_100,
            leading=ft.Icon(ft.Icons.UPGRADE, color=ft.Colors.AMBER, size=40),
            content=ft.Text(f"¡Hay una nueva versión disponible! ({update_info['new_version']})", color=ft.Colors.BLACK),
            actions=[
                ft.TextButton(content=ft.Text("Actualizar ahora"), on_click=lambda _: page.launch_url(update_info['download_url'])),
                ft.TextButton(content=ft.Text("Cerrar"), on_click=close_banner),
            ],
        )
        page.banner.open = True
        page.update()

if __name__ == "__main__":
    if os.getenv("FLET_WEB_MODE") == "1":
        # Use ft.run for consistency in 1.0 (0.80.0+)
        ft.run(main, view=ft.AppView.WEB_BROWSER, port=8550)
    else:
        ft.run(main)
