import re
from .scrap_utils import *

column_data_types = {
    "date": "DATE",
    "most_recent_quarter": "DATE",
    "fiscal_year_ends": "DATE",
    "timestamp": "TIMESTAMP",
    "ask": "TEXT",
    "bid": "TEXT",
    "day_s_range": "TEXT"
}


def convert_to_float(value_str):
    if 'N/A' in value_str.upper():
        return None
    if ':' in value_str:
        numerator, denominator = map(float, value_str.split(':'))
        if denominator == 0:
            return None  # Evita divisão por zero
        return numerator / denominator
    if re.search(r'^[\d.]+$', value_str[:-1]):
        if value_str.endswith('T'):
            return float(value_str[:-1]) * 10**12
        elif value_str.endswith('B'):
            return float(value_str[:-1]) * 10**9
        elif value_str.endswith('M'):
            return float(value_str[:-1]) * 10**6
        elif value_str.endswith('K'):
            return float(value_str[:-1]) * 10**3
        else:
            return float(value_str)
    else:
        return value_str


def adjust_metrics_keys(metrics):
    if metrics is not None:
        new_data_dict = {}
        for key, value in metrics.items():

            new_key = key.split('(')[0].strip()
            if new_key != "Symbol":
                new_key = new_key.lower()

            new_key = new_key.replace('%', 'percent')
            new_key = re.sub(r'\W+', '_', new_key)

            if not new_key[0].isdigit():

                if (new_key in ['Symbol', 'timestamp', 'type']):
                    new_data_dict[new_key] = value
                else:
                    new_data_dict[new_key] = convert_to_float(
                        value.replace('%', '').replace(',', ''))

            if value == "index":
                new_data_dict[new_key] = "currency"

        metrics.clear()
        metrics.update(new_data_dict)


def create_table(cursor, table_name, columns):

    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
    tables = [table[0] for table in cursor.fetchall()]

    table_exists = table_name.lower() in tables

    if not table_exists:
        column_declarations = []
        for column in columns:
            for pattern, data_type in column_data_types.items():
                if pattern in column.lower():
                    column_declarations.append(f"{column} {data_type}")
                    break
            else:
                column_declarations.append(f"{column} FLOAT")

        table_declaration = f"Symbol TEXT PRIMARY KEY, {', '.join(column_declarations)}"
        print('\n\n\n\n\n',
              f"CREATE TABLE IF NOT EXISTS {table_name} ({table_declaration})", '\n\\n\n')
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({table_declaration})")

    cursor.execute(
        f"SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table_name,))
    existing_columns = [column[0] for column in cursor.fetchall()]

    for column in columns:
        if column not in existing_columns:
            print("nao existia: ", column)
            cursor.execute(
                f"ALTER TABLE {table_name} ADD COLUMN {column} REAL")


def insert_data(cursor, table_name, data):
    cursor.execute(
        f"SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table_name,))
    table_columns = [column[0] for column in cursor.fetchall()]

    for key in data.keys():
        if key not in table_columns and key != 'type' and key != 'Symbol':
            raise ValueError(
                f"A coluna '{key}' não existe na tabela '{table_name}'")

    columns = ', '.join([col for col in data.keys() if col != 'type'])

    values = tuple(data[key] for key in data.keys() if key != 'type')

    placeholders = ', '.join(['%s' for _ in range(len(values))])

    cursor.execute(
        f"DELETE FROM {table_name} WHERE Symbol = %s", (data['Symbol'],))

    cursor.execute(
        f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)


def update_symbol(symbol, cursor):
    try:
        metrics = get_stock_metrics(symbol.upper())

        if metrics is None:
            raise (f"Erro ao obter dados  do simbolo '{symbol}': {e}")

        adjust_metrics_keys(metrics)

        table_name = metrics['type']
        create_table(cursor, table_name, [
            key for key in metrics.keys() if key != 'type' and key != 'Symbol'])

        insert_data(cursor, table_name, metrics)

        return metrics

    except BaseException as e:
        raise BaseException(f"Erro ao atualizar o simbolo '{symbol}': {e}")

    except ... as e:
        print(f"Erro ao atualizar o símbolo '{symbol}': {e}")
        raise Exception(f"Erro ao atualizar o simbolo '{symbol}': {e}")
