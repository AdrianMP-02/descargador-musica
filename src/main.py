import flet as ft
from downloader import Downloader
from updater import Updater
import os
import asyncio

# Configuration
REPO_OWNER = "AdrianMP-02"
REPO_NAME = "descargador-musica"
CURRENT_VERSION = "v1.0.0"

async def main(page: ft.Page):
    page.title = "Descargador de Música y Vídeo"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 600
    page.window.height = 500
    page.window.resizable = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 40

    downloader = Downloader()
    updater = Updater(REPO_OWNER, REPO_NAME, CURRENT_VERSION)

    # Shared state for progress (set by worker thread, read by async poller)
    progress_state = {"percent": 0, "text": "", "done": False, "error": None}

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

    # Buttons
    btn_mp3 = ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.MUSIC_NOTE, color=ft.Colors.WHITE),
                ft.Text("Escuchar (MP3)", size=22, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click=lambda e: page.run_task(download_click, e),
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
        on_click=lambda e: page.run_task(download_click, e),
        data="mp4",
        height=70,
        width=240,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            shape=ft.RoundedRectangleBorder(radius=15),
        )
    )

    def on_progress(d):
        """Called by yt-dlp in the worker thread — only writes to shared dict"""
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            if total > 0:
                pct = min(downloaded / total, 1.0)
                mb_down = downloaded / (1024 * 1024)
                mb_total = total / (1024 * 1024)
                progress_state["percent"] = pct
                progress_state["text"] = f"⏳ Descargando... {int(pct * 100)}% ({mb_down:.0f}/{mb_total:.0f} MB)"
            else:
                mb_down = downloaded / (1024 * 1024)
                progress_state["text"] = f"⏳ Descargando... {mb_down:.1f} MB"
        elif d['status'] == 'finished':
            progress_state["percent"] = 1.0
            progress_state["text"] = "⏳ Procesando archivo..."

    async def download_click(e):
        url = url_input.value
        if not url:
            status_text.value = "❌ Por favor, inserta un enlace."
            status_text.color = ft.Colors.RED_400
            page.update()
            return

        is_mp3 = e.control.data == "mp3"

        # Disable buttons
        btn_mp3.disabled = True
        btn_mp4.disabled = True
        progress_state["done"] = False
        progress_state["error"] = None
        progress_state["percent"] = 0
        progress_state["text"] = f"⏳ Preparando {'Audio' if is_mp3 else 'Vídeo'}..."
        status_text.value = progress_state["text"]
        status_text.color = ft.Colors.BLUE_400
        progress_bar.visible = True
        progress_bar.value = 0
        page.update()

        # Run the blocking download in a thread pool
        loop = asyncio.get_event_loop()

        def do_download():
            try:
                if is_mp3:
                    downloader.download_mp3(url, progress_hooks=[on_progress])
                else:
                    downloader.download_mp4(url, progress_hooks=[on_progress])
                progress_state["done"] = True
            except Exception as ex:
                progress_state["error"] = str(ex)[:80]
                progress_state["done"] = True

        # Start blocking work in thread pool
        download_future = loop.run_in_executor(None, do_download)

        # Poll progress from the async event loop — this is the key pattern
        while not progress_state["done"]:
            await asyncio.sleep(0.3)
            progress_bar.value = progress_state["percent"]
            status_text.value = progress_state["text"]
            page.update()

        # Wait for thread to finish cleanly
        await download_future

        # Final state
        if progress_state["error"]:
            status_text.value = f"❌ Error: {progress_state['error']}"
            status_text.color = ft.Colors.RED_400
        else:
            status_text.value = "✅ ¡Descarga completada!"
            status_text.color = ft.Colors.GREEN_400
            url_input.value = ""

        progress_bar.visible = False
        btn_mp3.disabled = False
        btn_mp4.disabled = False
        page.update()

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

    # --- Auto-Update Check (async) ---
    async def check_updates():
        try:
            loop = asyncio.get_event_loop()
            update_info = await loop.run_in_executor(
                None, updater.check_for_updates
            )
            if update_info and update_info.get('download_url'):
                async def start_update(e):
                    page.banner.actions = [ft.Text("Descargando...")]
                    page.update()

                    update_state = {"progress": 0, "done": False, "result": None}

                    def update_progress(p):
                        update_state["progress"] = p

                    def do_update_download():
                        result = updater.download_file(
                            update_info['download_url'], update_progress
                        )
                        update_state["result"] = result
                        update_state["done"] = True

                    loop2 = asyncio.get_event_loop()
                    download_future = loop2.run_in_executor(None, do_update_download)

                    while not update_state["done"]:
                        await asyncio.sleep(0.5)
                        pct = int(update_state["progress"] * 100)
                        page.banner.content = ft.Text(
                            f"Descargando actualización: {pct}%",
                            color=ft.Colors.BLACK,
                        )
                        page.update()

                    await download_future

                    if update_state["result"]:
                        page.banner.bgcolor = ft.Colors.GREEN_100
                        page.banner.leading = ft.Icon(
                            ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=40
                        )
                        page.banner.content = ft.Text(
                            f"✅ Descargado: {update_state['result']}. Cierra la app y ejecútalo.",
                            color=ft.Colors.BLACK,
                        )
                        page.banner.actions = [
                            ft.TextButton("Entendido", on_click=close_banner)
                        ]
                    else:
                        page.banner.bgcolor = ft.Colors.RED_100
                        page.banner.content = ft.Text(
                            "❌ Error al descargar la actualización.",
                            color=ft.Colors.BLACK,
                        )
                        page.banner.actions = [
                            ft.TextButton("Reintentar", on_click=lambda e: page.run_task(start_update, e)),
                            ft.TextButton("Cerrar", on_click=close_banner),
                        ]
                    page.update()

                async def close_banner(e):
                    page.banner.open = False
                    page.update()

                page.banner = ft.Banner(
                    bgcolor=ft.Colors.AMBER_100,
                    leading=ft.Icon(ft.Icons.UPGRADE, color=ft.Colors.AMBER, size=40),
                    content=ft.Text(
                        f"¡Nueva versión disponible! ({update_info['new_version']})",
                        color=ft.Colors.BLACK,
                    ),
                    actions=[
                        ft.TextButton("Actualizar ahora", on_click=lambda e: page.run_task(start_update, e)),
                        ft.TextButton("Cerrar", on_click=close_banner),
                    ],
                )
                page.banner.open = True
                page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error comprobando actualizaciones: {str(ex)[:60]}"),
                bgcolor=ft.Colors.RED_200,
            )
            page.snack_bar.open = True
            page.update()

    # Launch update check
    page.run_task(check_updates)

if __name__ == "__main__":
    if os.getenv("FLET_WEB_MODE") == "1":
        ft.app(main, view=ft.AppView.WEB_BROWSER, port=8550)
    else:
        ft.app(main)
