import psycopg2
from .db_utils import *
from datetime import datetime, timedelta
from flask import Flask, jsonify
from .config import *
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


@app.route('/api/<symbol>/getMetrics', methods=['GET'])
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
            return jsonify({"message": f"{e}"}), 500
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
        for j, column in enumerate(columns):
            result_dict[column] = data[i][j]
        result_list.append(result_dict)
        result_dict.clear

    if result_list == []:
        return jsonify({"message": "Failed to get metrics."}), 500

    return jsonify(result_list)


@app.route('/api/<table_name>/getAssetsList', methods=['GET'])
def get_table_list(table_name):
    table_name = table_name.upper()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f'SELECT Symbol FROM {table_name}')
    data = cursor.fetchall()
    conn.close()
    if data is None:
        return jsonify({"message": "Failed to get assets list."}), 500

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)  # Desativar o modo de depuração
