# Projeto

## Objetivo
O objetivo deste projeto foi realizar um web scraping do Yahoo Finance para coletar informações financeiras e criar um banco de dados sob demanda. Além disso, foi criado uma API, atualmente hospedada na Vercel usando um banco de dados na Neon Console para hospedagem, que possibilita a consulta dos dados armazenados no banco de dados, além da atualização desses. Esta iniciativa visa praticar diversas habilidades úteis, como:

- Criação e gerenciamento de banco de dados
- Manipulação de dados
- Web scraping
- Desenvolvimento de API

## Funcionalidades

O projeto possui as seguintes funcionalidades:

1. **Coleta de Dados Financeiros:** Realiza a coleta de dados financeiros do Yahoo Finance por meio de web scraping.
2. **Armazenamento em Banco de Dados:** Armazena as informações coletadas em um banco de dados.
3. **Consulta de Informações:** Permite a consulta das informações armazenadas no banco de dados.
4. **Disponibiliza  API:** Disponibiliza uma API que fornece acesso aos dados coletados de forma programática.

Para entender parte do processo, consulte o [registro de desenvolvimento](Project.ipynb).
Para mais detalhes da utilização, consulte a [documentação completa](DOCUMENTACAO.md).

## Metodologia
O desenvolvimento do projeto seguiu as seguintes etapas:

1. **Análise de Requisitos:** Identificação dos requisitos do projeto e definição de funcionalidades.
2. **Implementação do Web Scraping:** Desenvolvimento do código para extrair dados do Yahoo Finance.
3. **Criação do Banco de Dados:** Configuração de um banco de dados para armazenar os dados coletados e integração com a extração via Web Scrapping.
4. **Desenvolvimento da API:** Implementação de uma API para acesso aos dados armazenados.
5. **Implantação:** Hospedagem da API e do banco de dados para disponibilizá-la publicamente.

## Tecnologias Utilizadas

As principais tecnologias e ferramentas utilizadas no projeto incluem:

- **Python:** Linguagem de programação utilizada para desenvolver o código do projeto.
- **Beautiful Soup:** Biblioteca em Python utilizada para fazer o web scraping dos dados do Yahoo Finance.
- **Regex:** Expressões regulares são utilizadas para manipular e extrair informações específicas dos dados coletados.
- **SQLite:** Banco de dados embutido utilizado para armazenar as informações coletadas durante o processo de web scraping.
- **Flask:** Framework web em Python utilizado para criar a API que disponibiliza os dados coletados.
- **PostgreSQL:** Sistema de gerenciamento de banco de dados relacional utilizado para armazenar e gerenciar os dados de forma mais robusta em ambientes de produção.


## Adendo
### Cunho Educacional

É importante salientar que este projeto tem cunho exclusivamente educacional e não visa violar ou prejudicar a plataforma Yahoo Finance de nenhuma maneira.

O objetivo principal é aprender e praticar habilidades técnicas relacionadas ao web scraping, manipulação de dados, criação e gerenciamento de banco de dados, e desenvolvimento de API.

