import requests
import os
import sys

class Updater:
    def __init__(self, repo_owner, repo_name, current_version):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    def check_for_updates(self):
        """Checks GitHub for a newer version"""
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                latest_release = response.json()
                latest_version = latest_release.get('tag_name')
                if latest_version and latest_version != self.current_version:
                    return {
                        'new_version': latest_version,
                        'download_url': self._get_exe_download_url(latest_release),
                        'release_notes': latest_release.get('body', '')
                    }
        except Exception as e:
            print(f"Error checking updates: {e}")
        return None

    def _get_exe_download_url(self, release_info):
        """Finds the .exe asset in the release info"""
        assets = release_info.get('assets', [])
        for asset in assets:
            if asset.get('name', '').endswith('.exe'):
                return asset.get('browser_download_url')
        return None

    def download_and_install(self, download_url):
        """
        In a real scenario, this would download the new EXE and 
        potentially replace the current one or launch an installer.
        For now, this returns the URL to be handled by the UI.
        """
        return download_url
