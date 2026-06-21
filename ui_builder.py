import customtkinter as ctk


class UIBuilder:
    """Constructs and manages the application UI layout"""
    
    @staticmethod
    def build_top_frame(parent):
        top_frame = ctk.CTkFrame(parent, corner_radius=0)
        top_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        search_entry = ctk.CTkEntry(top_frame, placeholder_text="Entrez votre recherche...", width=350)
        search_entry.pack(side="left", padx=(0, 10), pady=10)
        
        search_button = ctk.CTkButton(top_frame, text="Rechercher")
        search_button.pack(side="left", padx=(0, 10), pady=10)
        
        status_label = ctk.CTkLabel(top_frame, text="Prêt.")
        status_label.pack(side="left", padx=(10, 0), pady=10)
        
        return {"frame": top_frame, "search_entry": search_entry, "search_button": search_button, "status_label": status_label}

    @staticmethod
    def build_loading_overlay(parent):
        loading_overlay = ctk.CTkFrame(parent, fg_color="#000000", corner_radius=0)
        loading_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        loading_overlay.lower()
        
        loading_label = ctk.CTkLabel(loading_overlay, text="Chargement...", font=ctk.CTkFont(size=24, weight="bold"))
        loading_label.place(relx=0.5, rely=0.5, anchor="center")
        
        return {"overlay": loading_overlay, "label": loading_label}

    @staticmethod
    def build_content_frame(parent):
        content_frame = ctk.CTkFrame(parent)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        tabview = ctk.CTkTabview(content_frame)
        tabview.pack(fill="both", expand=True)
        tabview.add("Torrent")
        tabview.add("1fichier.com")
        
        torrent_tab = tabview.tab("Torrent")
        fichier_tab = tabview.tab("1fichier.com")
        
        coming_soon = ctk.CTkLabel(fichier_tab, text="Coming soon", font=ctk.CTkFont(size=24, weight="bold"))
        coming_soon.place(relx=0.5, rely=0.5, anchor="center")
        
        return {"frame": content_frame, "torrent_tab": torrent_tab, "fichier_tab": fichier_tab}

    @staticmethod
    def build_site_frame(parent):
        site_frame = ctk.CTkFrame(parent)
        site_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=12, pady=(12, 0))
        
        site_entry = ctk.CTkEntry(site_frame, placeholder_text="URL du site", width=450)
        site_entry.pack(side="left", padx=(0, 10), pady=10)
        
        save_button = ctk.CTkButton(site_frame, text="Sauvegarder")
        save_button.pack(side="left", padx=(0, 10), pady=10)
        
        return {"frame": site_frame, "site_entry": site_entry, "save_button": save_button}

    @staticmethod
    def build_left_panel(parent):
        left_frame = ctk.CTkFrame(parent)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=10)
        
        header = ctk.CTkLabel(left_frame, text="Résultats", font=ctk.CTkFont(size=18, weight="bold"))
        header.pack(anchor="w", padx=12, pady=(12, 6))
        
        listbox_frame = ctk.CTkFrame(left_frame)
        listbox_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
        result_listbox = ctk.CTkScrollableFrame(listbox_frame, corner_radius=10)
        result_listbox.pack(fill="both", expand=True)
        
        return {"frame": left_frame, "listbox_frame": listbox_frame, "result_listbox": result_listbox}

    @staticmethod
    def build_right_panel(parent):
        right_frame = ctk.CTkFrame(parent)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=10)
        
        header = ctk.CTkLabel(right_frame, text="Détails sélectionnés", font=ctk.CTkFont(size=18, weight="bold"))
        header.pack(anchor="w", padx=12, pady=(12, 6))
        
        poster_label = ctk.CTkLabel(right_frame, text="Aucune image", width=300, height=300, corner_radius=10)
        poster_label.pack(padx=12, pady=(0, 12))
        
        title_label = ctk.CTkLabel(right_frame, text="Titre : -", wraplength=520, justify="left")
        title_label.pack(anchor="w", padx=12, pady=(0, 6))
        
        detail_url_label = ctk.CTkLabel(right_frame, text="Lien détail : -", wraplength=520, justify="left")
        detail_url_label.pack(anchor="w", padx=12, pady=(0, 6))
        
        torrent_url_label = ctk.CTkLabel(right_frame, text="Lien get torrent : -", wraplength=520, justify="left")
        torrent_url_label.pack(anchor="w", padx=12, pady=(0, 6))
        
        button_frame = ctk.CTkFrame(right_frame)
        button_frame.pack(fill="x", padx=12, pady=(10, 0))
        
        open_detail_button = ctk.CTkButton(button_frame, text="Ouvrir lien détail", state="disabled")
        open_detail_button.pack(side="left", expand=True, padx=(0, 8))
        
        open_torrent_button = ctk.CTkButton(button_frame, text="Ouvrir get torrent", state="disabled")
        open_torrent_button.pack(side="left", expand=True, padx=(8, 0))
        
        scroll_status = ctk.CTkLabel(right_frame, text="", wraplength=520, justify="left")
        scroll_status.pack(anchor="w", padx=12, pady=(10, 0))
        
        return {
            "frame": right_frame,
            "poster_label": poster_label,
            "title_label": title_label,
            "detail_url_label": detail_url_label,
            "torrent_url_label": torrent_url_label,
            "open_detail_button": open_detail_button,
            "open_torrent_button": open_torrent_button,
            "scroll_status": scroll_status
        }

    @staticmethod
    def configure_grid(torrent_tab, content_frame):
        torrent_tab.grid_columnconfigure(0, weight=1)
        torrent_tab.grid_columnconfigure(1, weight=2)
        torrent_tab.grid_rowconfigure(0, weight=0)
        torrent_tab.grid_rowconfigure(1, weight=1)
        
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)