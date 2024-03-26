# Documentação da API Yahoo Finance Scrap

Esta API permite acessar métricas financeiras e informações sobre ativos da Yahoo Finance.

## Requisições Permitidas

### Recuperar Métricas para um Símbolo Específico

Recupera métricas financeiras para um símbolo específico.

- **URL**: `/api/<symbol>/getMetrics`
- **Método HTTP**: GET
- **Parâmetros de URL**:
  - `symbol` (obrigatório): O símbolo do ativo financeiro.
- **Resposta de Sucesso**:
  - Status: 200 OK
  - Corpo: JSON contendo as métricas financeiras do ativo.

### Recuperar Métricas de Ativos de uma Tabela Específica

Recupera métricas financeiras de ativos de uma tabela específica.

- **URL**: `/api/<table_name>/getAssetsMetrics`
- **Método HTTP**: GET
- **Parâmetros de URL**:
  - `table_name` (obrigatório): O nome da tabela (ETF, EQUITY, etc) que contém os ativos.
- **Resposta de Sucesso**:
  - Status: 200 OK
  - Corpo: JSON contendo as métricas financeiras dos ativos da tabela.

### Recuperar Lista de Ativos de uma Tabela Específica

Recupera uma lista de ativos de uma tabela específica.

- **URL**: `/api/<table_name>/getAssetsList`
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
response = requests.get('https://yahoo-finance-scrap-api.vercel.app/api/AAPL/getMetrics')
print(response.json())

# Recuperar métricas de ativos de uma tabela específica
response = requests.get('https://yahoo-finance-scrap-api.vercel.app/api/ETF/getAssetsMetrics')
print(response.json())

# Recuperar lista de ativos de uma tabela específica
response = requests.get('https://yahoo-finance-scrap-api.vercel.app/api/EQUITY/getAssetsList')
print(response.json())
