import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Consultas Avançadas 📊")

try:
    conn = st.connection("mysql", type="sql")
except Exception as e:
    st.error(f"Erro de conexão: {e}")
    st.stop()

def plot_with_table(df, x_col, y_col, title, color_scale, x_label, y_label):
    col1, col2 = st.columns([1, 2])

    with col1:
        st.dataframe(df, use_container_width=True, height=400)  # Altura fixa para a tabela

    with col2:
        df_sorted = df.sort_values(x_col)
        fig = px.bar(
            df_sorted,
            x=x_col,
            y=y_col,
            orientation='h',
            labels={x_col: x_label, y_col: y_label},
            color=x_col,
            color_continuous_scale=color_scale,
            title=title,
            height=400  # Altura fixa para alinhar com tabela
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

# Consulta 1
st.subheader("1️⃣ Duração Média dos Filmes por Canal")
try:
    query1 = """
    SELECT C.nome AS Canal, ROUND(AVG(F.duracao), 2) AS Duracao_Media
    FROM Filme F
    JOIN Exibicao E ON F.num_filme = E.num_filme
    JOIN Canal C ON E.num_canal = C.num_canal
    GROUP BY C.nome
    ORDER BY Duracao_Media DESC;
    """
    resultado1 = conn.query(query1, ttl=0)
    plot_with_table(resultado1, "Duracao_Media", "Canal", "🎬 Duração Média por Canal", "Blues", "Duração Média (min)", "Canal")
except Exception as e:
    st.error(f"Erro na consulta 1: {e}")

# Consulta 2
st.subheader("2️⃣ Top 10 Filmes com Mais Exibições")
try:
    query2 = """
    SELECT F.nome AS Filme, COUNT(*) AS Qtde_Exibicoes
    FROM Filme F
    JOIN Exibicao E ON F.num_filme = E.num_filme
    GROUP BY F.nome
    ORDER BY Qtde_Exibicoes DESC
    LIMIT 10;
    """
    resultado2 = conn.query(query2, ttl=0)
    plot_with_table(resultado2, "Qtde_Exibicoes", "Filme", "📺 Top 10 Filmes Mais Exibidos", "Greens", "Quantidade de Exibições", "Filme")
except Exception as e:
    st.error(f"Erro na consulta 2: {e}")

# Consulta 3 (só tabela, sem gráfico)
st.subheader("3️⃣ Últimas Exibições Realizadas (Últimos 30 dias)")
try:
    query3 = """
    SELECT F.nome AS Filme, C.nome AS Canal, E.data_exibicao, E.hora_exibicao
    FROM Exibicao E
    JOIN Filme F ON E.num_filme = F.num_filme
    JOIN Canal C ON E.num_canal = C.num_canal
    WHERE E.data_exibicao >= CURDATE() - INTERVAL 30 DAY
    ORDER BY E.data_exibicao DESC, E.hora_exibicao DESC;
    """
    resultado3 = conn.query(query3, ttl=0)
    st.dataframe(resultado3, use_container_width=True)
except Exception as e:
    st.error(f"Erro na consulta 3: {e}")
