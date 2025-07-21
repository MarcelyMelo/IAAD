import streamlit as st
import pandas as pd

# Define the pages
main_page = st.Page("pages/Main.py", title="Base de dados - Filmes", icon="🎬")
gerenciar_filmes = st.Page("pages/Gerenciar_Filmes.py",
                           title="Gerenciar Filmes", icon="📝")
gerenciar_canais = st.Page("pages/Gerenciar_Canais.py",
                           title="Gerenciar Canais", icon="👥")
gerenciar_elenco = st.Page("pages/Gerenciar_Elenco.py",
                           title="Gerenciar Elenco", icon="🎭")
gerenciar_exibicao = st.Page("pages/Gerenciar_Exibicao.py",
                            title="Gerenciar Exibições", icon="📺")
consultas_avancadas = st.Page(
    "pages/consultas_extra.py", title="Consultas Avançadas", icon="📊")


# Set up navigation
pg = st.navigation([main_page, gerenciar_filmes, gerenciar_canais, 
                   gerenciar_elenco, gerenciar_exibicao, consultas_avancadas])

# Run the selected page
pg.run()
