import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

# Show the page title and description.
st.set_page_config(page_title="Explo JB", page_icon="")
st.title("Explo JB")
st.write(
    """
    Un petit aperçu de l'explo à venir ? C'est ici ! \n
    Pour ceux qui ne connaissent pas le réseau par coeur : \n
    La coupe du JB : https://groupe-speleo-vulcain.com/wp-content/uploads/2025/07/jb-2025-coupe.pdf \n
    Le plan du JB : https://groupe-speleo-vulcain.com/wp-content/uploads/2025/05/jb-2025-plan1000.pdf \n
    (Merci Xa !)
    """
)


#Importation des données d'appartenances
df_appartenances = pd.read_csv("data/equipes.csv")
# Nettoyer les espaces supplémentaires
df_appartenances["equipe"] = df_appartenances["equipe"].str.strip()
df_appartenances["date_debut"] = pd.to_datetime(df_appartenances["date_debut"])

#Importation des données de progression (après pour avoir les bonnes équipes)
df_progression = pd.read_csv("data/timing.csv")
df_progression["equipe"] = df_progression["equipe"].astype(str).str.strip()
df_progression["date"] = pd.to_datetime(df_progression["date"])

# Remplir les date_debut vides avec la première date de progression de l'équipe correspondante
date_debut_par_equipe = df_progression.groupby("equipe")["date"].min()
mask_vide = df_appartenances["date_debut"].isna()
df_appartenances.loc[mask_vide, "date_debut"] = df_appartenances.loc[mask_vide, "equipe"].map(date_debut_par_equipe)

# Trier par personne et par date
df_appartenances = df_appartenances.sort_values(by=["personne", "date_debut"])

# Calculer la date_fin
# La date_fin est soit la date de changement d'équipe (prochaine date_debut pour cette personne)
# soit la dernière date de progression de l'équipe
date_fin_par_equipe = df_progression.groupby("equipe")["date"].max()

df_appartenances["date_fin_changement"] = df_appartenances.groupby("personne")["date_debut"].shift(-1)
df_appartenances["date_fin_progression"] = df_appartenances["equipe"].map(date_fin_par_equipe)

# Prendre le minimum des deux (le premier événement qui arrive)
df_appartenances["date_fin"] = df_appartenances[["date_fin_changement", "date_fin_progression"]].min(axis=1)

# Supprimer les colonnes temporaires
df_appartenances = df_appartenances.drop(columns=["date_fin_changement", "date_fin_progression"])

#Calcul des dates de début et de fin des équipes
df_progression = df_progression.sort_values(by=["equipe", "date"]) # Trier par equipe et par date
df_debut_equipe = df_progression.groupby("equipe")["date"].shift(0)
df_fin_equipe = df_progression.groupby("equipe")["date"].shift(-1)


st.write(df_appartenances)

#Diagramme des equipes 
# Définir une palette de couleurs pour chaque équipe
couleurs_equipes = {
    "1": "#E74C3C",      # Rouge corail
    "2a": "#3498DB",     # Bleu ciel
    "2b": "#2980B9",     # Bleu océan
    "3": "#27AE60",      # Vert forêt
}
# Créer un dictionnaire de couleurs pour Plotly
color_map = {}
for equipe in df_appartenances["equipe"].unique():
    if str(equipe) in couleurs_equipes:
        color_map[str(equipe)] = couleurs_equipes[str(equipe)]
    else:
        color_map[str(equipe)] = "#95A5A6"  # Gris par défaut

# Préparer les données pour Plotly
# Créer un ordre de tri basé sur la date_debut et date_fin de chaque personne
# Trier d'abord par date_debut (décroissant), puis par date_fin (décroissant)
ordre_personnes = df_appartenances.groupby("personne").agg({
    "date_debut": "min",
    "date_fin": "max"
}).sort_values(by=["date_debut", "date_fin"], ascending=False).index.tolist()

# Tracer avec Plotly (plus interactif)
fig = px.timeline(
    df_appartenances,
    x_start="date_debut",
    x_end="date_fin",
    y="personne",
    color="equipe",
    color_discrete_map=color_map,
    title="Évolution des équipes dans le temps",
    labels={"nom_equipe": "Équipe", "personne": "personne"}
)

fig.update_yaxes(categoryorder="array", categoryarray=ordre_personnes)

st.plotly_chart(fig)



# Configuration de Streamlit
st.title("Chronogramme de l'explo")
st.write("Tout ce qui se passe sous terre reste sous terre...")

# Création du graphique interactif avec Plotly
fig = go.Figure()

# Ajouter une trace pour chaque série
for serie in df_progression['equipe'].unique():
    serie_data = df_progression[df_progression['equipe'] == serie]
    # Utiliser la couleur définie pour cette équipe
    couleur = color_map.get(str(serie), "#CCCCCC")
    fig.add_trace(go.Scatter(
        x=serie_data['date'],
        y=serie_data['profondeur'],
        mode='lines+markers',
        name=f"équipe {serie}",
        text=serie_data['commentaire'],  # Texte des commentaires pour chaque point
        line=dict(color=couleur),
        marker=dict(color=couleur),
        hoverinfo='text+x+y',  # Affiche les commentaires, l'heure (x) et la valeur (y)
    ))

# Personnalisation du graphique
fig.update_layout(
    title='Chronogramme détaillé',
    xaxis_title='Date',
    yaxis_title='Profondeur [m]',
    legend_title='Equipes',
    template='plotly_dark'  # ou 'plotly', 'ggplot2', 'seaborn', etc.
)

# Affichage du graphique dans Streamlit
st.plotly_chart(fig)

