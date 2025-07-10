import streamlit as st
import pandas as pd

# Define the pages
main_page = st.Page("pages/Tabelas.py", title="Base de dados - Filmes", icon="🎬")
page_crud = st.Page("pages/Gerenciar_Filmes.py", title="Gerenciar Filmes", icon="📝")
page_2 = st.Page("pages/Teste.py", title="Cadastrar Filmes", icon="❄️")
page_3 = st.Page("pages/teste2.py", title="Page 3", icon="🎉")

# Set up navigation
pg = st.navigation([main_page, page_crud, page_2, page_3])

# Run the selected page
pg.run()



