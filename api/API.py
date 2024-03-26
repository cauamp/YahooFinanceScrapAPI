from .config import *
import psycopg2
import datetime
from flask import Flask, jsonify, request
from .db_utils import *
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
DATABASE = os.getenv("DATABASE_URL")


def connect_db():
	try:
		conn = psycopg2.connect(DATABASE)
		print("Conexão bem sucedida ao banco de dados PostgreSQL!")
		return conn
	except psycopg2.Error as e:
		print("Erro ao conectar ao banco de dados PostgreSQL:", e)
		return None


def get_all_tables(cursor):
	cursor.execute(
		"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
	tables = cursor.fetchall()
	return [table[0] for table in tables]


@app.route('/api/<symbol>/metrics', methods=['GET'])
def get_metrics_for_symbol(symbol):
	symbol = symbol.upper()
	conn = connect_db()
	cursor = conn.cursor()
	metrics = []
	for table_name in get_all_tables(cursor):
		try:
			cursor.execute(
				f'SELECT * FROM {table_name} WHERE Symbol = %s', (symbol,))
			data = cursor.fetchall()
			if data:
				metrics.extend(data)
				columns = [column[0] for column in cursor.description]
				break

		except psycopg2.Error as e:
			print(f"Erro ao consultar tabela {table_name}: {e}")
			return jsonify({"message": f"Erro ao consultar tabela {table_name}: {e}"})

	result_dict = {}

	if metrics == []:
		print("Informações não encontradas para o símbolo especificado. Realizando pesquisa... \n")
		try:
			result_dict = update_symbol(symbol, cursor)
		except BaseException as e:
			return jsonify({"message": f"{e}"}), 404
		except ... as e:
			return jsonify({"message": f"Something went wrong when updating metrics. Exception: {e}"}), 500

	else:
		for i, column in enumerate(columns):
			result_dict[column] = metrics[0][i]

		if metrics != {}:
			current_date = datetime.datetime.now()
			data_timestamp = datetime.datetime.fromisoformat(
				str(result_dict['timestamp']))

			time_difference = current_date - data_timestamp
			if time_difference > datetime.timedelta(hours=24):
				print("Informações disponiveis são antigas, atualizando... \n")
				try:
					result_dict = update_symbol(symbol, cursor)
					if result_dict is None:
						return jsonify({"message": "Failed to update metrics."}), 500
				except ... as e:
					return jsonify({"message": f"Something went wrong when updating metrics. Exception: {e}"}), 500

	conn.commit()
	conn.close()

	return jsonify(result_dict), 200


@app.route('/api/<symbol>/update', methods=['PUT'])
def update_metrics_for_symbol(symbol):
	symbol = symbol.upper()
	conn = connect_db()
	cursor = conn.cursor()
	result_dict = {}
	try:
		result_dict = update_symbol(symbol, cursor)
	except BaseException as e:
		return jsonify({"message": f"Failed to update metrics. {e}"}), 404
	except ... as e:
		return jsonify({"message": f"Something went wrong when updating metrics. Exception: {e}"}), 500

	conn.commit()
	conn.close()
	return jsonify(result_dict), 200


@app.route('/api/<symbol>/filteredMetrics', methods=['GET'])
def get_specific_metrics_for_symbol(symbol):
	symbol = symbol.upper()
	conn = connect_db()
	cursor = conn.cursor()

	try:
		table_name = ''
		requested_columns = request.args.getlist('metrics')
		if not requested_columns:
			conn.close()
			return jsonify({"message": "Por favor, forneça o nome da(s) coluna(s) desejada(s) na consulta."}), 400

		for table in get_all_tables(cursor):
			cursor.execute(
				f"SELECT COUNT(*) FROM {table} WHERE symbol = %s", (symbol,))
			count = cursor.fetchone()[0]
			if count > 0:
				table_name = str(table)
				break

		columns_str = ', '.join(requested_columns)
		query = f"SELECT {columns_str} FROM {table_name} WHERE symbol = %s"

		cursor.execute(query, (symbol,))
		metrics = cursor.fetchall()

		if metrics:
			columns = [column[0] for column in cursor.description]

			result_dict = {}
			for i, column in enumerate(columns):
				result_dict[column] = metrics[0][i]

			conn.close()
			return jsonify(result_dict), 200
		else:
			conn.close()
			return jsonify({"message": f"Métricas para o símbolo {symbol} não encontradas."}), 404
		
	except psycopg2.Error as e:
		conn.close()
		print(f"Erro ao consultar métricas para o símbolo {symbol}: {e}")
		return jsonify({"message": f"Erro ao consultar métricas para o símbolo {symbol}: {str(e).replace(chr(10), '')}"}), 500


@app.route('/api/<table_name>/allSymbols', methods=['GET'])
def get_table(table_name):
	table_name = table_name.upper()
	conn = connect_db()
	cursor = conn.cursor()
	cursor.execute(f'SELECT * FROM {table_name}')
	data = cursor.fetchall()
	columns = [column[0] for column in cursor.description]

	conn.close()

	result_list = []
	result_dict = {}

	for i in range(len(data)):
		for j, column in enumerate(columns):
			result_dict[column] = data[i][j]
		result_list.append(result_dict)
		result_dict.clear

	if result_list == []:
		return jsonify({"message": "Failed to get metrics."}), 404

	return jsonify(result_list), 200


@app.route('/api/<table_name>/list', methods=['GET'])
def get_table_list(table_name):
	table_name = table_name.upper()
	conn = connect_db()
	cursor = conn.cursor()
	cursor.execute(f'SELECT Symbol FROM {table_name}')
	data = cursor.fetchall()
	conn.close()
	if data is None:
		return jsonify({"message": "Failed to get assets list."}), 404
	
	result_list = []
	for list in data:
		result_list.append(list[0])
		
	return jsonify(result_list), 200


if __name__ == '__main__':
	app.run(debug=True)  # Desativar o modo de depuração
