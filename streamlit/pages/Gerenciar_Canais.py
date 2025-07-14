import streamlit as st
from sqlalchemy import text
import pandas as pd

st.set_page_config(layout="wide")
st.title("Gerenciar Canais")

if 'success_message' in st.session_state:
    st.success(st.session_state.success_message)
    del st.session_state.success_message

# Conexão com o banco de dados
try:
    connection = st.connection("mysql", type="sql")
except Exception as e:
    st.error(f"Não foi possível conectar ao banco de dados: {e}")
    st.stop()

# Função para buscar os canais
def get_all_movies():
    df = connection.query("SELECT * FROM Canal", ttl=0)  # Sem cache
    return df

# Exibir canais cadastrados
st.header("📋 Canais Atualmente Cadastrados")
try:
    movies_df = get_all_movies()
    st.dataframe(movies_df, use_container_width=True)
except Exception as e:
    st.error(f"Erro ao buscar os canais: {e}")
    movies_df = pd.DataFrame()

# Formulário único para Adicionar / Editar / Deletar
st.header("✏️ Adicionar, Atualizar ou Remover um Canal")

selected_movie_name = ""
movie_id = None
movie_list = movies_df['nome'].tolist() if not movies_df.empty else []

selected_movie_name = st.selectbox(
    "Selecione um canal para editar ou deletar (ou deixe em branco para adicionar novo):",
    options=[""] + movie_list
)

# Determinar valores iniciais
if selected_movie_name:
    movie_details = movies_df[movies_df['nome'] == selected_movie_name].iloc[0]
    movie_id = int(movie_details['num_canal'])
    default_title = movie_details['nome']
    default_canal_number = int(movie_details['num_canal'])
else:
    default_title = ""
    default_canal_number = 0

with st.form("canal_form"):
    title = st.text_input("Nome do canal", value=default_title)
    new_canal_number = st.number_input("Número do canal", min_value=0, step=1, value=default_canal_number)
    col1, col2 = st.columns(2)
    with col1:
        submit_button = st.form_submit_button("Salvar")
    with col2:
        delete_button = st.form_submit_button("Deletar", type="primary")

    if submit_button:
        if not title.strip():
            st.error("O título do canal não pode ser vazio.")
        else:
            try:
                with connection.session as s:
                    if selected_movie_name:
                        # Atualização
                        update_query = text("""
                            UPDATE Canal 
                            SET nome = :nome, num_canal = :num_canal 
                            WHERE num_canal = :id
                        """)
                        s.execute(update_query, params={
                            "nome": title, 
                            "num_canal": new_canal_number, 
                            "id": movie_id
                        })
                        s.commit()
                        st.session_state.success_message = f"Canal '{title}' atualizado com sucesso!"
                    else:
                        # Verificar duplicação
                        check_query = text("SELECT COUNT(*) FROM Canal WHERE num_canal = :num_canal")
                        result = s.execute(check_query, params={"num_canal": new_canal_number}).scalar()
                        if result > 0:
                            st.warning(f"Já existe um canal com o número {new_canal_number}. Escolha outro número.")
                        else:
                            # Inserção
                            insert_query = text("INSERT INTO Canal (nome, num_canal) VALUES (:nome, :num_canal)")
                            s.execute(insert_query, params={"nome": title, "num_canal": new_canal_number})
                            s.commit()
                            st.session_state.success_message = f"Canal '{title}' adicionado com sucesso!"
                st.rerun()
            except Exception as e:
                if "foreign key constraint fails" in str(e):
                    st.error("Não é possível alterar o número do canal porque ele está vinculado a exibições existentes.")
                    st.info("Edite ou remova as exibições associadas antes de modificar este canal.")
                else:
                    st.error(f"Ocorreu um erro: {e}")

    if delete_button and selected_movie_name:
        try:
            delete_query = text("DELETE FROM Canal WHERE num_canal = :id")
            with connection.session as s:
                s.execute(delete_query, params={"id": movie_id})
                s.commit()
            st.session_state.success_message = f"O canal '{selected_movie_name}' foi deletado com sucesso."
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao deletar o canal: {e}")
            st.info("Este canal não pode ser excluído pois está associado a exibições.")
