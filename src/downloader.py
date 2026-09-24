import yt_dlp
import os
import sys

def get_base_path():
    """Returns the base path for resources, handles PyInstaller's --onefile mode"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Downloader:
    def __init__(self, download_path="Musica Descargada"):
        self.download_path = download_path
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

        # Detect FFmpeg location
        base_path = get_base_path()
        self.ffmpeg_path = os.path.join(base_path, "bin")
        if not os.path.exists(os.path.join(self.ffmpeg_path, "ffmpeg.exe")):
            # Fallback to current working directory or system PATH
            self.ffmpeg_path = None

        # Optional cookies file (Netscape format) placed next to the executable.
        # Required by YouTube for some videos/accounts once bot-verification kicks in.
        cookies_file = os.path.join(base_path, "cookies.txt")
        self.cookies_path = cookies_file if os.path.exists(cookies_file) else None

    def _base_opts(self):
        """Options shared by every yt-dlp call, tuned for YouTube's current
        bot-verification and signature-cipher rollout."""
        opts = {
            # Try multiple player clients; if one gets blocked by YouTube's
            # bot check or lacks a working signature cipher, fall back to the next.
            'extractor_args': {
                'youtube': {'player_client': ['android', 'web', 'tv']},
            },
            'retries': 10,
            'fragment_retries': 10,
            'nocheckcertificate': True,
        }
        if self.ffmpeg_path:
            opts['ffmpeg_location'] = self.ffmpeg_path
        if self.cookies_path:
            opts['cookiefile'] = self.cookies_path
        return opts

    def get_info(self, url):
        """Retrieves video information without downloading"""
        ydl_opts = self._base_opts()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown Title'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
            }

    def download_mp3(self, url, progress_hooks=None):
        """Downloads audio and converts it to MP3"""
        ydl_opts = self._base_opts()
        ydl_opts.update({
            'format': 'bestaudio/best',
            'noplaylist': True,
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': progress_hooks or [],
        })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def download_mp4(self, url, progress_hooks=None):
        """Downloads video and audio in MP4 format"""
        ydl_opts = self._base_opts()
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'noplaylist': True,
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': progress_hooks or [],
        })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

