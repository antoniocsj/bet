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


def teste_01():
    apostas = read_json('apostas.json')
    pass


if __name__ == '__main__':
    teste_01()
