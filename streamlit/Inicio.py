import streamlit as st
import pandas as pd

# Define the pages
main_page = st.Page("pages/Main.py", title="Base de dados - Filmes", icon="🎬")
gerenciar_filmes = st.Page("pages/Gerenciar_Filmes.py", title="Gerenciar Filmes", icon="📝")
gerenciar_canais = st.Page("pages/Gerenciar_Canais.py", title="Gerenciar Canais", icon="👥")

# Set up navigation
pg = st.navigation([main_page, gerenciar_filmes, gerenciar_canais])

# Run the selected page
pg.run()



