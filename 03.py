# supõe-se que todas as apostas são múltiplas

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


def write_json(filename: str, _dict: dict):
    with open(filename, 'w') as file:
        json.dump(_dict, file, indent=4, ensure_ascii=False)


def gera_relatorio(arquivo):
    data = read_json(arquivo)
    apostas = data['apostas']

    # Converte as apostas múltiplas para um formato imutável para poder usar um set
    multiple_bet_list = []

    for aposta in apostas:
        StakeDesc = aposta['StakeDesc']
        HeaderText = aposta['HeaderText']
        BetInformationText = aposta['BetInformationText']

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
        multiple_bet_list.append(multiple_bet_str)

    multiple_bet_list = sorted(multiple_bet_list)
    print(multiple_bet_list)

    multiple_bet_set = set(multiple_bet_list)
    print(multiple_bet_set)
    pass

    # Usa um set para remover duplicatas e compara o tamanho do set com a lista original
    if len(multiple_bet_set) != len(apostas):
        print("Há apostas múltiplas idênticas.")
    else:
        print("Não há apostas múltiplas idênticas.")


def teste_01():
    gera_relatorio('apostas.json')
    pass


def create_database(file_json_in: str, file_sqlite: str):
    data = read_json(file_json_in)
    apostas = data['apostas']

    # se já existe um arquivo de banco de dados, delete-o.
    if os.path.exists(file_sqlite):
        os.remove(file_sqlite)

    connection = None
    try:
        # Connect to DB and create a cursor
        connection = sqlite3.connect(file_sqlite)
        cursor = connection.cursor()
        print('DB Init')

        # Write a query and execute it with cursor
        query = 'select sqlite_version();'
        cursor.execute(query)

        # Fetch and output result
        result = cursor.fetchall()
        print(f'SQLite Version is {result}')

        with open('create_tables.sql') as file:
            cursor.executescript(file.read())

        simple_bet_id_counter = 1

        # percorre todas as apostas e adiciona-as no banco.
        for i, multiple_bet in enumerate(apostas):
            StakeDesc = multiple_bet['StakeDesc']
            HeaderText = multiple_bet['HeaderText']
            BetInformationText = multiple_bet['BetInformationText']
            multiple_id = i + 1
            MultipleBetData = (multiple_id, StakeDesc, HeaderText, BetInformationText)

            # inserir uma nova aposta múltipla na MultipleBet
            query = "INSERT INTO MultipleBet VALUES(?, ?, ?, ?)"
            print(MultipleBetData)
            cursor.execute(query, MultipleBetData)

            ParticipantContainer = multiple_bet['ParticipantContainer']

            for simple_bet in ParticipantContainer:
                ParticipantSpan = simple_bet['ParticipantSpan']
                MarketDescription = simple_bet['MarketDescription']
                FixtureName = simple_bet['FixtureName']
                SimpleBetData = (simple_bet_id_counter, ParticipantSpan, MarketDescription, FixtureName, multiple_id)
                simple_bet_id_counter += 1

                # inserir uma nova aposta múltipla na MultipleBet
                query = "INSERT INTO SimpleBet VALUES(?, ?, ?, ?, ?)"
                print(f'    {SimpleBetData}')
                cursor.execute(query, SimpleBetData)

        connection.commit()
        # Close the cursor
        cursor.close()

    # Handle errors
    except sqlite3.Error as error:
        print('Error occurred - ', error)

    # Close DB Connection irrespective of success
    # or failure
    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')


def teste_02():
    create_database('apostas.json', 'database.db')


def query_db_01(file_sqlite: str):
    """
    Faz uma consulta específica no BD.
    Solicita quais são as apostas múltiples que contém a seguinte linha (ou aposta simples)
    ('Arsenal', 'Vencedor Final', 'Inglaterra - Premier League 2023/24')
    O resultado é gravado no arquivo results.json
    :param file_sqlite:
    :return:
    """
    connection = None
    try:
        # Connect to DB and create a cursor
        connection = sqlite3.connect(file_sqlite)
        cursor = connection.cursor()
        print('DB Init')

        # consulta a versão do BD.
        query = 'select sqlite_version();'
        cursor.execute(query)

        # Fetch and output result
        result = cursor.fetchall()
        print(f'SQLite Version is {result}')

        # executa a consulta ao banco de dados
        query = '''
        SELECT SimpleBet.MultipleBetID FROM SimpleBet WHERE 
            ParticipantSpan = ? AND 
            MarketDescription = ? AND
            FixtureName = ?
        '''
        params = ('Arsenal', 'Vencedor Final', 'Inglaterra - Premier League 2023/24')
        cursor.execute(query, params)

        result = cursor.fetchall()

        results = {}
        for r in result:
            MultipleBetID = r[0]
            print(MultipleBetID)
            query2 = 'SELECT * from SimpleBet WHERE MultipleBetID = ?'
            cursor.execute(query2, r)
            result2 = cursor.fetchall()

            results[str(MultipleBetID)] = []
            result2_ = []
            for row in result2:
                row_str = f'{row[1]}, {row[2]}, {row[3]}'
                result2_.append(row_str)

            results[str(MultipleBetID)].append(sorted(result2_))

        write_json('results.json', results)

        # Close the cursor
        cursor.close()

    # Handle errors
    except sqlite3.Error as error:
        print('Error occurred - ', error)

    # Close DB Connection irrespective of success
    # or failure
    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')


if __name__ == '__main__':
    # teste_02()
    query_db_01('database.db')
