import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin


class Scraper:
    def __init__(self, site_url):
        self.site_url = site_url

    def fetch_search_results(self, query):
        url = f"{self.site_url}/recherche/{quote(query)}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        results = []
        seen = set()
        for lien in soup.find_all("a"):
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
        response = requests.get(url_detail, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        titre = soup.title.text.strip() if soup.title else "Titre inconnu"
        image_url = None

        bigcover = soup.find("div", id="bigcover")
        if bigcover:
            img = bigcover.find("img")
            if img and img.get("src"):
                image_url = urljoin(url_detail, img.get("src"))

        if not image_url:
            for img in soup.find_all("img"):
                src = img.get("src")
                if src:
                    image_url = urljoin(url_detail, src)
                    break

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
                image_response = requests.get(image_url, timeout=10)
                image_response.raise_for_status()
                result["image_bytes"] = image_response.content
            except Exception:
                result["image_bytes"] = None

        return result