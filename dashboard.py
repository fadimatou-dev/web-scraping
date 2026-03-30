import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Projet Immobilier 2025", layout="wide", page_icon="🏠")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("DATA/ANNONCES_CLEAN.csv", encoding="utf-8-sig")
        
        # Supprime toutes les colonnes qui commencent par "Unnamed"
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        if 'prix_m2' not in df.columns:
            df['prix_m2'] = df['prix'] / df['surface_m2']
        return df.dropna(subset=['prix', 'surface_m2', 'prix_m2'])
    except:
        return pd.DataFrame()

# --- 2. MENU LATÉRAL ---
with st.sidebar:
    st.title("📌 Menu de l'Application")
    selection = st.radio(
        "Navigation :",
        ["🔍 Étapes du Scraping", "📊 Analyse Graphique", "💾 Données Brutes"]
    )
    st.divider()
    st.info("Utilisez ce menu pour explorer le projet.")

df = load_data()

# --- 3. LOGIQUE D'AFFICHAGE ---

# --- PAGE 1 : LES ÉTAPES DU SCRAPING (Sert aussi de page d'accueil) ---
if selection == "🔍 Étapes du Scraping":
    
    st.title("Analyse du marché immobilier : Scraping Python")
    
    col_intro1, col_intro2 = st.columns([2, 1])
    with col_intro1:
        st.markdown("""
        **Objectifs du projet :** 
        * **Collecter automatiquement** des données immobilières sur plusieurs sites.
        * **Nettoyer et structurer** les données (prix, surface, ville, etc.).
        * **Analyser** les tendances (prix moyens, rapport prix/m²).
        * **Visualiser** les résultats via ce tableau de bord.
        """)
    
    st.divider()
    st.header("⚙️ Méthodologie : Extraction des données")

    

    # Etape 1 & 2
    col1, col2 = st.columns(2)
    with col1:
        st.success("### 1. Analyse du Site Web")
        st.write("""
        * **Inspection HTML :** Identification des balises (ex: `<p>` pour le prix).
        * **Analyse de l'URL :** Automatisation de la navigation via les filtres de recherche.
        """)
    with col2:
        st.info("### 2. Requête et Récupération")
        st.write("""
        * **Requests :** Récupération du code source HTML.
        * **Headers :** Simulation d'un navigateur pour contourner les protections.
        """)

    st.divider()

    # Etape 3 & 4
    col3, col4 = st.columns(2)
    with col3:
        st.warning("### 3. Extraction des données")
        st.write("""
        * **BeautifulSoup :** Transformation du HTML en objets Python.
        * **Parsing :** Boucle sur les annonces pour extraire les variables clés.
        """)
    with col4:
        st.error("### 4. Nettoyage, Structuration et Sauvegarde")
        st.write("""
        * **Formatage :** Conversion des textes en données numériques.
        * **Calcul :** Création de la colonne `prix_m2`.
        * **Sauvegarde :** On sauvegarde le fichier final en `csv`.
        """)

# --- PAGE 2 : ANALYSE GRAPHIQUE ---
elif selection == "📊 Analyse Graphique":
    if df.empty:
        st.error("⚠️ Fichier non trouvé. Veuillez vérifier le fichier.")
    else:
        st.title("📊 Visualisation Interactive du Marché")
        
        # Graphique 1 : Histogramme
        st.subheader("1. Distribution des Prix de Vente par annonce")
        # On place le filtre dans un menu dépliant pour cacher la liste longue   
        with st.expander("Modifier la sélection des villes"):
            v_h = st.multiselect(
                "Choisissez les villes à inclure :", 
                options=sorted(df['ville'].unique()), 
                default=sorted(df['ville'].unique()), 
                key="gh"
            )

        if v_h:
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            sns.histplot(df[df['ville'].isin(v_h)]['prix'], kde=True, color='blue', ax=ax1)
            
            
    
            formatter = ticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'.replace(',', ' '))
            ax1.xaxis.set_major_formatter(formatter)
            
            # Renommer les axes
            ax1.set_xlabel("Prix de vente (€)")
            ax1.set_ylabel("Nombre d'annonces")
            
            # Incliner les prix pour éviter les chevauchements
            plt.xticks(rotation=45)
            
            
            st.pyplot(fig1)
        
        # Graphique 2 : Boxplot
        st.divider()
        with st.expander("⚙️ Filtrer par type de bien"):
            t_o = st.multiselect(
                "Types de bien à inclure :", 
                options=df['type_bien'].unique(), 
                default=df['type_bien'].unique(), 
                key="go"
            )
        
        if t_o:
            # On augmente un peu la hauteur (figsize) pour laisser de la place aux étiquettes
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            
            # Utilisation de y='type_bien' pour afficher les noms à gauche
            sns.boxplot(
                data=df[df['type_bien'].isin(t_o)],
                x='prix', 
                y='type_bien', 
                palette="Set2", 
                ax=ax2
            )
            
            # FORMATAGE POUR ENLEVER .0 ET EXPOSANTS 
            import matplotlib.ticker as ticker
            
            # Formateur avec espace pour les milliers et sans décimales
            formatter = ticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'.replace(',', ' '))
            ax2.xaxis.set_major_formatter(formatter)
            
            # Nettoyage des noms d'axes
            ax2.set_xlabel("Prix de vente (€)")
            ax2.set_ylabel("") 
            
            st.pyplot(fig2)

        # Graphique 3 : Scatterplot
        st.divider()
        st.subheader("3. Prix au m² vs Surface")
        with st.expander("⚙️ Paramètres de comparaison des villes"):
            v_m = st.multiselect(
                "Villes à comparer :", 
                options=sorted(df['ville'].unique()), 
                default=df['ville'].unique(), 
                key="gm"
            )
        
        if v_m:
            fig3, ax3 = plt.subplots(figsize=(10, 5))
            sns.scatterplot(
                data=df[df['ville'].isin(v_m)], 
                x='surface_m2', 
                y='prix_m2', 
                hue='type_bien', 
                s=100, 
                ax=ax3
            )
            
            
            # Formateur pour l'axe Y (Prix au m²) 
            formatter = ticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'.replace(',', ' '))
            ax3.yaxis.set_major_formatter(formatter)
            
            # Nommer les axes plus clairement
            ax3.set_xlabel("Surface habitable (m²)")
            ax3.set_ylabel("Prix au m² (€/m²)")
            
            ax3.grid(True, linestyle='--', alpha=0.6)
            
            
            st.pyplot(fig3)
            
        st.subheader("📍 Analyse par Département")
        
        # 1. Extraction/Calcul des données par département
        if 'departements' in df.columns:
            
            with st.expander("⚙️ Options d'affichage par département"):
                # Permettre de filtrer certains départements si besoin
                depts_sel = st.multiselect(
                    "Choisir les départements :", 
                    options=sorted(df['departements'].unique()), 
                    default=sorted(df['departements'].unique()),
                    key="gd"
                )
            
            if depts_sel:
                # Calcul de la moyenne pour le graphique
                df_dept = df[df['departements'].isin(depts_sel)].groupby('departements')['prix'].mean().reset_index()
                df_dept = df_dept.sort_values('prix', ascending=False)

                fig4, ax4 = plt.subplots(figsize=(10, 5))
                sns.barplot(data=df_dept, x='departements', y='prix', palette="viridis", ax=ax4)

                # --- FORMATAGE PROFESSIONNEL ---
                import matplotlib.ticker as ticker
                
                # Formateur pour l'axe Y (Prix Moyen) 
                formatter = ticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'.replace(',', ' '))
                ax4.yaxis.set_major_formatter(formatter)
                
                # Ajouter les étiquettes de prix au-dessus de chaque barre
                for p in ax4.patches:
                    ax4.annotate(f'{p.get_height():,.0f} €'.replace(',', ' '), 
                                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                                 ha='center', va='center', 
                                 xytext=(0, 9), 
                                 textcoords='offset points',
                                 fontsize=9)

                ax4.set_xlabel("Départements")
                ax4.set_ylabel("Prix Moyen de vente (€)")
                
                
                st.pyplot(fig4)
        else:
            st.warning(f"⚠️ La colonne 'departements' est manquante. Colonnes dispos : {list(df.columns)}")


        st.subheader("🏙️ Prix au m² Moyen par Ville")
        
        # Expander pour la sélection
        with st.expander("⚙️ Choisir les villes à comparer"):
            v_m2 = st.multiselect(
                "Sélectionner les villes :", 
                options=sorted(df['ville'].unique()), 
                default=sorted(df['ville'].unique())[:10], # Top 10 par défaut pour la lisibilité
                key="gm2"
            )
        
        if v_m2:
            # Calcul de la moyenne du prix au m² par ville
            df_m2 = df[df['ville'].isin(v_m2)].groupby('ville')['prix_m2'].mean().reset_index()
            df_m2 = df_m2.sort_values('prix_m2', ascending=False)

            fig5, ax5 = plt.subplots(figsize=(10, 5))
            sns.barplot(data=df_m2, x='ville', y='prix_m2', palette="magma", ax=ax5)

            # --- FORMATAGE PROFESSIONNEL ---
            import matplotlib.ticker as ticker
            
            # Formateur : pas de .0, espace pour les milliers
            formatter = ticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'.replace(',', ' '))
            ax5.yaxis.set_major_formatter(formatter)
            
            # Ajout des valeurs au-dessus des barres
            for p in ax5.patches:
                ax5.annotate(f'{p.get_height():,.0f} €'.replace(',', ' '), 
                             (p.get_x() + p.get_width() / 2., p.get_height()), 
                             ha='center', va='center', 
                             xytext=(0, 9), 
                             textcoords='offset points',
                             fontsize=9)

            ax5.set_xlabel("Ville")
            ax5.set_ylabel("Prix moyen au m² (€/m²)")
            plt.xticks(rotation=45)
            
            st.pyplot(fig5)
            
# --- PAGE 3 : DONNÉES BRUTES ---
elif selection == "💾 Données Brutes":
    st.title("📂 Aperçu de la base de données")
    st.write(f"Le fichier contient actuellement **{len(df)}** annonces.")
    st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Télécharger le CSV final", csv, "immobilier_final.csv", "text/csv")