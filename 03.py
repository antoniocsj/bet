import os
import json


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


if __name__ == '__main__':
    teste_01()
