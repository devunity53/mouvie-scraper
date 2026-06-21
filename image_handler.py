import requests
from PIL import Image
from io import BytesIO
import customtkinter as ctk


class ImageHandler:
    def __init__(self, poster_label):
        self.poster_label = poster_label
        self.current_image = None

    def load_from_url(self, image_url):
        if not image_url:
            self.display_no_image()
            return

        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            self.load_from_bytes(response.content)
        except Exception:
            self.poster_label.configure(image=None, text="Image introuvable")

    def load_from_bytes(self, image_bytes):
        if not image_bytes:
            self.display_no_image()
            return

        try:
            image = Image.open(BytesIO(image_bytes))
            image.thumbnail((380, 380), Image.LANCZOS)
            self.current_image = ctk.CTkImage(light_image=image, dark_image=image, size=image.size)
            self.poster_label.configure(image=self.current_image, text="")
        except Exception:
            self.poster_label.configure(image=None, text="Image introuvable")

    def display_no_image(self):
        self.poster_label.configure(image=None, text="Aucune image")
        self.current_image = None

    def clear(self):
        self.display_no_image()