# 🏠 Analyse du Marché Immobilier — Web Scraping & Dashboard

Projet de scraping et d'analyse des annonces immobilières du site [Le Réflexe Notaire](https://www.lereflexenotaire.fr/petites-annonces), avec visualisation interactive via un tableau de bord Streamlit.

## 🎯 Objectifs

- Collecter automatiquement des annonces immobilières sur plusieurs pages
- Nettoyer et structurer les données (prix, surface, ville, département, etc.)
- Analyser les tendances du marché (prix moyens, prix au m²)
- Visualiser les résultats via un dashboard interactif

## 🛠️ Stack technique

- **Python** · **Requests** · **BeautifulSoup** — scraping
- **Pandas** · **Regex** — nettoyage et structuration
- **Streamlit** · **Matplotlib** · **Seaborn** — visualisation

## 📊 Fonctionnalités du dashboard

- Distribution des prix de vente par ville
- Boxplot des prix par type de bien
- Scatter plot prix au m² vs surface
- Prix moyen par département et par ville
- Export CSV des données brutes

## 🚀 Lancer le projet
```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer le scraper (génère DATA/ANNONCES_CLEAN.csv)
python scraper.py

# Lancer le dashboard
streamlit run dashboard.py
```

## 📁 Structure du projet
```
web-scraping/
├── scraper.py         # Collecte et nettoyage des données
├── dashboard.py       # Tableau de bord Streamlit
├── DATA/
│   └── ANNONCES_CLEAN.csv
├── requirements.txt
└── README.md
```

## 📦 Dépendances

requests
beautifulsoup4
pandas
streamlit
matplotlib
seaborn
```
