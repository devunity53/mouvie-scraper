# Mouvie Scraper

Une application de scraping de films avec interface GUI moderne.

## Fonctionnalités

- 🔍 Recherche de films
- 📊 Affichage des résultats avec images
- 🔗 Accès direct aux liens de torrents
- ⚙️ Configuration du site de scraping
- 🔄 Mise à jour automatique

## Installation

1. Clonez le repository:
```bash
git clone https://github.com/devunity53/mouvie-scraper.git
cd mouvie-scraper
```

2. Installez les dépendances:
```bash
pip install -r requirements.txt
```

3. Lancez l'application:
```bash
python launcher.py
```

## Structure

```
mouvie-scraper/
├── launcher.py           # Script de lancement avec auto-update
├── mouvie_gui.py         # Application principale
├── config_manager.py     # Gestion de la configuration
├── scraper.py            # Web scraping
├── image_handler.py      # Gestion des images
├── ui_builder.py         # Construction UI
├── ui_components.py      # Composants UI
├── VERSION.txt           # Numéro de version
└── requirements.txt      # Dépendances
```

## Configuration

Éditez `config_manager.py` pour changer l'URL du site par défaut.

## Mise à jour

Le launcher vérifie automatiquement les mises à jour au démarrage et les télécharge si nécessaire.

## Licence

MIT