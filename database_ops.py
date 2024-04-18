# supõe-se que todas as apostas são múltiplas

import os
import sqlite3
from utils import read_json, write_json


def create_database(main_dir: str, filename_bets_json: str, filename_database: str, filename_terms_json: str) -> bool:
    """
    Cria um arquivo de banco de dados sqlite (bets.db) a partir de um arquivo json (apostas.json).
    Também cria um arquivo (termos.json) que contém as listas de termos que aparecem nas apostas e que serão
    usadas na interface gráfica para formar os elementos da pesquisa.
    :param main_dir: o diretório onde fica main.py
    :param filename_bets_json:
    :param filename_database:
    :param filename_terms_json:
    :return: Retorna True em caso de sucesso, False em caso de falha ao criar o banco de dados ou o arquivo dos termos.
    """
    temp_dir = os.path.join(main_dir, 'temp')

    if not os.path.exists(temp_dir):
        print('ERRO. O diretório temp não foi encontrado.')
        return False

    filepath_bets_json = os.path.join(temp_dir, filename_bets_json)
    filepath_database = os.path.join(temp_dir, filename_database)
    filepath_terms_json = os.path.join(temp_dir, filename_terms_json)

    data = read_json(filepath_bets_json)
    multiple_bets = data['bets']

    # estes conjuntos servirão para saber quantos termos diferentes são usados como ParticipantSpan, MarketDescription
    # e FixtureName.
    ParticipantSpanSet = set()
    MarketDescriptionSet = set()
    FixtureNameSet = set()

    # se já existe um arquivo de banco de dados, delete-o.
    if os.path.exists(filepath_database):
        os.remove(filepath_database)

    connection = None
    try:
        connection = sqlite3.connect(filepath_database)
        cursor = connection.cursor()

        # with open('create_tables.sql') as file:
        #     cursor.executescript(file.read())
        query = '''
        CREATE TABLE SimpleBet (
            ID INT NOT NULL UNIQUE,
            ParticipantSpan VARCHAR,
            MarketDescription VARCHAR,
            FixtureName VARCHAR,
            MultipleBetID INT NOT NULL,
            FOREIGN KEY (MultipleBetID) REFERENCES MultipleBet(ID)
            PRIMARY KEY (ID)
        );
        '''
        cursor.execute(query)

        query = '''
                CREATE TABLE MultipleBet (
                ID INT NOT NULL UNIQUE,
                StakeDesc VARCHAR,
                HeaderText VARCHAR,
                BetInformationText VARCHAR,
                PRIMARY KEY (ID)
            );
        '''
        cursor.execute(query)

        simple_bet_id_counter = 1

        # percorre todas as apostas e adiciona-as no banco.
        for i, multiple_bet in enumerate(multiple_bets):
            StakeDesc = multiple_bet['StakeDesc']
            HeaderText = multiple_bet['HeaderText']
            BetInformationText = multiple_bet['BetInformationText']
            multiple_id = i + 1
            MultipleBetData = (multiple_id, StakeDesc, HeaderText, BetInformationText)

            # inserir uma nova aposta múltipla na MultipleBet
            query = "INSERT INTO MultipleBet VALUES(?, ?, ?, ?)"
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
                cursor.execute(query, SimpleBetData)

                ParticipantSpanSet.add(ParticipantSpan)
                MarketDescriptionSet.add(MarketDescription)
                FixtureNameSet.add(FixtureName)

        connection.commit()  # Save changes
        cursor.close()

    except sqlite3.Error as error:
        print('sqlite3. Error occurred : ', error)
        return False

    finally:
        if connection:
            connection.close()

    # salva os conjuntos em forma de listas ordenadas
    _dict = {
        'ParticipantSpanList': sorted(list(ParticipantSpanSet)),
        'MarketDescriptionList': sorted(list(MarketDescriptionSet)),
        'FixtureNameList': sorted(list(FixtureNameSet))
    }

    write_json(filepath_terms_json, _dict)

    return True


def tuple_parameters_ok(_tuple: tuple):
    for elem in _tuple:
        if not isinstance(elem, str) or elem == '':
            return False
    return True


def query_db_01(main_dir: str, filename_database: str, parameters: dict) -> dict | None:
    """
    Faz uma consulta específica no BD.
    Solicita quais são as apostas múltiplas que contém a seguinte linha (ou aposta simples)
    ('ParticipantSpan') ou ('ParticipantSpan', 'MarketDescription') ou
    ('ParticipantSpan', 'MarketDescription', 'FixtureName')
    O resultado é retornado e também é gravado no arquivo results.json
    :param main_dir:
    :param filename_database:
    :param parameters: uma tupla no formato ('ParticipantSpan', 'MarketDescription', 'FixtureName')
    :return: Retorna um dict com os resultados da busca em caso de sucesso ou None em caso de falha. Também guarda um
            arquivo results.json contendo o resultado da busca.
    """
    temp_dir = os.path.join(main_dir, 'temp')

    if not os.path.exists(temp_dir):
        print('ERRO. O diretório temp não foi encontrado.')
        return None

    filepath_database = os.path.join(temp_dir, filename_database)
    filepath_results_json = os.path.join(temp_dir, 'results.json')

    connection = None
    try:
        connection = sqlite3.connect(filepath_database)
        cursor = connection.cursor()

        _len_parameters = len(parameters.items())
        if _len_parameters == 0 or _len_parameters > 3:
            return None

        # prepara a string de consulta ao banco de dados
        _params = []
        where = 'WHERE '
        _list = []
        for k, v in parameters.items():
            if v:
                _list.append(f'{k} = ?')
                _params.append(v)

        where += ' AND '.join(_list)
        query = 'SELECT SimpleBet.MultipleBetID FROM SimpleBet ' + where

        cursor.execute(query, _params)
        query_result = cursor.fetchall()

        results = {}
        for r in query_result:
            MultipleBetID = r[0]
            results[str(MultipleBetID)] = {'info': tuple(), 'rows': []}

            query2 = 'SELECT * FROM MultipleBet WHERE ID = ?'
            cursor.execute(query2, r)
            result2 = cursor.fetchone()
            results[str(MultipleBetID)]['info'] = (result2[1], result2[2], result2[3])

            query3 = 'SELECT * from SimpleBet WHERE MultipleBetID = ?'
            cursor.execute(query3, r)
            result3 = cursor.fetchall()

            result3_ = []
            for row in result3:
                # row_str = f'{row[1]}, {row[2]}, {row[3]}'
                _row = (row[1], row[2], row[3])
                result3_.append(_row)

            results[str(MultipleBetID)]['rows'] = sorted(result3_)

        write_json(filepath_results_json, results)
        cursor.close()

        return results

    except sqlite3.Error as error:
        print('Error occurred - ', error)

    finally:
        if connection:
            connection.close()


if __name__ == '__main__':
    cur_dir = os.curdir

    _r = create_database(cur_dir, 'bets.json', 'bets.db', 'terms.json')
    if not _r:
        print('ERRO. Falha ao criar o banco de dados.')
        exit(-1)

    params = {
        'ParticipantSpan': 'Arsenal',
        'MarketDescription': 'Vencedor Final',
        'FixtureName': 'Inglaterra - Premier League 2023/24'
    }
    _res = query_db_01(cur_dir, 'bets.db', params)
    for k, v in _res.items():
        print(k, v)
