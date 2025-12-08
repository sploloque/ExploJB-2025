import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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


#Importation des données de Timing
df_timing = pd.read_csv("data/timing.csv")

df_timing["date"] = pd.to_datetime(df_timing["date"])

# Configuration de Streamlit
st.title("Chronogramme de l'explo")
st.write("Tout ce qui se passe sous terre reste sous terre...")

# Création du graphique interactif avec Plotly
fig = go.Figure()

# Ajouter une trace pour chaque série
for serie in df_timing['equipe'].unique():
    serie_data = df_timing[df_timing['equipe'] == serie]
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

