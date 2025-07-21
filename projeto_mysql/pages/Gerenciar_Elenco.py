import streamlit as st
from sqlalchemy import text
import pandas as pd

st.set_page_config(layout="wide")
st.title("Gerenciar Elenco 🎭")

if 'success_message' in st.session_state:
    st.success(st.session_state.success_message)
    del st.session_state.success_message

try:
    connection = st.connection("mysql", type="sql")
except Exception as e:
    st.error(f"Não foi possível conectar ao banco de dados: {e}")
    st.stop()

def get_all_cast():
    """Busca todo o elenco do banco de dados e retorna como DataFrame."""
    df = connection.query("""
        SELECT e.num_filme, f.nome as filme_nome, e.nome_ator, e.protagonista 
        FROM Elenco e 
        JOIN Filme f ON e.num_filme = f.num_filme 
        ORDER BY f.nome ASC, e.nome_ator ASC
    """, ttl=0) 
    return df

def get_all_movies():
    """Busca todos os filmes para o dropdown."""
    df = connection.query("SELECT num_filme, nome FROM Filme ORDER BY nome ASC", ttl=0)
    return df

# READ
st.header("Elenco Atualmente Cadastrado")
try:
    cast_df = get_all_cast()
    st.dataframe(cast_df, use_container_width=True)
except Exception as e:
    st.error(f"Erro ao buscar o elenco: {e}")
    cast_df = pd.DataFrame()

# Buscar filmes para o dropdown
try:
    movies_df = get_all_movies()
    movie_options = {f"{row['nome']} (ID: {row['num_filme']})": row['num_filme'] 
                    for _, row in movies_df.iterrows()}
except Exception as e:
    st.error(f"Erro ao buscar filmes: {e}")
    movie_options = {}

st.header("Adicionar, Atualizar ou Remover um Ator do Elenco")
if not cast_df.empty:
    cast_list = [f"{row['nome_ator']} - {row['filme_nome']} (ID: {row['num_filme']})" 
                for _, row in cast_df.iterrows()]
    selected_cast = st.selectbox(
        "Selecionar um ator para ATUALIZAR ou DELETAR",
        options=[""] + cast_list
    )
else:
    selected_cast = ""

# UPDATE e DELETE
if selected_cast:
    # Extrair informações do ator selecionado
    selected_index = cast_list.index(selected_cast)
    cast_details = cast_df.iloc[selected_index]
    
    with st.form("update_cast_form"):
        st.subheader(f"Editando: {cast_details['nome_ator']} - {cast_details['filme_nome']}")
        
        # Dropdown para selecionar filme
        current_movie_key = f"{cast_details['filme_nome']} (ID: {cast_details['num_filme']})"
        selected_movie_key = st.selectbox(
            "Filme", 
            options=list(movie_options.keys()),
            index=list(movie_options.keys()).index(current_movie_key) if current_movie_key in movie_options else 0
        )
        new_movie_id = movie_options[selected_movie_key]
        
        new_actor_name = st.text_input("Nome do Ator", value=cast_details['nome_ator'])
        new_is_protagonist = st.checkbox("É protagonista?", value=bool(cast_details['protagonista']))
        
        update_button = st.form_submit_button("Atualizar Elenco")
        if update_button:
            if not new_actor_name.strip():
                st.error("O nome do ator não pode ser vazio.")
            else:
                try:
                    # Verificar se já existe esse ator neste filme (evitar duplicatas)
                    if not (new_movie_id == cast_details['num_filme'] and new_actor_name == cast_details['nome_ator']):
                        check_query = text("SELECT COUNT(*) FROM Elenco WHERE num_filme = :num_filme AND nome_ator = :nome_ator")
                        with connection.session as s:
                            result = s.execute(check_query, params={"num_filme": new_movie_id, "nome_ator": new_actor_name}).scalar()
                            if result > 0:
                                st.error(f"O ator '{new_actor_name}' já está cadastrado no filme selecionado.")
                                st.stop()
                    
                    # Atualizar o registro
                    update_query = text("""
                        UPDATE Elenco 
                        SET num_filme = :new_num_filme, nome_ator = :new_nome_ator, protagonista = :new_protagonista 
                        WHERE num_filme = :old_num_filme AND nome_ator = :old_nome_ator
                    """)
                    with connection.session as s:
                        s.execute(update_query, params={
                            "new_num_filme": new_movie_id,
                            "new_nome_ator": new_actor_name,
                            "new_protagonista": new_is_protagonist,
                            "old_num_filme": cast_details['num_filme'],
                            "old_nome_ator": cast_details['nome_ator']
                        })
                        s.commit()
                    st.session_state.success_message = f"Elenco atualizado com sucesso!"
                    st.rerun()
                except Exception as e:
                    st.error(f"Ocorreu um erro durante a atualização: {e}")
    
    if st.button(f"DELETAR: {cast_details['nome_ator']} - {cast_details['filme_nome']}", type="primary"):
        try:
            delete_query = text("DELETE FROM Elenco WHERE num_filme = :num_filme AND nome_ator = :nome_ator")
            with connection.session as s:
                s.execute(delete_query, params={
                    "num_filme": cast_details['num_filme'],
                    "nome_ator": cast_details['nome_ator']
                })
                s.commit()
            st.session_state.success_message = f"O ator '{cast_details['nome_ator']}' foi removido do filme '{cast_details['filme_nome']}' com sucesso."
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao deletar o registro do elenco: {e}")

# CREATE    
else:
    with st.form("create_cast_form"):
        st.subheader("Adicionar um Novo Ator ao Elenco")
        
        # Dropdown para selecionar filme
        if movie_options:
            selected_movie_key = st.selectbox("Filme", options=list(movie_options.keys()))
            movie_id = movie_options[selected_movie_key]
        else:
            st.error("Nenhum filme encontrado. Adicione filmes primeiro.")
            st.stop()
        
        actor_name = st.text_input("Nome do Ator")
        is_protagonist = st.checkbox("É protagonista?")
        
        submit_button = st.form_submit_button("Adicionar ao Elenco")
        if submit_button:
            if not actor_name.strip():
                st.error("O nome do ator não pode ser vazio.")
            else:
                try:
                    # Verificar se já existe esse ator neste filme
                    check_query = text("SELECT COUNT(*) FROM Elenco WHERE num_filme = :num_filme AND nome_ator = :nome_ator")
                    with connection.session as s:
                        result = s.execute(check_query, params={"num_filme": movie_id, "nome_ator": actor_name}).scalar()
                        if result > 0:
                            st.error(f"O ator '{actor_name}' já está cadastrado no filme selecionado.")
                        else:
                            insert_query = text("INSERT INTO Elenco (num_filme, nome_ator, protagonista) VALUES (:num_filme, :nome_ator, :protagonista)")
                            s.execute(insert_query, params={
                                "num_filme": movie_id,
                                "nome_ator": actor_name,
                                "protagonista": is_protagonist
                            })
                            s.commit()
                            st.session_state.success_message = f"Ator '{actor_name}' adicionado ao elenco com sucesso!"
                            st.rerun()
                except Exception as e:
                    st.error(f"Ocorreu um erro ao adicionar o ator: {e}")