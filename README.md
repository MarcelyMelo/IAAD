Projeto de Gerenciamento de Filmes (IAAD)
Este projeto consiste em um sistema computacional para gerenciar a programação de filmes em canais de televisão. A aplicação web foi desenvolvida com o framework Streamlit (Python) e se conecta a um banco de dados MySQL para realizar as operações.

Adicionalmente, o repositório contém scripts para a modelagem e manipulação dos mesmos dados em um banco de dados NoSQL (Cassandra) como parte de um estudo comparativo.

1. Pré-requisitos
   Antes de começar, garanta que você tenha os seguintes softwares instalados em sua máquina:

Python (versão 3.8 ou superior)

MySQL Server (MySQL Community Server ou similar)

Um cliente MySQL para executar scripts (Ex: MySQL Workbench, DBeaver, ou o próprio terminal)

Git para clonar o repositório

2. Configuração do Banco de Dados (MySQL)
   O primeiro passo é configurar o banco de dados relacional que será utilizado pela aplicação Streamlit.

2.1. Criação da Base e Tabelas
Execute o script streamlit/database/criar_base.sql no seu cliente MySQL para criar o banco de dados FILMES e todas as tabelas necessárias (Canal, Filme, Elenco, Exibicao).

Exemplo (via terminal):

mysql -u seu_usuario -p < streamlit/database/criar_base.sql

2.2. Povoamento do Banco
Após a criação, execute o script streamlit/database/populate.sql para inserir os dados iniciais nas tabelas.

Exemplo (via terminal):

mysql -u seu_usuario -p FILMES < streamlit/database/populate.sql

3. Configuração da Aplicação (Streamlit)
   Com o banco de dados pronto, configure o ambiente Python para rodar a aplicação web.

3.1. Clone o Repositório
Abra um terminal, navegue até o diretório onde deseja salvar o projeto e clone este repositório:

git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA_DO_PROJETO>

3.2. Instale as Dependências
Navegue até a pasta streamlit e instale as bibliotecas Python necessárias.

# Instalar as bibliotecas

pip install streamlit sqlalchemy mysqlclient

3.3. Configure a Conexão
Para que a aplicação consiga se conectar ao seu banco de dados, é preciso informar sua senha do MySQL.

Navegue até a pasta .streamlit dentro da pasta streamlit.

Abra o arquivo secrets.toml.

Altere o valor da variável password para a senha que você utiliza no seu MySQL.

[connections.mysql]
dialect = "mysql"
host = "localhost"
port = 3306
database = "filmes"
username = "root"
password = "SUA_SENHA_AQUI" # Altere esta linha

4. Executando o Projeto
   Após seguir todos os passos, a aplicação está pronta para ser executada. Certifique-se de que você está na pasta streamlit e execute o seguinte comando no seu terminal:

streamlit run Inicio.py

Isso iniciará o projeto e uma nova aba será aberta no seu navegador com a aplicação web em execução. ✨

5. Componente NoSQL (Cassandra)
   Esta seção é dedicada à parte que envolve o uso do Cassandra.

5.1. Configuração
É necessário ter uma instância do Cassandra rodando. Você pode instalá-lo localmente ou usar um container Docker.

5.2. Criação do Keyspace e Tabelas
Execute o script cassandra/create_filmes.cql no cqlsh (o shell de linha de comando do Cassandra) para criar o keyspace filmes e as tabelas modeladas para consulta.

5.3. Povoamento dos Dados
Para popular as tabelas, execute o conteúdo do script cassandra/populate.cql no cqlsh.

5.4. Consultas de Exemplo
O arquivo cassandra/read_update_delete.cql contém exemplos de consultas de leitura, atualização e remoção que podem ser executadas para testar e demonstrar as operações CRUD no Cassandra.
