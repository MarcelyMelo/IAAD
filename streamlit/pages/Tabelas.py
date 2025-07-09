import streamlit as st
import pandas as pd

st.header("Base de Dados - Filmes 🎬")

# conexão com a base de dados
conn = st.connection('mysql', type='sql')

# consultas sql
filme_df = conn.query("SELECT * FROM Filme")
elenco_df = conn.query("SELECT * FROM Elenco")
exibicao_df = conn.query("SELECT * FROM Exibicao")
canal_df = conn.query("SELECT * FROM Canal")

st.subheader("Filmes")
st.dataframe(filme_df)

st.subheader("Elenco")
st.dataframe(elenco_df)

st.subheader("Exibições")
st.dataframe(exibicao_df)

st.subheader("Canais")
st.dataframe(canal_df)
