import streamlit as st
from sqlalchemy import text
import pandas as pd

st.set_page_config(layout="wide")
st.title("Gerenciar Canais 📺")

if 'success_message' in st.session_state:
    st.success(st.session_state.success_message)
    del st.session_state.success_message

try:
    connection = st.connection("mysql", type="sql")
except Exception as e:
    st.error(f"Não foi possível conectar ao banco de dados: {e}")
    st.stop()

def get_all_channels():
    """Busca todos os canais do banco de dados e retorna como DataFrame."""
    df = connection.query("SELECT * FROM Canal ORDER BY nome ASC", ttl=0) 
    return df


# READ
st.header("Canais Atualmente Cadastrados")
try:
    channels_df = get_all_channels()
    st.dataframe(channels_df, use_container_width=True)
except Exception as e:
    st.error(f"Erro ao buscar os canais: {e}")
    channels_df = pd.DataFrame() 

st.header("Adicionar, Atualizar ou Remover um Canal")
if not channels_df.empty:
    channel_list = channels_df['nome'].tolist()
    selected_channel_name = st.selectbox(
        "Selecionar um canal para ATUALIZAR ou DELETAR",
        options=[""] + channel_list
    )
else:
    selected_channel_name = ""

# UPDATE e DELETE
if selected_channel_name:
    channel_details = channels_df[channels_df['nome'] == selected_channel_name].iloc[0]
    channel_id = int(channel_details['num_canal'])
    with st.form("update_channel_form"):
        st.subheader(f"Editando: {channel_details['nome']}")
        new_name = st.text_input("Nome do Canal", value=channel_details['nome'])
        new_channel_number = st.number_input("Número do Canal", min_value=0, step=1, value=int(channel_details['num_canal']))
        update_button = st.form_submit_button("Atualizar Canal")
        if update_button:
            if not new_name.strip():
                st.error("O nome do canal não pode ser vazio.")
            else:
                try:
                    # Verificar se o novo número não está sendo usado por outro canal
                    if new_channel_number != channel_id:
                        check_query = text("SELECT COUNT(*) FROM Canal WHERE num_canal = :num_canal")
                        with connection.session as s:
                            result = s.execute(check_query, params={"num_canal": new_channel_number}).scalar()
                            if result > 0:
                                st.error(f"Já existe um canal com o número {new_channel_number}. Escolha outro número.")
                                st.stop()
                    
                    update_query = text("UPDATE Canal SET nome = :nome, num_canal = :num_canal WHERE num_canal = :id")
                    with connection.session as s:
                        s.execute(update_query, params={"nome": new_name, "num_canal": new_channel_number, "id": channel_id})
                        s.commit()
                    st.session_state.success_message = f"Canal '{new_name}' atualizado com sucesso!"
                    st.rerun()
                except Exception as e:
                    if "foreign key constraint fails" in str(e):
                        st.error("Não é possível alterar o número do canal porque ele está vinculado a exibições existentes.")
                        st.info("Edite ou remova as exibições associadas antes de modificar este canal.")
                    else:
                        st.error(f"Ocorreu um erro durante a atualização: {e}")
    
    if st.button(f"DELETAR o canal: {selected_channel_name}", type="primary"):
        try:
            delete_query = text("DELETE FROM Canal WHERE num_canal = :id")
            with connection.session as s:
                s.execute(delete_query, params={"id": channel_id})
                s.commit()
            st.session_state.success_message = f"O canal '{selected_channel_name}' foi deletado com sucesso."
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao deletar o canal: {e}")
            st.info("Este canal não pode ser excluído pois está associado a uma ou mais exibições. Remova as exibições relacionadas primeiro.")

# CREATE    
else:
    with st.form("create_channel_form"):
        st.subheader("Adicionar um Novo Canal")
        name = st.text_input("Nome do Canal")
        channel_number = st.number_input("Número do Canal", min_value=0, step=1)
        submit_button = st.form_submit_button("Adicionar Canal")
        if submit_button:
            if not name.strip():
                st.error("O nome do canal não pode ser vazio.")
            else:
                try:
                    # Verificar se o número do canal já existe
                    check_query = text("SELECT COUNT(*) FROM Canal WHERE num_canal = :num_canal")
                    with connection.session as s:
                        result = s.execute(check_query, params={"num_canal": channel_number}).scalar()
                        if result > 0:
                            st.error(f"Já existe um canal com o número {channel_number}. Escolha outro número.")
                        else:
                            insert_query = text("INSERT INTO Canal (nome, num_canal) VALUES (:nome, :num_canal)")
                            s.execute(insert_query, params={"nome": name, "num_canal": channel_number})
                            s.commit()
                            st.session_state.success_message = f"Canal '{name}' adicionado com sucesso!"
                            st.rerun()
                except Exception as e:
                    st.error(f"Ocorreu um erro ao adicionar o canal: {e}")