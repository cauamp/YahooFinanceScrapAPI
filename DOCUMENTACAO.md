# Documentação da API Yahoo Finance Scrap

Esta API permite acessar métricas financeiras e informações sobre ativos da Yahoo Finance.

## Requisições Permitidas

### Recuperar Métricas para um Símbolo Específico

Recupera métricas financeiras para um símbolo específico.

- **URL**: `/api/<symbol>/metrics`
- **Método HTTP**: GET
- **Parâmetros de URL**:
  - `symbol` (obrigatório): O símbolo do ativo financeiro.
- **Resposta de Sucesso**:
  - Status: 200 OK
  - Corpo: JSON contendo as métricas financeiras do ativo.

### Atualizar Métricas para um Símbolo Específico

Atualiza as métricas financeiras para um símbolo específico.

- **URL**: `/api/<symbol>/update`
- **Método HTTP**: PUT
- **Parâmetros de URL**:
  - `symbol` (obrigatório): O símbolo do ativo financeiro.
- **Corpo da Solicitação**:
  - JSON contendo os dados de atualização das métricas.
- **Resposta de Sucesso**:
  - Status: 200 OK
  - Corpo: JSON contendo as métricas financeiras atualizadas.

### Recuperar Métricas Específicas para um Símbolo

Recupera métricas financeiras específicas para um símbolo, filtradas por colunas específicas.

- **URL**: `/api/<symbol>/filteredMetrics`
- **Método HTTP**: GET
- **Parâmetros de URL**:
  - `symbol` (obrigatório): O símbolo do ativo financeiro.
- **Parâmetros de Consulta**:
  - `metrics` (obrigatório): Uma lista com os nomes das colunas desejadas.
- **Resposta de Sucesso**:
  - Status: 200 OK
  - Corpo: JSON contendo as métricas financeiras filtradas pelo símbolo e pelas colunas especificadas.

### Recuperar Métricas de Ativos de uma Tabela Específica

Recupera métricas financeiras de ativos de uma tabela específica.

- **URL**: `/api/<table_name>/metrics`
- **Método HTTP**: GET
- **Parâmetros de URL**:
  - `table_name` (obrigatório): O nome da tabela (ETF, EQUITY, etc) que contém os ativos.
- **Resposta de Sucesso**:
  - Status: 200 OK
  - Corpo: JSON contendo as métricas financeiras dos ativos da tabela.

### Recuperar Lista de Ativos de uma Tabela Específica

Recupera uma lista de ativos de uma tabela específica.

- **URL**: `/api/<table_name>/list`
- **Método HTTP**: GET
- **Parâmetros de URL**:
  - `table_name` (obrigatório): O nome da tabela (ETF, EQUITY, etc) que contém os ativos.
- **Resposta de Sucesso**:
  - Status: 200 OK
  - Corpo: JSON contendo a lista de ativos da tabela.

## Exemplos de Uso

### Python

```python
import requests

# Recuperar métricas para um símbolo específico
response = requests.get('https://yahoo-finance-scrap-api.vercel.app/api/AAPL/metrics')
print(response.json())

# Atualizar métricas para um símbolo específico
response = requests.put('https://yahoo-finance-scrap-api.vercel.app/api/AAPL/update')
print(response.json())

# Recuperar métricas específicas para um símbolo
response = requests.get('https://yahoo-finance-scrap-api.vercel.app/api/AAPL/filteredMetrics?metrics=symbol&metrics=qsp_price')
print(response.json())

# Recuperar métricas de ativos de uma tabela específica
response = requests.get('https://yahoo-finance-scrap-api.vercel.app/api/ETF/metrics')
print(response.json())

# Recuperar lista de ativos de uma tabela específica
response = requests.get('https://yahoo-finance-scrap-api.vercel.app/api/EQUITY/list')
print(response.json())
