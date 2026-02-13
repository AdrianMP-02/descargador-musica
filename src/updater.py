import requests
import os
import sys
import logging

# Configure logging to a file
logging.basicConfig(
    filename='app_debug.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Updater:
    def __init__(self, repo_owner, repo_name, current_version):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        self.headers = {
            'User-Agent': 'Descargador-Musica-App'
        }

    def check_for_updates(self):
        """Checks GitHub for a newer version"""
        try:
            logging.info(f"Checking for updates at {self.api_url}")
            response = requests.get(self.api_url, headers=self.headers, timeout=10)
            logging.info(f"GitHub API response status: {response.status_code}")
            
            if response.status_code == 200:
                latest_release = response.json()
                latest_version = latest_release.get('tag_name')
                logging.info(f"Latest version found: {latest_version} (Current: {self.current_version})")
                
                if latest_version and latest_version != self.current_version:
                    logging.info("Update found!")
                    return {
                        'new_version': latest_version,
                        'download_url': self._get_exe_download_url(latest_release),
                        'release_notes': latest_release.get('body', '')
                    }
                else:
                    logging.info("No new version available.")
            else:
                logging.error(f"Failed to check updates. Status: {response.status_code}, Body: {response.text[:100]}")
        except Exception as e:
            logging.error(f"Error checking updates: {str(e)}")
            print(f"Error checking updates: {e}")
        return None

    def _get_exe_download_url(self, release_info):
        """Finds the .exe asset in the release info"""
        assets = release_info.get('assets', [])
        for asset in assets:
            if asset.get('name', '').lower().endswith('.exe'):
                return asset.get('browser_download_url')
        return None

    def download_and_install(self, download_url):
        """
        In a real scenario, this would download the new EXE and 
        potentially replace the current one or launch an installer.
        For now, this returns the URL to be handled by the UI.
        """
        return download_url
