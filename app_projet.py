__author__ = "Marion Nguyen"
__copyright__= "Copyright 2023, Les festivals en France projet"
__version__= "0.0.1"
__maintener__= "Marion Nguyen"
__email__="marion.nguyen@efrei.net"



import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import re
import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.models import RadioGroup, CustomJS
from bokeh.layouts import column
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import HoverTool, ColorBar
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256





st.title('Les festivals en France')

with st.sidebar :
    st.write("Prénom : Marion")
    st.write("Nom : Nguyen") 
    st.write("Linkedin : https://www.linkedin.com/in/marion-nguyen/ ") 
    st.write("Mail : marion.nguyen@efrei.net")
    st.write("#datavz2023efrei ")
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("Lien du dataset : https://www.data.gouv.fr/fr/datasets/liste-des-festivals-en-france/ ")


st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### Contexte", unsafe_allow_html=True)
st.write("L'évolution des festivals en France est le reflet des mutations socioculturelles et des préférences du public. À travers une diversité de disciplines artistiques, de périodes de déroulement et de localisations géographiques, les festivals sont devenus un indicateur riche de l'identité culturelle de la nation. Cette évolution soulève des questions importantes quant à l'adaptation des organisateurs de festivals à ces changements, mais offre également des opportunités pour repenser et dynamiser l'offre culturelle. Dans cette étude, nous explorerons comment ces tendances influencent le paysage festivalier en France et les implications qu'elles ont pour les professionnels du secteur et les pouvoirs publics.")
st.markdown("<br>", unsafe_allow_html=True)
st.write("Comment l'évolution des festivals en France, en termes de disciplines, de périodes et de localisation, reflète-t-elle les changements socioculturels et les préférences du public, et quelles opportunités cela crée-t-il pour les organisateurs de festivals ?")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


# URL du lien de téléchargement
url = "https://www.data.gouv.fr/fr/datasets/r/47ac11c2-8a00-46a7-9fa8-9b802643f975"
df = pd.read_csv(url, delimiter=";")


# RECUPERATION DES COORDONNEES : LATITUDE ET LONGITUDE
df["geocodage_xy"] = df["geocodage_xy"].astype(str) #la colonne "geocodage_xy" est traitée comme une chaîne de caractères pour faciliter l'extraction de la latitude et de la longitude
# Fonction pour extraire les coordonnées en latitude et longitude
def extract_coords(x):
    try:
        if ',' in x: #les coordonnées sont séparées par une virgule, par exemple : 50.4286822706,2.87559653416
            lat, lon = map(float, x.split(','))
            return lat, lon
        else: #gérer les cas où les coordonnées ne sont pas renseignées
            return None, None
    except (ValueError, AttributeError):
        return None, None

df[["Latitude", "Longitude"]] = df["geocodage_xy"].apply(lambda x: pd.Series(extract_coords(x)))





# CARTE DE CHALEUR DE LA DENSITE DES FESTIVALS EN FRANCE
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### Répartition des festivals en France", unsafe_allow_html=True)
st.write("Densité des festivals en France ")
fig = px.density_mapbox(
    df.dropna(subset=["Latitude", "Longitude"]), lat="Latitude", lon="Longitude", radius=10,
    center=dict(lat=46.603354, lon=1.888334), zoom=5,
    mapbox_style="carto-positron", title="Carte de chaleur des festivals en France",
    color_continuous_scale="Inferno",
    width=1000,  #largeur de la carte
    height=800   #hauteur de la carte
)
st.plotly_chart(fig)




# RECUPERATION DE L'ANNEE SOUS LE BON FORMAT
df["annee_de_creation_du_festival"] = df["annee_de_creation_du_festival"].astype(str) #la colonne "annee_de_creation_du_festival" est traitée comme une chaîne de caractères pour faciliter l'extraction de l'année sous le bon format
# Fonction pour extraire les années sous le bon format
def extract_year(year_str):
    try:
        year_match = re.search(r'\b\d{4}\b', year_str) #si l'année est noté sous le format "YYYY"
        if year_match:
            return int(year_match.group())
        year_match = re.search(r'\b\d{4}\-\d{2}\-\d{2}', year_str) #si l'année est noté sous le format "YYYY-MM-DD"
        if year_match:
            return int(year_match.group()[:4]) #on ne récupère que l'année
        return None #si aucune correspondance trouvée
    except (ValueError, AttributeError):
        return None





# COURBE DES ANNEES DE CREATION DES FESTIVALS EN FRANCE
# Extraction de l'année de création des festivals
df["Annee de Creation"] = df["annee_de_creation_du_festival"].apply(extract_year)
# On ne garde que les années sous le bon format
valid_years = df["Annee de Creation"].dropna()
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
# Créez une sous-section Streamlit pour le graphique
st.subheader("Évolution du nombre de créations de festivals en France au fil des années")
# Créer un DataFrame pour compter le nombre de festivals par année
festivals_by_year = valid_years.value_counts().sort_index().reset_index()
festivals_by_year.columns = ["Année de création", "Nombre de festivals"]
# Créer un graphique de ligne avec Streamlit
st.line_chart(festivals_by_year.set_index("Année de création"))





# DIAGRAMME EN BOITE DE LA DISTRIBUTION DES FESTIVALS SELON LES DIFFERENTES DISCIPLINES
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### Répartition des festivals en France selon la discipline", unsafe_allow_html=True)
st.write("Distribution des festivals par discipline ")
discipline_counts = df["discipline_dominante"].value_counts() #comptage du nombre d'occurrence de chaque discipline
# Création du diagramme en boite
plt.figure(figsize=(10, 6))
plt.title("Diagramme en boîte du nombre de festivals par discipline")
discipline_counts.sort_values(ascending=False).plot(kind='barh')
plt.ylabel("Discipline")
plt.xlabel("Nombre de festivals")
st.pyplot(plt)





#CARTE DE CHALEUR DE LA DENSITE DES FESTIVALS SELON LES DISCIPLINES
st.markdown("<br>", unsafe_allow_html=True)
st.write("Répartition géographique des festivals par discipline")
# Menu déroulant pour sélectionner la discipline
selected_discipline = st.selectbox("Veuillez sélectionner une discipline", df["discipline_dominante"].unique())
# Filtrer les données en fonction de la discipline sélectionnée
filtered_df = df[df["discipline_dominante"] == selected_discipline]
filtered_df["Latitude"] = filtered_df["Latitude"]
filtered_df["Longitude"] = filtered_df["Longitude"]
# Création de la carte de chaleur
fig = px.density_mapbox(filtered_df, lat="Latitude", lon="Longitude", z=filtered_df.index, radius=10, zoom=3, mapbox_style="stamen-terrain", title="Carte thermique de la répartition géographique des festivals par discipline ")
st.plotly_chart(fig, use_container_width=True)






# CAMEMBERT DE LA DISTRIBUTION DES FESTIVALS SELON LES PERIODES
# Regroupage des valeurs similaires dans la colonne "periode_principale_de_deroulement_du_festival" :
df["periode_principale_de_deroulement_du_festival"] = df["periode_principale_de_deroulement_du_festival"].replace(
    {"après-saison (6 septembre - 31 décembre)": "Après-saison (6 septembre - 31 décembre)"}
)
df["periode_principale_de_deroulement_du_festival"] = df["periode_principale_de_deroulement_du_festival"].replace(
    {"avant-saison (1er janvier - 20 juin)": "Avant-saison (1er janvier - 20 juin)"}
)
# Exclusion des lignes où la colonne "periode_principale_de_deroulement_du_festival" contient des mois de l'année
excluded_months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre","Ocotbre"]
data = df[~df["periode_principale_de_deroulement_du_festival"].isin(excluded_months)]
# Comptage du nombre d'occurrences de chaque période
periode_counts = data["periode_principale_de_deroulement_du_festival"].value_counts()
# Création du diagramme camembert
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### Répartition des festivals en France selon la période de déroulement", unsafe_allow_html=True)
st.write("Répartition des festivals selon leur période de déroulement ")
plt.figure(figsize=(8, 8)) 
colors = plt.cm.Paired(range(len(periode_counts)))
wedges, texts, autotexts = plt.pie(periode_counts, autopct='%1.1f%%', colors=colors)
plt.axis('equal')
# Légende à côté du camembert pour plus de lisibilité
plt.legend(periode_counts.index, title="Périodes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
plt.title("Camembert de répartition des festivals selon leur période de déroulement ")
st.pyplot(plt)




# DIAGRAMME EN BARRE DE LA DISTRIBUTION DES FESTIVALS EN FRANCE SELON LA PERIODE ET LA DISCIPLINE
st.markdown("<br>", unsafe_allow_html=True)
st.write("Répartition des festivals selon leur période de déroulement et leur discipline")
# Menu déroulant pour sélectionner la période
selected_period = st.selectbox("Sélectionnez une période", df['periode_principale_de_deroulement_du_festival'].unique())
# Filtrer les données en fonction de la période sélectionnée
filtered_data = df[df['periode_principale_de_deroulement_du_festival'] == selected_period]
# Regrouper les données par discipline et compter le nombre de festivals
data_grouped = filtered_data.groupby('discipline_dominante').size().reset_index(name='nombre_de_festivals')
# Création du diagramme
chart = alt.Chart(data_grouped).mark_bar().encode(
    x=alt.X('discipline_dominante:N', title='Discipline'),
    y=alt.Y('nombre_de_festivals:Q', title='Nombre de festivals')
).properties(
    width=400,
    height=400
)
st.altair_chart(chart, use_container_width=True)
