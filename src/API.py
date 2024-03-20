from flask import Flask, jsonify
import sqlite3
from datetime import datetime, timedelta
from db_utils import *

app = Flask(__name__)

DATABASE = 'finance_data.db'

def connect_db():
	return sqlite3.connect(DATABASE)

def get_all_tables():
	conn = connect_db()
	cursor = conn.cursor()
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables = cursor.fetchall()
	conn.close()
	return [table[0] for table in tables]

@app.route('/api/<symbol>/getMetrics', methods=['GET'])
def get_metrics_for_symbol(symbol):
	symbol = symbol.upper()
	conn = connect_db()
	metrics = []
	for table_name in get_all_tables():
		cursor = conn.cursor()

		try:
			cursor.execute(f"PRAGMA table_info({table_name})")
			columns = [column[1] for column in cursor.fetchall()]

			cursor.execute(f'SELECT * FROM {table_name} WHERE Symbol = ?', (symbol,))
			data = cursor.fetchall()
			if data:
				metrics.extend(data)
				break

		except sqlite3.Error as e:
			print(f"Erro ao consultar tabela {table_name}: {e}")
	conn.close()

	if metrics != [] and metrics is not None and 'timestamp' in metrics:
		current_date = datetime.datetime.now()
		data_timestamp = datetime.datetime.fromisoformat(metrics[0]['timestamp'])
		time_difference = current_date - data_timestamp
		if time_difference > datetime.timedelta(hours=24):
			print("Informações disponiveis são antigas, atualizando... \n")
			metrics = update_symbol(symbol)
			if metrics is None:
				return jsonify({"message": "Failed to update metrics."}), 500

	result_dict = {}

	if metrics == []:
		print("Informações não encontradas para o símbolo especificado. Realizando pesquisa... \n")
		result_dict = update_symbol(symbol)
	else:
		for i, column  in enumerate(columns):
			result_dict[column] = metrics[0][i]

	return jsonify(result_dict)

@app.route('/api/<table_name>/getAssetsMetrics', methods=['GET'])
def get_table(table_name):
	table_name = table_name.upper()
	conn = connect_db()
	cursor = conn.cursor()
	cursor.execute(f'SELECT * FROM {table_name}')
	data = cursor.fetchall()
	cursor.execute(f"PRAGMA table_info({table_name})")
	columns = [column[1] for column in cursor.fetchall()]

	conn.close()

	result_list = []
	result_dict = {}

	for i in range(len(data)):
		for j, column  in enumerate(columns):
			result_dict[column] = data[i][j]
		result_list.append(result_dict)
		result_dict.clear


	return jsonify(result_list)

@app.route('/api/<table_name>/getAssetsList', methods=['GET'])
def get_table_list(table_name):
	table_name = table_name.upper()
	conn = connect_db()
	cursor = conn.cursor()
	cursor.execute(f'SELECT Symbol FROM {table_name}')
	data = cursor.fetchall()
	conn.close()		
	return jsonify(data)

if __name__ == '__main__':
	app.run(debug=True)  # Desativar o modo de depuração
