import os
import json
import hashlib
import urllib.request
import urllib.error
import shutil
import subprocess
import sys
from pathlib import Path


class AppUpdater:
    def __init__(self, repo_owner, repo_name, local_version_file="VERSION.txt"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.version_file = local_version_file
        self.local_version = self.read_local_version()
        self.github_api = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        
    def read_local_version(self):
        if os.path.exists(self.version_file):
            with open(self.version_file, 'r') as f:
                return f.read().strip()
        return "0.0.0"
    
    def get_remote_version(self):
        try:
            url = f"{self.github_api}/contents/VERSION.txt"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                content = data.get('content', '')
                import base64
                return base64.b64decode(content).decode().strip()
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de la version distante: {e}")
            return None
    
    def get_file_hash(self, filepath):
        if not os.path.exists(filepath):
            return None
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def get_remote_files(self):
        try:
            url = f"{self.github_api}/contents"
            with urllib.request.urlopen(url) as response:
                files = json.loads(response.read().decode())
                return {f['name']: f['download_url'] for f in files if f['type'] == 'file'}
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des fichiers: {e}")
            return {}
    
    def get_remote_file_hash(self, filename):
        try:
            url = f"{self.github_api}/contents/{filename}"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                import base64
                content = base64.b64decode(data.get('content', '')).decode()
                return hashlib.sha256(content.encode()).hexdigest()
        except Exception:
            return None
    
    def download_file(self, filename, download_url):
        try:
            print(f"⬇️  Téléchargement de {filename}...")
            urllib.request.urlretrieve(download_url, filename)
            print(f"✅ {filename} téléchargé avec succès")
            return True
        except Exception as e:
            print(f"❌ Erreur lors du téléchargement de {filename}: {e}")
            return False
    
    def check_and_update(self):
        print("🔍 Vérification des mises à jour...")
        
        remote_version = self.get_remote_version()
        if remote_version is None:
            print("⚠️  Impossible de vérifier les mises à jour (pas de connexion)")
            return False
        
        print(f"📦 Version locale: {self.local_version}")
        print(f"📦 Version distante: {remote_version}")
        
        if remote_version == self.local_version:
            print("✅ Vous avez la dernière version!")
            return False
        
        print(f"🔄 Une nouvelle version est disponible ({remote_version})")
        return self.update_files()
    
    def update_files(self):
        remote_files = self.get_remote_files()
        
        if not remote_files:
            print("❌ Impossible de récupérer la liste des fichiers")
            return False
        
        updated_count = 0
        
        for filename in remote_files:
            if filename == "launcher.py" or filename == ".git":
                continue
            
            local_hash = self.get_file_hash(filename)
            remote_hash = self.get_remote_file_hash(filename)
            
            if local_hash != remote_hash:
                print(f"🔄 {filename} a changé, mise à jour...")
                if self.download_file(filename, remote_files[filename]):
                    updated_count += 1
        
        # Mettre à jour VERSION.txt
        remote_version = self.get_remote_version()
        if remote_version:
            with open("VERSION.txt", 'w') as f:
                f.write(remote_version)
            updated_count += 1
        
        if updated_count > 0:
            print(f"✅ {updated_count} fichier(s) mis à jour")
            return True
        
        return False


def launch_app():
    try:
        print("\n🚀 Lancement de l'application...")
        subprocess.run([sys.executable, "mouvie_gui.py"], check=True)
    except FileNotFoundError:
        print("❌ mouvie_gui.py introuvable!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # À CONFIGURER: nom du propriétaire et du repo GitHub
    REPO_OWNER = "devunity53"  # À remplacer par votre username GitHub
    REPO_NAME = "mouvie-scraper"  # À remplacer par le nom de votre repo
    
    print("=" * 50)
    print("🎬 Mouvie Scraper Launcher")
    print("=" * 50)
    
    updater = AppUpdater(REPO_OWNER, REPO_NAME)
    updater.check_and_update()
    
    print()
    launch_app()