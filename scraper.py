import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import time
import random


class Scraper:
    """Scrape des informations sur les films depuis un site torrent."""
    
    # User-Agents pour rotation
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    ]
    
    def __init__(self, site_url):
        """
        Args:
            site_url: URL de base du site à scraper
        """
        self.site_url = site_url
        
        # Session réutilisable avec connection pooling
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': random.choice(self.USER_AGENTS)})
        
        # Configuration du pool de connexions
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=10,
            max_retries=requests.adapters.Retry(
                total=2,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504]
            )
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        self.last_request_time = 0
        self.min_request_interval = 0.5  # 500ms entre les requêtes

    def _rate_limit(self):
        """Respecte le délai minimum entre les requêtes."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def fetch_search_results(self, query):
        """
        Recherche des films par requête.
        
        Returns:
            list: Liste des résultats avec 'nom' et 'lien_detail'
        """
        self._rate_limit()
        url = f"{self.site_url}/recherche/{quote(query)}"
        try:
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Erreur lors de la recherche: {e}")
            return []
            
        soup = BeautifulSoup(response.content, "html.parser")

        results = []
        seen = set()
        for lien in soup.find_all("a", limit=30):
            href = lien.get("href")
            if href and href.startswith("/detail"):
                detail_url = urljoin(self.site_url, href)
                if detail_url in seen:
                    continue
                seen.add(detail_url)
                name = lien.get_text(strip=True) or detail_url
                results.append({"nom": name, "lien_detail": detail_url})

        return results

    def fetch_detail_info(self, url_detail, preload=False):
        """
        Récupère les détails d'un film (titre, image, lien torrent).
        
        Args:
            url_detail: URL de la page détail
            preload: Si True, précharge l'image
            
        Returns:
            dict ou None: Détails du film ou None si pas de torrent trouvé
        """
        self._rate_limit()
        try:
            response = self.session.get(url_detail, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Erreur lors de la récupération des détails: {e}")
            return None
            
        soup = BeautifulSoup(response.content, "html.parser")

        titre = soup.title.text.strip() if soup.title else "Titre inconnu"
        image_url = None

        # Chercher d'abord dans bigcover
        bigcover = soup.find("div", id="bigcover")
        if bigcover:
            img = bigcover.find("img")
            if img and img.get("src"):
                image_url = urljoin(url_detail, img.get("src"))

        # Fallback: première image valide
        if not image_url:
            for img in soup.find_all("img", limit=10):
                src = img.get("src")
                if src:
                    try:
                        image_url = urljoin(url_detail, src)
                        break
                    except Exception as e:
                        print(f"⚠️  URL image invalide: {e}")
                        continue

        # Chercher le lien torrent
        torrent_url = None
        for a in soup.find_all("a"):
            href = a.get("href")
            if href and "get_torrents" in href:
                torrent_url = urljoin(url_detail, href)
                break

        if not torrent_url:
            return None

        result = {"titre": titre, "lien_get_torrent": torrent_url, "image_url": image_url, "image_bytes": None}

        if preload and image_url:
            try:
                self._rate_limit()
                image_response = self.session.get(image_url, timeout=8)
                image_response.raise_for_status()
                result["image_bytes"] = image_response.content
            except requests.RequestException as e:
                print(f"⚠️  Erreur lors du préchargement de l'image: {e}")
                result["image_bytes"] = None

        return result