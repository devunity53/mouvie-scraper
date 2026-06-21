import customtkinter as ctk
import threading
from config_manager import ConfigManager, DEFAULT_SITE
from scraper import Scraper
from image_handler import ImageHandler
from ui_builder import UIBuilder
from ui_components import ResultsList, DetailPanel, LoadingOverlay


class MouvieApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mouvie Search")
        self.geometry("1100x700")
        self.minsize(1000, 650)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")

        self.config_manager = ConfigManager()
        self.scraper = Scraper(self.config_manager.site_url)

        self.results = []
        self.detail_cache = {}
        self.cache_lock = threading.Lock()

        self._build_ui()

    def _build_ui(self):
        top_components = UIBuilder.build_top_frame(self)
        self.search_entry = top_components["search_entry"]
        search_button = top_components["search_button"]
        self.status_label = top_components["status_label"]
        search_button.configure(command=self.perform_search)

        loading_components = UIBuilder.build_loading_overlay(self)
        self.loading_overlay = LoadingOverlay(loading_components["overlay"], loading_components["label"])

        content_components = UIBuilder.build_content_frame(self)
        torrent_tab = content_components["torrent_tab"]

        site_components = UIBuilder.build_site_frame(torrent_tab)
        self.site_entry = site_components["site_entry"]
        self.site_entry.insert(0, self.config_manager.site_url)
        save_button = site_components["save_button"]
        save_button.configure(command=self.save_site_url)

        left_components = UIBuilder.build_left_panel(torrent_tab)
        right_components = UIBuilder.build_right_panel(torrent_tab)

        self.results_list = ResultsList(left_components["result_listbox"])
        self.detail_panel = DetailPanel(
            right_components["poster_label"],
            right_components["title_label"],
            right_components["detail_url_label"],
            right_components["torrent_url_label"],
            right_components["open_detail_button"],
            right_components["open_torrent_button"]
        )

        self.image_handler = ImageHandler(right_components["poster_label"])

        UIBuilder.configure_grid(torrent_tab, content_components["frame"])

    def perform_search(self):
        query = self.search_entry.get().strip()
        if not query:
            self.status_label.configure(text="Veuillez entrer une recherche.")
            return

        self.update_site_url()
        self.status_label.configure(text="Recherche en cours...")
        self.clear_results()
        self.detail_cache.clear()
        self.loading_overlay.show("Recherche en cours...")

        try:
            self.results = self.scraper.fetch_search_results(query)
            if not self.results:
                self.status_label.configure(text="Aucun résultat trouvé.")
                return

            self.status_label.configure(text=f"{len(self.results)} résultats trouvés.")
            self.results_list.populate(self.results, self.select_result)
            self.preload_detail_infos()
        except Exception as exc:
            self.status_label.configure(text=f"Erreur : {exc}")
        finally:
            self.loading_overlay.hide()

    def clear_results(self):
        self.results_list.clear()
        self.detail_panel.clear()
        self.image_handler.clear()

    def update_site_url(self):
        url = self.site_entry.get().strip() or DEFAULT_SITE
        self.config_manager.site_url = url
        self.scraper.site_url = url

    def save_site_url(self):
        self.update_site_url()
        success, message = self.config_manager.save(self.config_manager.site_url)
        self.status_label.configure(text=message)

    def preload_detail_infos(self):
        max_items = min(10, len(self.results))
        if max_items == 0:
            return

        thread = threading.Thread(target=self._preload_detail_worker, args=(max_items,), daemon=True)
        thread.start()

    def _preload_detail_worker(self, max_items):
        for idx in range(max_items):
            item = self.results[idx]
            try:
                detail = self.scraper.fetch_detail_info(item["lien_detail"], preload=True)
                with self.cache_lock:
                    self.detail_cache[idx] = detail
            except Exception:
                pass

    def select_result(self, index):
        item = self.results[index]
        self.status_label.configure(text=f"Chargement du détail pour {item['nom']}...")
        self.loading_overlay.show("Chargement du détail...")

        with self.cache_lock:
            detail = self.detail_cache.get(index)

        if detail is None:
            detail = self.scraper.fetch_detail_info(item["lien_detail"], preload=True)
            if detail:
                with self.cache_lock:
                    self.detail_cache[index] = detail

        self.loading_overlay.hide()

        if not detail:
            self.status_label.configure(text="Aucun lien get torrent trouvé.")
            return

        self.detail_panel.update(detail, item['lien_detail'])

        if detail.get("image_bytes"):
            self.image_handler.load_from_bytes(detail["image_bytes"])
        elif detail.get("image_url"):
            self.image_handler.load_from_url(detail["image_url"])
        else:
            self.image_handler.display_no_image()

        self.status_label.configure(text="Détail chargé.")


if __name__ == "__main__":
    app = MouvieApp()
    app.mainloop()