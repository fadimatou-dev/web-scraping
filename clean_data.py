# Import des librairies nécessaires
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import geopandas as gpd 

# chargement du fichier
df = pd.read_csv("../DATA/ANNONCES_CLEAN.csv", encoding="utf-8-sig")


# afficher les 5 premières lignes 
print(df.head())
print(df.shape)

#int Les info sur df
print(df.info())

# Création d’un dictionnaire de correspondance afin d’extraire correctement les départements, ceux-ci étant
# imparfaitement identifiés lors du processus de web scraping.

departements_dict =  {"01": "Ain", "02": "Aisne", "03": "Allier", "04": "Alpes-de-Haute-Provence", "05": "Hautes-Alpes", 
                "06": "Alpes-Maritimes", "07": "Ardèche", "08": "Ardennes", "09": "Ariège", "10": "Aube", "11": "Aude", 
                "12": "Aveyron", "13": "Bouches-du-Rhône", "14": "Calvados", "15": "Cantal", "16": "Charente", 
                "17": "Charente-Maritime", "18": "Cher", "19": "Corrèze", "2A": "Corse-du-Sud", "2B": "Haute-Corse", 
                "21": "Côte-d'Or", "22": "Côtes-d'Armor", "23": "Creuse", "24": "Dordogne", "25": "Doubs", "26": "Drôme", 
                "27": "Eure", "28": "Eure-et-Loir", "29": "Finistère", "30": "Gard", "31": "Haute-Garonne", "32": "Gers", 
                "33": "Gironde", "34": "Hérault", "35": "Ille-et-Vilaine", "36": "Indre", "37": "Indre-et-Loire", 
                "38": "Isère", "39": "Jura", "40": "Landes", "41": "Loir-et-Cher", "42": "Loire", "43": "Haute-Loire", 
                "44": "Loire-Atlantique", "45": "Loiret", "46": "Lot", "47": "Lot-et-Garonne", "48": "Lozère", 
                "49": "Maine-et-Loire", "50": "Manche", "51": "Marne", "52": "Haute-Marne", "53": "Mayenne", 
                "54": "Meurthe-et-Moselle", "55": "Meuse", "56": "Morbihan", "57": "Moselle", "58": "Nièvre", "59": "Nord", 
                "60": "Oise", "61": "Orne", "62": "Pas-de-Calais", "63": "Puy-de-Dôme", "64": "Pyrénées-Atlantiques", 
                "65": "Hautes-Pyrénées", "66": "Pyrénées-Orientales", "67": "Bas-Rhin", "68": "Haut-Rhin", "69": "Rhône", 
                "70": "Haute-Saône", "71": "Saône-et-Loire", "72": "Sarthe", "73": "Savoie", "74": "Haute-Savoie", "75": "Paris", 
                "76": "Seine-Maritime", "77": "Seine-et-Marne", "78": "Yvelines", "79": "Deux-Sèvres", "80": "Somme", "81": "Tarn", 
                "82": "Tarn-et-Garonne", "83": "Var", "84": "Vaucluse", "85": "Vendée", "86": "Vienne", "87": "Haute-Vienne", 
                "88": "Vosges", "89": "Yonne", "90": "Territoire de Belfort", "91": "Essonne", "92": "Hauts-de-Seine", 
                "93": "Seine-Saint-Denis", "94": "Val-de-Marne", "95": "Val-d'Oise", "971": "Guadeloupe", "972": "Martinique", 
                "973": "Guyane", "974": "La Réunion", "976": "Mayotte"}

# Creation d'une nouvelle colonne departement
# Normalisation du code département
df = df.copy(deep=True)
df["code_dep"] = (df["code_dep"].astype(str).str.replace(".0", "", regex=False).str.strip().str.zfill(2))                        
# Création de la colonne département à partir du dictionnaire
df.loc[:, "departements"] = df["code_dep"].map(departements_dict)
# Suppression des colonnes département et url
df.drop(columns=["url", "departement"], inplace=True)

# Transformer la colonne type de bien
df["type_bien"] = (df["type_bien"].astype(str).str.split("/", n=1).str[0].str.strip())

#On observe la présence de valeurs nulles pour le nombre de pièces, probablement liées à des erreurs de saisie.
# On va les remplacer par de NaN.
df = df.replace(0, np.nan)

# Les valeurs uniques dans type_bien
df.type_bien.unique()

# gardons que les ligne qui contiennent "maison", "appartement" les immeuble n'ont pas de nombre de 
df = df[df["type_bien"].isin(["Maison", "Appartement", "Immeuble"])]

df.isna().sum()

#visualisation des valeurs manquantes
plt.figure(figsize=(15, 8))
msno.matrix(df, sparkline=False)
plt.show()

# calculer la surface moyenne, le nombre de pièce moyenne et le prix moyen par département
# et on va remplacer les valeur manquantes de surface et nb_pièces par leur moyenne par departement
df_grouped= (df.groupby("code_dep").agg(
        surface_moyenne=("surface_m2", "mean"),
        nb_pieces_moyen=("nb_pieces", "mean"),
        prix_moyen=("prix", "mean")
    ).round(2)
    .reset_index()
)
df_grouped

# nombre d'annonces 'lignes' pour les départment 24, 60, 971.
df.loc[df["code_dep"].isin(["24","30","60", "92", "971"])]

# Étant donné qu’il n’existe qu’une seule annonce pour les départements 24, 60, 92 et 971, le prix moyen sera fussé pour ces départements.
# ces lignes ont été supprimées.
df = df.copy(deep=True)
df = df.drop(index=[3680,3772,3884,4239,4318])

print(df.shape)

# Remplacement des valeurs manquantes par la moyenne observée au niveau du département
# Création d'une copie de df
df = df.copy(deep=True)

# Remplacer les NaN de la colonne surface_m2
df["surface_m2"] = df["surface_m2"].fillna(
    df.groupby("code_dep")["surface_m2"].transform("mean"))

# Remplacer les NaN de la colonne nb_pieces
df["nb_pieces"] = df["nb_pieces"].fillna(
    df.groupby("code_dep")["nb_pieces"].transform("mean"))

# Remplacer les NaN de la colonne prix
df["prix"] = df["prix"].fillna(
    df.groupby("code_dep")["prix"].transform("mean"))

# Verifons les na.
df.isna().sum()

# Il y a une valeur manquantes pour surface, nb_pieces et departemets.
# Affichons les lignes avec les valeurs manquantes.
# Affichons les  lignes contenant des valeur manquantes.
df[df.isna().any(axis=1)]

# Suprimmons cette dernière ligne avec 3 valeur manquantes.
df = df.copy()
df = df.dropna(ignore_index=True)

df.describe().round(2)

# Valeurs aberrantes
df_aberrant = df[(df["nb_pieces"] > 500) | (df["surface_m2"] <=7 )]
df_aberrant.shape

# suppression df_aberrant.
df = df.drop(df_aberrant.index).reset_index(drop=True)

df_clean = df.copy()
df_clean.shape

df_clean.to_csv("df_clean.csv")

# statistiques descriptives
df_clean.describe().round(2)

# création d'une colonne année.
df_clean["date"] = pd.to_datetime(
    df_clean["date"], 
    format="%d/%m/%Y", 
    errors="coerce"
)
df_clean["annee"] = df_clean["date"].dt.year


# arrondir surface et nb_pièces
df_clean[["surface_m2", "nb_pieces"]] = df_clean[
    ["surface_m2", "nb_pieces"]].round(2)

# création d'une nouvelle colonne prix au metre carre.
df_clean["prix_m2"] = round(df_clean["prix"] / df_clean["surface_m2"],2)
# Galculons prix au metre carré par departement.
prix_m2_dep = (
    df_clean
    .groupby("departements")["prix_m2"]
    .mean()
    .reset_index(name="prix_m2")
    .round(2))
print(prix_m2_dep)


prix_m2_dep_sorted = prix_m2_dep.sort_values("prix_m2", ascending=False)

plt.figure(figsize=(10, 6))
ax = sns.barplot(
    data=prix_m2_dep_sorted,
    x="departements",
    y="prix_m2"
)

# Ajout des valeurs au-dessus des barres
for container in ax.containers:
    ax.bar_label(container, fmt="%.2f", padding=3)

plt.xlabel("Département")
plt.ylabel("Prix moyen au m² (€)")
plt.title("Prix moyen au mètre carré par département (trié)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# prix au metre carre par année et par département
prix_m2_dep_annee = (
    df_clean
    .groupby(["departements", "annee"])
    .agg(
        prix_total=("prix", "sum"),
        surface_totale=("surface_m2", "sum")
    )
    .reset_index()
)

prix_m2_dep_annee["prix_m2"] = (
    prix_m2_dep_annee["prix_total"] /
    prix_m2_dep_annee["surface_totale"]
).round(2)


print(prix_m2_dep_annee)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=prix_m2_dep_annee,
    x="annee",
    y="prix_m2",
    hue="departements"
)

plt.xlabel("Année")
plt.ylabel("Prix moyen au m² (€)")
plt.title("Prix moyen au mètre carré par département et par année")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# courbe
plt.figure(figsize=(12, 7))

sns.lineplot(
    data=prix_m2_dep_annee,
    x="annee",
    y="prix_m2",
    hue="departements",
    marker="o"
)

plt.xlabel("Année")
plt.ylabel("Prix moyen au m² (€)")
plt.title("Évolution du prix moyen au mètre carré par département")
plt.legend(title="Département")
plt.grid(True)
plt.tight_layout()
plt.show()

# tendance globale par année
prix_m2_global_annee = (
    df_clean
    .groupby("annee")
    .agg(
        prix_total=("prix", "sum"),
        surface_totale=("surface_m2", "sum")
    )
    .reset_index()
)

prix_m2_global_annee["prix_m2"] = (
    prix_m2_global_annee["prix_total"] /
    prix_m2_global_annee["surface_totale"]
).round(2)

# Courbe de tendance
plt.figure(figsize=(10, 6))

sns.lineplot(
    data=prix_m2_global_annee,
    x="annee",
    y="prix_m2",
    marker="o"
)

plt.xlabel("Année")
plt.ylabel("Prix moyen au m² (€)")
plt.title("Tendance globale du prix moyen au mètre carré par année")
plt.grid(True)
plt.tight_layout()
plt.show()

# Définition de l’URL du fichier GeoJSON. Cette URL pointe vers un fichier officiel au format GeoJSON
# qui contient tous les départements français,
url_geojson = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"

# Chargement du fichier
departements_map = gpd.read_file(url_geojson)

departements_map.head()

# Convertion du dataframe scraper en DataFrame unique de départements
deps = df["code_dep"].unique()
df_deps = pd.DataFrame({"code": deps})

# Préparer la colonne pour merge
departements_map["departements"] = departements_map["code"]
gdf = departements_map.merge(df_deps, on="code", how="inner")


# Création d'un dictionnaire avec les departements scrapées
fig, ax = plt.subplots(figsize=(8, 10))

# Afficher la carte de France métropolitaine 
departements_map.plot(ax=ax, color="#dddddd", edgecolor="black", linewidth=0.5)

# Coloration des départements scrappés (en rouge)
gdf.plot(ax=ax, color="red", edgecolor="black", linewidth=1.2)

# Gestion des bornes de la carte pour positionner les labels à gauche
minx, miny, maxx, maxy = departements_map.total_bounds
label_x = minx - 0.3 * (maxx - minx)   # plus ou moins loin à gauche

for idx, row in gdf.iterrows():
    centroid = row.geometry.centroid
    
    code_dep = str(row["departements"])
    nom_dep = departements_dict.get(code_dep, "")

    # Afficher les textes (numero département et non du departement) à gauche de la carte
    label_text = f"{code_dep} - {nom_dep}"

    # Positionner les textes : à gauche, aligné sur la hauteur du centroïde
    ax.annotate(
        label_text,
        xy=(centroid.x, centroid.y),      # point cible (sur la carte)
        xytext=(label_x, centroid.y),     # position du texte (à gauche)
        arrowprops=dict(
            arrowstyle="->",
            color="black",
            lw=0.8
        ),
        ha="right",   # texte aligné à droite (vers la carte)
        va="center",
        fontsize=7,
        color="black",
    )

ax.set_title("Départements scrappés", fontsize=16)
plt.axis("off")
plt.show()


# Création d'une nouvelle colonne calculée
df["prix_m2"] = df["prix"] / df["surface_m2"]

# On enlève les valeurs manquantes pour le prix au m²
df_graph = df.dropna(subset=["prix_m2"])

top_10_villes = (
    df_graph.groupby("ville")["prix_m2"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

# Figure
plt.figure(figsize=(12, 7))
sns.set_theme(style="whitegrid")

# Palette
colors = sns.color_palette("Reds_r", n_colors=len(top_10_villes))

# Graphique à barres horizontales (palette + hue pour éviter le warning)
barplot = sns.barplot(
    x=top_10_villes.values,
    y=top_10_villes.index,
    hue=top_10_villes.index,   # nécessaire pour utiliser palette sans warning
    palette=colors,
    legend=False               # pas de légende (inutile ici)
)

# Personnalisation
plt.title("Top 10 des villes les plus chères au m²", fontsize=18, fontweight="bold", pad=20)
plt.xlabel("Prix moyen au m² (€/m²)", fontsize=13)
plt.ylabel("Ville", fontsize=13)

# Ajout des étiquettes de données
max_v = top_10_villes.values.max()
offset = 0.02 * max_v  # décalage relatif (plus robuste que +50)

for i, v in enumerate(top_10_villes.values):
    barplot.text(v + offset, i, f"{int(v)} €/m²", color="black", va="center", fontweight="bold")

plt.tight_layout()
plt.show()

df['prix_m2'] = df['prix'] / df['surface_m2']
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='surface_m2', y='prix', hue='type_bien', s=100)

plt.title('Analyse du Prix au m² par rapport à la Surface')
plt.xlabel('Surface (m²)')
plt.ylabel('Prix')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
