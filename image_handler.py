import requests
from PIL import Image
from io import BytesIO
import customtkinter as ctk
from cache_manager import CacheManager


class ImageHandler:
    """Gère le chargement et l'affichage des images de film avec cache disque."""
    
    def __init__(self, poster_label):
        """
        Args:
            poster_label: Widget CTkLabel pour afficher l'image
        """
        self.poster_label = poster_label
        self.current_image = None
        CacheManager.ensure_cache_dir()

    def load_from_url(self, image_url):
        """Charge une image depuis une URL (avec cache disque)."""
        if not image_url:
            self.display_no_image()
            return

        # Vérifier le cache disque d'abord
        cached_bytes = CacheManager.get_cached_image(image_url)
        if cached_bytes:
            print(f"📦 Image chargée depuis le cache")
            self.load_from_bytes(cached_bytes)
            return

        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            # Sauvegarder en cache pour la prochaine fois
            CacheManager.cache_image(image_url, response.content)
            self.load_from_bytes(response.content)
        except requests.RequestException as e:
            print(f"⚠️  Erreur lors du chargement de l'image: {e}")
            self.poster_label.configure(image=None, text="Image introuvable")

    def load_from_bytes(self, image_bytes):
        """Charge une image depuis des données brutes."""
        if not image_bytes:
            self.display_no_image()
            return

        try:
            image = Image.open(BytesIO(image_bytes))
            image.thumbnail((380, 380), Image.LANCZOS)
            self.current_image = ctk.CTkImage(light_image=image, dark_image=image, size=image.size)
            self.poster_label.configure(image=self.current_image, text="")
        except Exception as e:
            print(f"⚠️  Erreur lors du traitement de l'image: {e}")
            self.poster_label.configure(image=None, text="Image introuvable")

    def display_no_image(self):
        """Affiche le message "Aucune image"."""
        self.poster_label.configure(image=None, text="Aucune image")
        self.current_image = None

    def clear(self):
        """Efface l'image actuelle."""
        self.display_no_image()