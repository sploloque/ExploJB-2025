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
    Un petit aperçu de l'explo à venir ? C'est ici !
    Pour ceux qui ne connaissent pas le réseau par coeur : \n
    La coupe du JB : https://groupe-speleo-vulcain.com/wp-content/uploads/2025/07/jb-2025-coupe.pdf \n
    Le plan du JB : https://groupe-speleo-vulcain.com/wp-content/uploads/2025/05/jb-2025-plan1000.pdf \n
    (Merci Xa !)
    """
)


#Importation des données de progression
df_progression = pd.read_csv("data/timing.csv")
df_progression["date"] = pd.to_datetime(df_progression["date"])

#Calcul des dates de début et de fin des équipes
df_progression = df_progression.sort_values(by=["equipe", "date"]) # Trier par equipe et par date
df_debut_equipe = df_progression.groupby("equipe")["date"].shift(0)
df_fin_equipe = df_progression.groupby("equipe")["date"].shift(-1) 


#Importation des données d'appartenances
df_appartenances = pd.read_csv("data/equipes.csv")
df_appartenances["date_debut"] = pd.to_datetime(df_appartenances["date_debut"])

    

# Trier par personne et par date
df_appartenances = df_appartenances.sort_values(by=["personne", "date_debut"])

# Calculer la date_fin
df_appartenances["date_fin"] = df_appartenances.groupby("personne")["date_debut"].shift(-1)


#Diagramme des equipes 
# Préparer les données pour Plotly
df_appartenances["date_fin"] = df_appartenances["date_fin"].fillna(pd.to_datetime("2025-12-31"))  # Remplacer NaN par une date future

# Tracer avec Plotly (plus interactif)
fig = px.timeline(
    df_appartenances,
    x_start="date_debut",
    x_end="date_fin",
    y="personne",
    color="equipe",
    title="Évolution des équipes dans le temps",
    labels={"nom_equipe": "Équipe", "personne": "personne"}
)

fig.update_yaxes(categoryorder="total ascending")

st.plotly_chart(fig)



# Configuration de Streamlit
st.title("Chronogramme de l'explo")
st.write("Tout ce qui se passe sous terre reste sous terre...")

# Création du graphique interactif avec Plotly
fig = go.Figure()

# Ajouter une trace pour chaque série
for serie in df_progression['equipe'].unique():
    serie_data = df_progression[df_progression['equipe'] == serie]
    fig.add_trace(go.Scatter(
        x=serie_data['date'],
        y=serie_data['profondeur'],
        mode='lines+markers',
        name=f"équipe {serie}",
        text=serie_data['commentaire'],  # Texte des commentaires pour chaque point
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

