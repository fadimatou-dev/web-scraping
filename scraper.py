# Import des libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import hashlib
from urllib.parse import urljoin
import matplotlib.pyplot as plt
import seaborn as sns

# Url de base
url = 'https://www.lereflexenotaire.fr/petites-annonces'
# Envoi d’une requête HTTP pour récupérer le contenu de la page web
page = requests.get(url, timeout=30)
# Vérification du code de réponse du serveur
print("HTTP status:", page.status_code)
# Analyse du code HTML de la page pour permettre l’extraction des données
soup = BeautifulSoup(page.text, "html.parser")

# Recherche du conteneur principal regroupant les annonces immobilières
html_page = soup.find("div", class_="offers flex flex-col md:flex-row flex-wrap")
# Extraction de toutes les annonces contenues dans le conteneur
conteneur_annonces = html_page.find_all(class_="w-full md:w-1/2 lg:w-1/3 p-2 mb-4") 

# Affichage du nombre d'annonces extraites
print("Nombre d'annonces trouvées sur la page d'accueil:", len(conteneur_annonces))


# Vérification du contenu du conteneur principal
len(html_page)
# Sélection de la première annonce extraite pour analyser sa structure
first_annonce = conteneur_annonces[0]
# Affichage de la première annonce afin d’identifier les éléments à extraire
print(first_annonce)

# Extraction de la date de la première annonce
first_date = first_annonce.find('p', class_='pb-2').text
# Affichage de la date extraite
print(first_date)

# Extraction du prix de la première annonce sous forme de texte
#on affiche le prix TTC
first_price_text = first_annonce.find('p', class_='notaires-color2-color').text

# Nettoyage du prix en supprimant les caractères non numériques
# puis conversion en valeur entière
if first_price_text:
    first_price = int(re.sub(r"\D", "", first_price_text))
else:
    first_price = None
# Affichage du prix extrait
print(f"💰 Le prix TTC est : {first_price} €")

# Recherche du bloc contenant le type de transaction et le type de bien
tag = first_annonce.find("p", class_="mt-3")
# Extraction du texte correspondant, si le bloc est présent
first_carac_type = tag.get_text(strip=True) if tag else None
# Découpage du texte en éléments distincts
first_carac_type= first_carac_type.split()
# Affichage du résultat obtenu
print(first_carac_type)

# Recherche des blocs contenant les informations de localisation et de caractéristiques
block_loc = first_annonce.find_all("p", class_="py-1")

# Extraction du texte correspondant à la localisation (ville et département)
first_loc = block_loc[0].get_text(strip=True) if len(block_loc) > 0 else None

# Extraction dep, ville et code du departement
ville = first_loc.split("-")[0].strip()  # Extraction du nom de la ville
departement = re.search(r"-\s*(.+)\s*\(", first_loc).group(1) # Extraction du nom du département à partir du texte
code_dep = re.search(r"\((\d+)\)", first_loc).group(1)   # Extraction du code du département

# Affichage ville, département et code du département
print("Localisation:", first_loc)

# Extraction du texte correspondant aux caractéristiques du bien
first_carac = block_loc[1].get_text(strip=True) if len(block_loc) > 1 else None

# Extraction surface_m2, nb_pieces
if first_carac:
    surface_match = re.search(r"(\d+)\s*m2", first_carac)
    pieces_match = re.search(r"(\d+)\s*pi[eè]ces", first_carac)

    surface_m2 = int(surface_match.group(1)) if surface_match else None
    nb_pieces = int(pieces_match.group(1)) if pieces_match else None
else:
    surface_m2 = None
    nb_pieces = None
surface_m2, nb_pieces

# Affichage de la surface et nombre de pièces
print(f"Caractéristiques : {surface_m2} m2, {nb_pieces} pièces")

# Recherche du bloc contenant la description du bien
block_description = first_annonce.select_one('p.mt-3.text-2xs.text-gray-600')

# Extraction du texte correspondant à la localisation (ville et département)
description = block_description.get_text(strip=True) if len(block_description) > 0 else None

# Affichage de la description
print("Description:", description)

# Recupérer les informations de toute la page.
# Creation des listes pour recupérer les annonces de toute la page
dates = []
prix = []
type_transactions = []
type_biens = []
villes = []
departements = []
codes_dep = []
surfaces_m2 = []
nb_pieces_list = []
descriptions = []

# Création d'une boucle pour boucler sur les annonces d'une page
for conteneur in conteneur_annonces:
    # Extraction des dates
    date_tag = conteneur.find('p', class_='pb-2')
    date = date_tag.get_text(strip=True) if date_tag else None
    dates.append(date)
    
    print(f"📅 Date : {date}")
    
    # Extraction des prix
    price_tag = conteneur.select_one('span.block.py-1')  # plus fiable que class_="block py-1"
    price_text = price_tag.get_text(strip=True) if price_tag else ""
    price_digits = re.sub(r"\D", "", price_text)
    price = int(price_digits) if price_digits else None
    prix.append(price)

    print(f"💰 Prix : {price} €")


    #Les caractéristiques en bloc
    tag = conteneur.find("p", class_="mt-3")
    txt = tag.get_text(strip=True) if tag else ""
    
    # Le split pour extraire les données séparement.
    if "-" in txt:
        type_transaction, type_bien = [x.strip() for x in txt.split("-", 1)]
    else:
        type_transaction, type_bien = (None, txt.strip() or None)
    
    type_transactions.append(type_transaction)
    type_biens.append(type_bien)


    # Extraction de la ville, le departement et le code du departement.
    if first_loc:
        ville = first_loc.split("-", 1)[0].strip()

        dep_match = re.search(r"-\s*(.+?)\s*\((\d+)\)", first_loc)
        if dep_match:
            departement = dep_match.group(1).strip()
            code_dep = dep_match.group(2).strip()
        else:
            departement = None
            code_dep = None
    else:
        ville = None
        departement = None
        code_dep = None

    villes.append(ville)
    departements.append(departement)
    codes_dep.append(code_dep)

    # Recupérer la localisation du bien
    
    block_loc = conteneur.find_all("p", class_="py-1")
    first_loc = block_loc[0].get_text(strip=True) if len(block_loc) > 0 else None
    

    # Extraction des caractéristiques (surface et le nombre de pièces)
    first_carac = block_loc[1].get_text(strip=True) if len(block_loc) > 1 else None
    if first_carac:
        surface_match = re.search(r"(\d+)\s*m[²2]", first_carac)
        pieces_match = re.search(r"(\d+)\s*pi[eè]ces?", first_carac)

        surface_m2 = int(surface_match.group(1)) if surface_match else None
        nb_pieces = int(pieces_match.group(1)) if pieces_match else None
    else:
        surface_m2 = None
        nb_pieces = None

    surfaces_m2.append(surface_m2)
    nb_pieces_list.append(nb_pieces)
    
    # Extraction des descriptions
    desc = conteneur.select_one('p.mt-3.text-2xs.text-gray-600')
    descr = desc.get_text(strip=True) if desc else None
    descriptions.append(descr)
    
    # Affichage de la description
    print("Description:", descr)

  # creation du dataframe
df = pd.DataFrame({
    "date": dates,
    "prix": prix,
    "type_transaction": type_transactions,
    "type_bien": type_biens,
    "ville": villes,
    "departement": departements,
    "code_dep": codes_dep,
    "surface_m2": surfaces_m2,
    "nb_pieces": nb_pieces_list,
    "description": descriptions
})
# Affiche le dataframe
print(df)

# 4- Identifier et Compter les doublons 
nb_doublons = df.duplicated().sum()

# 3. Action conditionnelle
if nb_doublons > 0:
    print(f"✅ {nb_doublons} doublons trouvés. Suppression en cours...")
    df = df.drop_duplicates(subset=df, keep='first').reset_index(drop=True)
    print("✨ Doublons supprimés avec succès.")
else:
    print("🔍 Aucun doublon détecté.")


# Craping de plusieurs pages.
# Création d’une session HTTP pour réutiliser la connexion et définir un User-Agent
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

# URL de base du site à scarper.
BASE_URL = "https://www.lereflexenotaire.fr/petites-annonces"

# Paramètres de pagination et de temporisation
MAX_PAGES = 410 # nombre de pages maximales à scraper
SLEEP_SEC = 0.3   # temps d'attente

# Initialisation des structures de stockage des données
all_rows = []
seen_urls = set()

# Boucle de parcours des pages d’annonces
for page in range(1, MAX_PAGES + 1):
    url_page = f"{BASE_URL}?page={page}"
    
    # Envoi de la requête HTTP pour chaque page
    r = session.get(url_page, timeout=20)
    r.raise_for_status()

    # Analyse du contenu HTML de la page
    soup = BeautifulSoup(r.text, "html.parser")

    # Filtrage des liens afin de ne conserver que ceux correspondant à des annonces valides
    candidates = soup.select('a[href*="immobilier.notaires.fr"]')
    conteneur_annonces = [
        a for a in candidates
        if a.find("p", class_="pb-2") and a.find("p", class_="mt-3")
    ]

    # Arrêt du scraping si aucune annonce n’est détectée sur la page
    if not conteneur_annonces:
        print(f"Arrêt: 0 annonce détectée en page {page}")
        break
    
    # Initialisation du compteur de nouvelles annonces
    new_count = 0

    # Boiucle sur les annonces filtrées
    for conteneur in conteneur_annonces:
        # Extraction de l’URL de l’annonce
        href = conteneur.get("href")
        url_annonce = urljoin(url_page, href) if href else None
        if not url_annonce:
            continue
            
        # Vérification de l’unicité de l’annonce afin d’éviter les doublons
        if url_annonce in seen_urls:
            continue
        # Enregistrement de l’URL et incrémentation du compteur
        seen_urls.add(url_annonce)
        new_count += 1

        # Extraction champs
        date_tag = conteneur.find("p", class_="pb-2")
        date = date_tag.get_text(strip=True) if date_tag else None

        # prix: chercher un span "block" (évite la dépendance stricte à py-1)
        price_tag = conteneur.select_one("span.block")
        price_text = price_tag.get_text(" ", strip=True) if price_tag else ""
        price_digits = re.sub(r"\D", "", price_text)
        prix = int(price_digits) if price_digits else None

        tag = conteneur.find("p", class_="mt-3")
        txt = tag.get_text(strip=True) if tag else ""
        if "-" in txt:
            type_transaction, type_bien = [x.strip() for x in txt.split("-", 1)]
        else:
            type_transaction, type_bien = (None, txt.strip() or None)

        block_loc = conteneur.find_all("p", class_="py-1")
        first_loc = block_loc[0].get_text(strip=True) if len(block_loc) > 0 else None
        first_carac = block_loc[1].get_text(strip=True) if len(block_loc) > 1 else None

        if first_loc:
            ville = first_loc.split("-", 1)[0].strip()
            dep_match = re.search(r"-\s*(.+?)\s*\((\d+)\)", first_loc)
            departement = dep_match.group(1).strip() if dep_match else None
            code_dep = dep_match.group(2).strip() if dep_match else None
        else:
            ville = departement = code_dep = None

        if first_carac:
            surface_match = re.search(r"(\d+)\s*m[²2]", first_carac)
            pieces_match = re.search(r"(\d+)\s*pi[eè]ces?", first_carac)
            surface_m2 = int(surface_match.group(1)) if surface_match else None
            nb_pieces = int(pieces_match.group(1)) if pieces_match else None
        else:
            surface_m2 = nb_pieces = None
            
          # Extraction des descriptions
        desc = conteneur.select_one('p.mt-3.text-2xs.text-gray-600')
        descr = desc.get_text(strip=True) if desc else None
        descriptions.append(descr)


        all_rows.append({
            "url": url_annonce,
            "date": date,
            "prix": prix,
            "type_transaction": type_transaction,
            "type_bien": type_bien,
            "ville": ville,
            "departement": departement,
            "code_dep": code_dep,
            "surface_m2": surface_m2,
            "nb_pieces": nb_pieces,
            "description": descr
        })

    print(f"Page {page}", end="\r", flush=True)

    # arrêt si la pagination n’apporte plus rien
    if new_count == 0:
        print(f"Arrêt: aucune nouvelle annonce en page {page} (fin ou boucle).")
        break

    time.sleep(SLEEP_SEC)

df_raw = pd.DataFrame(all_rows)
df = df_raw.drop_duplicates(subset=["url"]).reset_index(drop=True)

print("TOTAL ANNONCES", len(df))
df.head(10)



