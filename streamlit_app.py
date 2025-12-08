import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Show the page title and description.
st.set_page_config(page_title="Movies dataset", page_icon="🎬")
st.title("🎬 Movies dataset")
st.write(
    """
    This app visualizes data from [The Movie Database (TMDB)](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
    It shows which movie genre performed best at the box office over the years. Just 
    click on the widgets below to explore!
    """
)


#Importation des données de Timing
df_timing = pd.read_csv("data/timing.csv")

df_timing["date"] = pd.to_datetime(df_timing["date"])

# Configuration de Streamlit
st.title("Trace des valeurs par série")
st.write("Voici l'évolution des valeurs en fonction du temps pour chaque série.")

# Création du graphique interactif avec Plotly
fig = go.Figure()

# Ajouter une trace pour chaque série
for serie in df_timing['equipe'].unique():
    serie_data = df_timing[df_timing['equipe'] == serie]
    fig.add_trace(go.Scatter(
        x=serie_data['date'],
        y=serie_data['profondeur'],
        mode='lines+markers',
        name=f"équipe {serie}"
    ))

# Personnalisation du graphique
fig.update_layout(
    title='Évolution des valeurs par série',
    xaxis_title='Temps',
    yaxis_title='Valeur',
    legend_title='Série',
    template='plotly_dark'  # ou 'plotly', 'ggplot2', 'seaborn', etc.
)

# Affichage du graphique dans Streamlit
st.plotly_chart(fig)

