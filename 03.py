import os
import json
import sqlite3


def read_json(filename: str) -> dict:
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            _dict = json.load(file)
        return _dict
    else:
        print(f'ERRO. o arquivo {filename} não foi encontrado.')
        exit(-1)


def gera_relatorio(arquivo):
    data = read_json(arquivo)
    apostas = data['apostas']

    # Converte as apostas múltiplas para um formato imutável para poder usar um set
    multiple_bet_bank = []

    for aposta in apostas:
        ParticipantContainer = aposta['ParticipantContainer']
        multiple_bet = []

        for p in ParticipantContainer:
            ParticipantSpan = p['ParticipantSpan']
            MarketDescription = p['MarketDescription']
            FixtureName = p['FixtureName']
            simple_bet = (ParticipantSpan, MarketDescription, FixtureName)
            simple_bet_str = '|'.join(simple_bet)
            multiple_bet.append(simple_bet_str)
            print(f'simple_bet = {simple_bet_str}')

        multiple_bet_str = ', '.join(sorted(multiple_bet))
        print(f'multiple_bet = {multiple_bet_str}')
        multiple_bet_bank.append(multiple_bet_str)

    multiple_bet_bank = sorted(multiple_bet_bank)
    print(multiple_bet_bank)

    multiple_bet_bank_set = set(multiple_bet_bank)
    print(multiple_bet_bank_set)
    pass

    # Usa um set para remover duplicatas e compara o tamanho do set com a lista original
    # if len(set(apostas_convertidas1)) != len(apostas):
    #     print("Há apostas múltiplas idênticas.")
    # else:
    #     print("Não há apostas múltiplas idênticas.")


def teste_01():
    gera_relatorio('apostas.json')
    pass


def create_database(file_json_in: str, file_sqlite):
    data = read_json(file_json_in)
    apostas = data['apostas']

    sqliteConnection = None
    try:
        # Connect to DB and create a cursor
        sqliteConnection = sqlite3.connect(file_sqlite)
        cursor = sqliteConnection.cursor()
        print('DB Init')

        # Write a query and execute it with cursor
        query = 'select sqlite_version();'
        cursor.execute(query)

        # Fetch and output result
        result = cursor.fetchall()
        print('SQLite Version is {}'.format(result))

        # Close the cursor
        cursor.close()

    # Handle errors
    except sqlite3.Error as error:
        print('Error occurred - ', error)

    # Close DB Connection irrespective of success
    # or failure
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')


def teste_02():
    create_database('apostas.json', 'database.db')


if __name__ == '__main__':
    teste_02()
