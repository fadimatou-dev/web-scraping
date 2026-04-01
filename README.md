# 🏠 Analyse du Marché Immobilier — Web Scraping & Dashboard

Projet de scraping et d'analyse des annonces immobilières du site [Le Réflexe Notaire](https://www.lereflexenotaire.fr/petites-annonces), avec visualisation interactive via un tableau de bord Streamlit.

## 🎯 Contexte & Objectifs
Ce projet simule un pipeline de collecte et d'analyse de données de marché à partir du site Le Réflexe Notaire, un portail d'annonces immobilières notariales françaises.
Problématique : Comment automatiser la collecte de données immobilières dispersées sur plusieurs pages web et en extraire des insights exploitables sur les tendances de prix ?
Objectifs :

✅ Scraper automatiquement des centaines d'annonces immobilières sur plusieurs pages
✅ Nettoyer et structurer les données brutes (prix, surface, ville, département, type de bien)
✅ Analyser les tendances du marché (prix moyens, prix au m², disparités régionales)
✅ Restituer les résultats via un dashboard interactif sans infrastructure serveur

## 🏗️ Architecture du Pipeline
[Source Web]          [Collecte]         [Traitement]        [Restitution]
Le Réflexe     →    scraper.py     →    clean_data.py   →   dashboard.py
Notaire             Requests /          Pandas / Regex       Streamlit /
(HTML)              BeautifulSoup       Structuration        Matplotlib /
                    Pagination          Normalisation        Seaborn
                         ↓
                   DATA/ANNONCES_CLEAN.csv

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


## 📁 Structure du projet
web-scraping/
│
├── scraper.py          # Collecte multi-pages + 1er niveau de nettoyage
├── clean_data.py       # Nettoyage avancé, normalisation, feature engineering
├── dashboard.py        # Application Streamlit interactive
│
├── DATA/
│   └── ANNONCES_CLEAN.csv   # Données nettoyées prêtes à l'analyse
│
├── requirements.txt    # Dépendances Python
└── README.md


## 🚀 Installation & Lancement
Prérequis

Python 3.10+
pip

Étapes

# 1. Cloner le dépôt
git clone https://github.com/fadimatou-dev/web-scraping.git
cd web-scraping

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer le scraper (génère DATA/ANNONCES_CLEAN.csv)
python scraper.py

# 4. (Optionnel) Relancer le nettoyage seul
python clean_data.py

# 5. Lancer le dashboard interactif
streamlit run dashboard.py

Le dashboard s'ouvre automatiquement sur http://localhost:8501.

## 📦 Dépendances
requests
beautifulsoup4
pandas
streamlit
matplotlib
seaborn

## 💡 Compétences Démontrées
Web scraping : navigation multi-pages, gestion des structures HTML dynamiques, extraction ciblée avec BeautifulSoup
Data wrangling : nettoyage de données textuelles brutes, extraction par regex, gestion des valeurs manquantes, normalisation
Analyse exploratoire (EDA) : statistiques descriptives, distributions, corrélations, comparaisons géographiques
Data viz : choix des représentations graphiques adaptées aux questions métier, dashboard sans infrastructure lourde

## 📌 Pistes d'Amélioration
 Ajouter une carte choroplèthe par département (Folium / Plotly)
 Automatiser le scraping via un scheduler (cron / Airflow)
 Stocker les données en base (SQLite ou PostgreSQL) pour historisation
 Ajouter un modèle de prédiction du prix au m² (régression, Scikit-Learn)
 Déployer le dashboard sur Streamlit Cloud


