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

    def get_info(self, url):
        """Retrieves video information without downloading"""
        ydl_opts = {}
        if self.ffmpeg_path:
            ydl_opts['ffmpeg_location'] = self.ffmpeg_path
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown Title'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
            }

    def download_mp3(self, url, progress_hooks=None):
        """Downloads audio and converts it to MP3"""
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': progress_hooks or [],
        }
        if self.ffmpeg_path:
            ydl_opts['ffmpeg_location'] = self.ffmpeg_path

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def download_mp4(self, url, progress_hooks=None):
        """Downloads video and audio in MP4 format"""
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'noplaylist': True,
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': progress_hooks or [],
        }
        if self.ffmpeg_path:
            ydl_opts['ffmpeg_location'] = self.ffmpeg_path

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

