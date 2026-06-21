import customtkinter as ctk
import webbrowser
import threading


class ResultsList:
    """Manages the results list display"""
    
    def __init__(self, listbox_frame):
        self.listbox_frame = listbox_frame
        self.buttons = []
        self.results = []

    def populate(self, results, on_select_callback):
        self.clear()
        self.results = results
        
        for index, item in enumerate(self.results, start=1):
            button = ctk.CTkButton(
                self.listbox_frame,
                text=f"{index}. {item['nom']}",
                anchor="w",
                command=lambda idx=index - 1: on_select_callback(idx),
                width=520,
                fg_color="#1f6aa5",
                hover_color="#2a83cf",
                corner_radius=10
            )
            button.pack(fill="x", padx=10, pady=6)
            self.buttons.append(button)

    def clear(self):
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
        self.results.clear()


class DetailPanel:
    """Manages the detail panel display"""
    
    def __init__(self, poster_label, title_label, detail_url_label, torrent_url_label, 
                 open_detail_button, open_torrent_button):
        self.poster_label = poster_label
        self.title_label = title_label
        self.detail_url_label = detail_url_label
        self.torrent_url_label = torrent_url_label
        self.open_detail_button = open_detail_button
        self.open_torrent_button = open_torrent_button

    def update(self, detail, item_detail_url):
        self.title_label.configure(text=f"Titre : {detail['titre']}")
        self.detail_url_label.configure(text=f"Lien détail : {item_detail_url}")
        self.torrent_url_label.configure(text=f"Lien get torrent : {detail['lien_get_torrent']}")
        self.open_detail_button.configure(command=lambda url=item_detail_url: self.open_url(url), state="normal")
        self.open_torrent_button.configure(command=lambda url=detail["lien_get_torrent"]: self.open_url(url), state="normal")

    def clear(self):
        self.title_label.configure(text="Titre : -")
        self.detail_url_label.configure(text="Lien détail : -")
        self.torrent_url_label.configure(text="Lien get torrent : -")
        self.open_detail_button.configure(state="disabled")
        self.open_torrent_button.configure(state="disabled")

    @staticmethod
    def open_url(url):
        webbrowser.open_new_tab(url)


class LoadingOverlay:
    """Manages the loading overlay display"""
    
    def __init__(self, overlay, label):
        self.overlay = overlay
        self.label = label

    def show(self, text="Chargement..."):
        self.label.configure(text=text, text_color="white")
        self.overlay.lift()
        self.overlay.update()

    def hide(self):
        self.overlay.lower()