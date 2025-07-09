import streamlit as st
from sqlalchemy import Column, Integer, String, SmallInteger, create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 1. Modelo SQLAlchemy
class Base(DeclarativeBase):
    pass

class Filme(Base):
    __tablename__ = "Filme"
    num_filme = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    ano = Column(SmallInteger, nullable=False)
    duracao = Column(Integer)

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/filmes"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# 3. Criar tabela (se não existir)
Base.metadata.create_all(bind=engine)

# 4. Streamlit app
st.title("Cadastro de Filmes 🎬")

with st.form("cadastro_filme"):
    title = st.text_input("Título do filme")
    ano = st.number_input("Ano de lançamento", min_value=1900, max_value=2100, value=2025)
    duracao = st.number_input("Duração (min)", min_value=0, step=1)

    submit = st.form_submit_button("Cadastrar Filme")

if submit:
    if not title.strip():
        st.error("Título não pode ser vazio.")
    else:
        with SessionLocal() as session:
            novo_filme = Filme(nome=title, ano=ano, duracao=duracao)
            session.add(novo_filme)
            session.commit()
            st.success(f"Filme '{title}' cadastrado com sucesso!")

# 5. Mostrar lista atualizada de filmes
with SessionLocal() as session:
    filmes = session.query(Filme).order_by(Filme.num_filme.desc()).all()

if filmes:
    filmes_data = [
        {"ID": f.num_filme, "Nome": f.nome, "Ano": f.ano, "Duração": f.duracao} for f in filmes
    ]
    st.subheader("Filmes cadastrados")
    st.dataframe(filmes_data)
else:
    st.write("Nenhum filme cadastrado ainda.")


"""
melhorias que quero fazer:

entender o que é o "Base"
colocar o secrets.toml conectado no lugar do SQLALCHEMY_DATABASE_URL
deixar o código todo em inglês pq ele tá todo meio a meio


"""