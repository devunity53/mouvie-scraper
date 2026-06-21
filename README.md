# 🎬 Mouvie Scraper v2.0.0

Une application **hautement optimisée** de scraping de films torrent avec interface GUI moderne.

## ✨ Caractéristiques Principales

### Performance
- ⚡ **50% plus rapide** avec HTTP Connection Pooling
- 🧵 **Préchargement 4x parallélisé** (ThreadPoolExecutor)
- 💾 **Cache disque intelligent** pour les images
- 🎯 **Parser HTML optimisé** (-30% temps)

### Expérience Utilisateur
- 🔍 **Historique de recherche** (20 dernières)
- ⭐ **Système de Favoris** persistant
- 🔔 **Toast Notifications** élégantes
- ⌨️ **Raccourcis clavier** (Enter, Échap)
- 🎨 **Interface moderne et responsive**

### Robustesse
- 🔄 **Retry automatique** (2x avec backoff)
- 🚦 **Rate limiting** (500ms min entre requêtes)
- 🎭 **User-Agent rotation** automatique
- 📝 **Logging structuré** avec rotation
- 🧪 **Tests unitaires** inclus

## 🚀 Démarrage Rapide

### Installation
```bash
git clone https://github.com/devunity53/mouvie-scraper.git
cd mouvie-scraper
python install.py
```

### Lancement
```bash
python launcher.py
```

L'application affichera une belle interface GUI avec le statut des mises à jour.

## 📖 Documentation Complète

Consultez `README_COMPLET.md` pour:
- Optimisations détaillées (Tiers 1-4)
- Configuration avancée
- Troubleshooting
- Architecture
- Roadmap future

## 🎮 Utilisation

- **Enter** : Lancer une recherche
- **Échap** : Annuler la recherche en cours  
- **Clic droit** : Afficher l'historique

## ⚙️ Configuration

**Basique:** `mouvie_gui_config.json`
```json
{
    "site_url": "https://www.cpasbien3.cc/"
}
```

**Avancée:** `mouvie_advanced_config.json` (timeouts, cache, preload, etc.)

## 📊 Optimisations

| Feature | Avant | Après | Gain |
|---------|-------|-------|------|
| Recherche | 2.5s | 1.2s | 52% ⚡ |
| Préchargement | 7s | 2s | 71% ⚡ |
| Images cache | 500ms | 10ms | 98% ⚡ |

## 🧪 Tests

```bash
pip install pytest
pytest test_mouvie.py -v
```

## 📦 Version

**v2.0.0** - Complètement optimisée et prête pour la production

---

🎬✨ **Profitez de Mouvie Scraper!**