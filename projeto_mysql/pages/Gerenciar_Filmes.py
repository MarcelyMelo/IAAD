import streamlit as st
from sqlalchemy import text
import pandas as pd

st.set_page_config(layout="wide")
st.title("Gerênciar Filmes 🎞️")

if 'success_message' in st.session_state:
    st.success(st.session_state.success_message)
    del st.session_state.success_message

try:
    connection = st.connection("mysql", type="sql")
except Exception as e:
    st.error(f"Não foi possível conectar ao banco de dados: {e}")
    st.stop()

def get_all_movies():
    """Busca todos os filmes do banco de dados e retorna como DataFrame."""
    df = connection.query("SELECT * FROM filme ORDER BY nome ASC", ttl=0) 
    return df


# READ
st.header("Filmes Atualmente Cadastrados")
try:
    movies_df = get_all_movies()
    st.dataframe(movies_df, use_container_width=True)
except Exception as e:
    st.error(f"Erro ao buscar os fimes: {e}")
    movies_df = pd.DataFrame() 

st.header("Adicionar, Atualizar ou Remover um Filme")
if not movies_df.empty:
    movie_list = movies_df['nome'].tolist()
    selected_movie_name = st.selectbox(
        "Selecionar um filme para ATUALIZAR ou DELETAR",
        options=[""] + movie_list
    )
else:
    selected_movie_name = ""

# UPDATE e DELETE
if selected_movie_name:
    movie_details = movies_df[movies_df['nome'] == selected_movie_name].iloc[0]
    movie_id = int(movie_details['num_filme'])
    with st.form("update_movie_form"):
        st.subheader(f"Editando: {movie_details['nome']}")
        new_title = st.text_input("Título do Filme", value=movie_details['nome'])
        new_year = st.number_input("Ano de Lançamento", min_value=1900, max_value=2027, value=int(movie_details['ano']))
        new_duration = st.number_input("Duração (min)", min_value=0, step=1, value=int(movie_details['duracao']))
        update_button = st.form_submit_button("Atualizar Filme")
        if update_button:
            if not new_title.strip():
                st.error("O título do filme não pode ser vazio.")
            else:
                try:
                    update_query = text("UPDATE Filme SET nome = :nome, ano = :ano, duracao = :duracao WHERE num_filme = :id")
                    with connection.session as s:
                        s.execute(update_query, params={"nome": new_title, "ano": new_year, "duracao": new_duration, "id": movie_id})
                        s.commit()
                    st.session_state.success_message = f"Filme '{new_title}' atualizado com sucesso!"
                    st.rerun()
                except Exception as e:
                    st.error(f"Ocorreu um erro durante a atualização: {e}")
    if st.button(f"DELETAR o filme: {selected_movie_name}", type="primary"):
        try:
            delete_query = text("DELETE FROM Filme WHERE num_filme = :id")
            with connection.session as s:
                s.execute(delete_query, params={"id": movie_id})
                s.commit()
            st.session_state.success_message = f"O filme '{selected_movie_name}' foi deletado com sucesso."
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao deletar o filme: {e}")
            st.info("Este filme não pode ser excluído pois está associado a uma ou mais exibições. Remova as exibições relacionadas primeiro.")

# CREATE    
else:
    with st.form("create_movie_form"):
        st.subheader("Adicionar um Novo Filme")
        title = st.text_input("Título do Filme")
        year = st.number_input("Ano de Lançamento", min_value=1900, max_value=2027, value=2025)
        duration = st.number_input("Duração (min)", min_value=0, step=1)
        submit_button = st.form_submit_button("Adicionar Filme")
        if submit_button:
            if not title.strip():
                st.error("O título do filme não pode ser vazio.")
            else:
                try:
                    insert_query = text("INSERT INTO Filme (nome, ano, duracao) VALUES (:nome, :ano, :duracao)")
                    with connection.session as s:
                        s.execute(insert_query, params={"nome": title, "ano": year, "duracao": duration})
                        s.commit()
                    st.session_state.success_message = f"Filme '{title}' adicionado com sucesso!"
                    st.rerun()
                except Exception as e:
                    st.error(f"Ocorreu um erro ao adicionar o filme: {e}")
