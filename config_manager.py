import json
import os

CONFIG_FILE = "mouvie_gui_config.json"
DEFAULT_SITE = "https://www.cpasbien3.cc/"


class ConfigManager:
    """Gère la configuration de l'application (URL du site de scraping)."""
    
    def __init__(self):
        """Initialise le gestionnaire de configuration."""
        self.site_url = DEFAULT_SITE
        self.load()

    def load(self):
        """Charge la configuration depuis le fichier JSON."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.site_url = data.get("site_url", DEFAULT_SITE)
            except Exception:
                self.site_url = DEFAULT_SITE

    def save(self, site_url):
        """
        Sauvegarde la configuration.
        
        Returns:
            tuple: (succès: bool, message: str)
        """
        self.site_url = site_url or DEFAULT_SITE
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump({"site_url": self.site_url}, f, indent=4, ensure_ascii=False)
            return True, "URL du site sauvegardée."
        except Exception as exc:
            return False, f"Erreur sauvegarde : {exc}"