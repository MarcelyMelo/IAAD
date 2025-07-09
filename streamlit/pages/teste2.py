import streamlit as st
from sqlalchemy import text

st.title("Cadastro de Filme 🎬")

conn = st.connection("mysql", type="sql")

with st.form("cadastro_filme"):
    title = st.text_input("Título do filme")
    data_lancamento = st.date_input("Data de lançamento")
    ano = data_lancamento.year
    duracao = st.number_input("Duração (min)", min_value=0, step=1)

    submit = st.form_submit_button("Cadastrar Filme")

if submit:
    if not title.strip():
        st.error("Título não pode ser vazio.")
    else:
        try:
            conn.session.execute(
                text("INSERT INTO Filme (nome, ano, duracao) VALUES (:nome, :ano, :duracao)"),
                params={"nome": title, "ano": ano, "duracao": int(duracao)}
            )
            conn.session.commit()

            # Query para confirmar inserção
            ultimo = conn.query("SELECT * FROM Filme ORDER BY num_filme DESC LIMIT 1")
            st.write("Último filme inserido:", ultimo)
        except Exception as e:
            st.error(f"Erro ao cadastrar: {e}")


# Sempre recarrega a lista atualizada de filmes do banco

filme_df = conn.query('SELECT * FROM Filme')
st.write(filme_df)

db_name = conn.query("SELECT DATABASE() AS db").iloc[0]['db']
st.write(f"Banco de dados conectado: {db_name}")
