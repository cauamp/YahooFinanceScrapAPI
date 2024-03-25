import requests
from bs4 import BeautifulSoup
import re
import datetime


def check_symbol_existence(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1d"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        exist = 'No data found, symbol may be delisted' not in response.text

        if not exist:
            raise Exception(
                f"No data found for symbol '{symbol}', it may be delisted.")

        metrics = {}
        metrics['Symbol'] = re.findall(r'"symbol":"(.*?)"', response.text)[0]
        metrics['type'] = re.findall(
            r'"instrumentType":"(.*?)"', response.text)[0].lower()
        return metrics

    except requests.exceptions.RequestException as e:
        print(
            f"Erro na request de teste. O ativo '{symbol}' não existe ou não foi encontrada.\n\n")
        raise BaseException(
            f"Erro na request de teste. O ativo '{symbol}' nao existe ou nao foi encontrado. ")


def get_stock_metrics(symbol):
    symbol = symbol.upper()
    url = f"https://finance.yahoo.com/quote/{symbol}/key-statistics"
    headers = {"User-Agent": "https://query1.finance.yahoo.com/v8/finance/chart/NVDA?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"}

    try:
        print(f'Checando a existencia de {symbol}...')

        metrics = check_symbol_existence(symbol)

        print('Encontrado! \nAguarde ...')
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')

        metrics['qsp-price'] = soup.find('fin-streamer',
                                         attrs={'data-test': 'qsp-price'})['value']

        table_rows = soup.find_all('tr')

        for row in table_rows:
            cells = row.find_all('td')

            if len(cells) == 2:
                metric = cells[0].text.strip()
                value = cells[1].text.strip()
                metrics[metric] = value

        metrics['timestamp'] = datetime.datetime.now().isoformat()
        print('\n')
        print('Metricas Obtidas!')
        return metrics

    except BaseException as e:
        raise BaseException(f"{e}")

    except ...:
        print(f"Erro em get_stock_metrics: {e}")
        raise Exception(f"Erro em get_stock_metrics: {e}")
