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
			print(f"A ação '{symbol}' não existe ou não foi encontrada.")
			return False
		
		metrics = {}
		metrics['Symbol'] = re.findall(r'"symbol":"(.*?)"', response.text)[0]
		metrics['type'] = re.findall(r'"instrumentType":"(.*?)"', response.text)[0].lower()
		return metrics

	except requests.exceptions.RequestException as e:
		print(f"Erro na request de teste, A ação '{symbol}' não existe ou não foi encontrada.")
		return False


def get_stock_metrics(symbol):
	symbol = symbol.upper()
	url = f"https://finance.yahoo.com/quote/{symbol}/key-statistics"
	headers = {"User-Agent": "https://query1.finance.yahoo.com/v8/finance/chart/NVDA?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"}

	try:
		print(f'Checando a existencia de {symbol}...')
		
		metrics = check_symbol_existence(symbol)
		if metrics is False:  
			return None         
		print('Encontrado! \nAguarde ...')
		response = requests.get(url, headers=headers)

		soup = BeautifulSoup(response.text, 'html.parser')
		
		metrics['qsp-price'] = soup.find('fin-streamer', attrs={'data-test': 'qsp-price'})['value']
		
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
	
	except requests.exceptions.HTTPError as e:
		print("Erro na request:", e)
		print("A ação foi encontrada porém, não foi possível obter as estatisticas da ação.")
		return None