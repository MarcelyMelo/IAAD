import streamlit as st
from sqlalchemy import text
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide")
st.title("Gerenciar Exibições 📺")

if 'success_message' in st.session_state:
    st.success(st.session_state.success_message)
    del st.session_state.success_message

try:
    connection = st.connection("mysql", type="sql")
except Exception as e:
    st.error(f"Não foi possível conectar ao banco de dados: {e}")
    st.stop()

def get_all_exhibitions():
    """Busca todas as exibições do banco de dados e retorna como DataFrame."""
    df = connection.query("""
        SELECT e.num_filme, f.nome as filme_nome, e.num_canal, c.nome as canal_nome, 
               e.data_exibicao, e.hora_exibicao 
        FROM Exibicao e 
        JOIN Filme f ON e.num_filme = f.num_filme 
        JOIN Canal c ON e.num_canal = c.num_canal 
        ORDER BY e.data_exibicao DESC, e.hora_exibicao DESC
    """, ttl=0) 
    return df

def get_all_movies():
    """Busca todos os filmes para o dropdown."""
    df = connection.query("SELECT num_filme, nome FROM Filme ORDER BY nome ASC", ttl=0)
    return df

def get_all_channels():
    """Busca todos os canais para o dropdown."""
    df = connection.query("SELECT num_canal, nome FROM Canal ORDER BY nome ASC", ttl=0)
    return df

# READ
st.header("Exibições Atualmente Cadastradas")
try:
    exhibitions_df = get_all_exhibitions()
    st.dataframe(exhibitions_df, use_container_width=True)
except Exception as e:
    st.error(f"Erro ao buscar as exibições: {e}")
    exhibitions_df = pd.DataFrame()

# Buscar filmes e canais para os dropdowns
try:
    movies_df = get_all_movies()
    movie_options = {f"{row['nome']} (ID: {row['num_filme']})": row['num_filme'] 
                    for _, row in movies_df.iterrows()}
except Exception as e:
    st.error(f"Erro ao buscar filmes: {e}")
    movie_options = {}

try:
    channels_df = get_all_channels()
    channel_options = {f"{row['nome']} (Canal: {row['num_canal']})": row['num_canal'] 
                      for _, row in channels_df.iterrows()}
except Exception as e:
    st.error(f"Erro ao buscar canais: {e}")
    channel_options = {}

st.header("Adicionar, Atualizar ou Remover uma Exibição")
if not exhibitions_df.empty:
    exhibition_list = [f"{row['filme_nome']} - {row['canal_nome']} - {row['data_exibicao']} às {row['hora_exibicao']}" 
                      for _, row in exhibitions_df.iterrows()]
    selected_exhibition = st.selectbox(
        "Selecionar uma exibição para ATUALIZAR ou DELETAR",
        options=[""] + exhibition_list
    )
else:
    selected_exhibition = ""

# UPDATE e DELETE
if selected_exhibition:
    # Extrair informações da exibição selecionada
    selected_index = exhibition_list.index(selected_exhibition)
    exhibition_details = exhibitions_df.iloc[selected_index]
    
    with st.form("update_exhibition_form"):
        st.subheader(f"Editando: {exhibition_details['filme_nome']} - {exhibition_details['canal_nome']}")
        
        # Dropdown para selecionar filme
        current_movie_key = f"{exhibition_details['filme_nome']} (ID: {exhibition_details['num_filme']})"
        selected_movie_key = st.selectbox(
            "Filme", 
            options=list(movie_options.keys()),
            index=list(movie_options.keys()).index(current_movie_key) if current_movie_key in movie_options else 0
        )
        new_movie_id = movie_options[selected_movie_key]
        
        # Dropdown para selecionar canal
        current_channel_key = f"{exhibition_details['canal_nome']} (Canal: {exhibition_details['num_canal']})"
        selected_channel_key = st.selectbox(
            "Canal", 
            options=list(channel_options.keys()),
            index=list(channel_options.keys()).index(current_channel_key) if current_channel_key in channel_options else 0
        )
        new_channel_id = channel_options[selected_channel_key]
        
        # Campos de data e hora
        current_date = pd.to_datetime(exhibition_details['data_exibicao']).date()
        new_date = st.date_input("Data da Exibição", value=current_date)
        
        current_time = pd.to_datetime(str(exhibition_details['hora_exibicao']), format='%H:%M:%S').time()
        new_time = st.time_input("Hora da Exibição", value=current_time)
        
        update_button = st.form_submit_button("Atualizar Exibição")
        if update_button:
            try:
                # Verificar se já existe essa combinação (evitar duplicatas)
                original_key = (exhibition_details['num_filme'], exhibition_details['num_canal'], 
                              exhibition_details['data_exibicao'], exhibition_details['hora_exibicao'])
                new_key = (new_movie_id, new_channel_id, new_date, new_time)
                
                if original_key != new_key:
                    check_query = text("""
                        SELECT COUNT(*) FROM Exibicao 
                        WHERE num_filme = :num_filme AND num_canal = :num_canal 
                        AND data_exibicao = :data_exibicao AND hora_exibicao = :hora_exibicao
                    """)
                    with connection.session as s:
                        result = s.execute(check_query, params={
                            "num_filme": new_movie_id,
                            "num_canal": new_channel_id,
                            "data_exibicao": new_date,
                            "hora_exibicao": new_time
                        }).scalar()
                        if result > 0:
                            st.error(f"Já existe uma exibição para este filme neste canal na data e hora especificadas.")
                            st.stop()
                
                # Atualizar o registro
                update_query = text("""
                    UPDATE Exibicao 
                    SET num_filme = :new_num_filme, num_canal = :new_num_canal, 
                        data_exibicao = :new_data_exibicao, hora_exibicao = :new_hora_exibicao 
                    WHERE num_filme = :old_num_filme AND num_canal = :old_num_canal 
                    AND data_exibicao = :old_data_exibicao AND hora_exibicao = :old_hora_exibicao
                """)
                with connection.session as s:
                    s.execute(update_query, params={
                        "new_num_filme": new_movie_id,
                        "new_num_canal": new_channel_id,
                        "new_data_exibicao": new_date,
                        "new_hora_exibicao": new_time,
                        "old_num_filme": exhibition_details['num_filme'],
                        "old_num_canal": exhibition_details['num_canal'],
                        "old_data_exibicao": exhibition_details['data_exibicao'],
                        "old_hora_exibicao": exhibition_details['hora_exibicao']
                    })
                    s.commit()
                st.session_state.success_message = f"Exibição atualizada com sucesso!"
                st.rerun()
            except Exception as e:
                st.error(f"Ocorreu um erro durante a atualização: {e}")
    
    if st.button(f"DELETAR: {exhibition_details['filme_nome']} - {exhibition_details['canal_nome']}", type="primary"):
        try:
            delete_query = text("""
                DELETE FROM Exibicao 
                WHERE num_filme = :num_filme AND num_canal = :num_canal 
                AND data_exibicao = :data_exibicao AND hora_exibicao = :hora_exibicao
            """)
            with connection.session as s:
                s.execute(delete_query, params={
                    "num_filme": exhibition_details['num_filme'],
                    "num_canal": exhibition_details['num_canal'],
                    "data_exibicao": exhibition_details['data_exibicao'],
                    "hora_exibicao": exhibition_details['hora_exibicao']
                })
                s.commit()
            st.session_state.success_message = f"A exibição foi deletada com sucesso."
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao deletar a exibição: {e}")

# CREATE    
else:
    with st.form("create_exhibition_form"):
        st.subheader("Adicionar uma Nova Exibição")
        
        # Dropdown para selecionar filme
        if movie_options:
            selected_movie_key = st.selectbox("Filme", options=list(movie_options.keys()))
            movie_id = movie_options[selected_movie_key]
        else:
            st.error("Nenhum filme encontrado. Adicione filmes primeiro.")
            st.stop()
        
        # Dropdown para selecionar canal
        if channel_options:
            selected_channel_key = st.selectbox("Canal", options=list(channel_options.keys()))
            channel_id = channel_options[selected_channel_key]
        else:
            st.error("Nenhum canal encontrado. Adicione canais primeiro.")
            st.stop()
        
        # Campos de data e hora
        exhibition_date = st.date_input("Data da Exibição", value=datetime.now().date())
        exhibition_time = st.time_input("Hora da Exibição", value=time(20, 0))
        
        submit_button = st.form_submit_button("Adicionar Exibição")
        if submit_button:
            try:
                # Verificar se já existe essa combinação
                check_query = text("""
                    SELECT COUNT(*) FROM Exibicao 
                    WHERE num_filme = :num_filme AND num_canal = :num_canal 
                    AND data_exibicao = :data_exibicao AND hora_exibicao = :hora_exibicao
                """)
                with connection.session as s:
                    result = s.execute(check_query, params={
                        "num_filme": movie_id,
                        "num_canal": channel_id,
                        "data_exibicao": exhibition_date,
                        "hora_exibicao": exhibition_time
                    }).scalar()
                    if result > 0:
                        st.error(f"Já existe uma exibição para este filme neste canal na data e hora especificadas.")
                    else:
                        insert_query = text("""
                            INSERT INTO Exibicao (num_filme, num_canal, data_exibicao, hora_exibicao) 
                            VALUES (:num_filme, :num_canal, :data_exibicao, :hora_exibicao)
                        """)
                        s.execute(insert_query, params={
                            "num_filme": movie_id,
                            "num_canal": channel_id,
                            "data_exibicao": exhibition_date,
                            "hora_exibicao": exhibition_time
                        })
                        s.commit()
                        st.session_state.success_message = f"Exibição adicionada com sucesso!"
                        st.rerun()
            except Exception as e:
                st.error(f"Ocorreu um erro ao adicionar a exibição: {e}")