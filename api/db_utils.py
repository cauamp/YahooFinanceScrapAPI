import re
from scrap_utils  import *
import os
import psycopg2


def adjust_metrics_keys (metrics):
	if metrics is not None:
		new_data_dict = {}
		for key, value in metrics.items():
			
			new_key = key.split('(')[0].strip()
			if new_key != "Symbol":
				new_key = new_key.lower()
			
			new_key = new_key.replace('%', 'percent')
			new_key = re.sub(r'\W+', '_', new_key)
			
			if not new_key[0].isdigit():
				new_data_dict[new_key] = value
				if value == "INDEX":
					new_data_dict[new_key] = "CURRENCY"

		metrics.clear() 
		metrics.update(new_data_dict)

def create_table(cursor, table_name, columns):
	
	cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
	table_exists = cursor.fetchone()[0]

	if not table_exists:
		cursor.execute(f"CREATE TABLE {table_name} (Symbol TEXT PRIMARY KEY, {', '.join(columns)})")
	
	cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table_name,))
	existing_columns = [column[0] for column in cursor.fetchall()]

	for column in columns:
		if column not in existing_columns:
			cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column} REAL")
			

def insert_data(cursor, table_name, data):
	cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table_name,))
	table_columns = [column[0] for column in cursor.fetchall()]

	for key in data.keys():
		if key not in table_columns and key != 'type' and key != 'Symbol':
			raise ValueError(f"A coluna '{key}' não existe na tabela '{table_name}'")

	columns = ', '.join([col for col in data.keys() if col != 'type'])
	
	values = tuple(data[key] for key in data.keys() if key != 'type')

	placeholders = ', '.join(['%s' for _ in range(len(values))])

	cursor.execute(f"DELETE FROM {table_name} WHERE Symbol = ?", (data['Symbol'],))

	cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)

def update_symbol(symbol):
	try:
		metrics = get_stock_metrics(symbol.upper())
		
		if metrics is None:
			return None
		
		adjust_metrics_keys(metrics)
		
		conn = psycopg2.connect(os.getenv("DATABASE_URL"))

		cursor = conn.cursor()
		
		table_name = metrics['type']
		create_table(cursor, table_name, [key for key in metrics.keys() if key != 'type' and key != 'Symbol'])
		
		insert_data(cursor, table_name, metrics)
		
		# Commit e fechar conexão
		conn.commit()
		conn.close()
		
		return metrics
	
	except Exception as e:
		print(f"Erro ao atualizar o símbolo '{symbol}': {e}")
		return None