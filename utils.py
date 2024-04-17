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


def write_json(filename: str, _dict: dict):
    with open(filename, 'w') as file:
        json.dump(_dict, file, indent=4, ensure_ascii=False)


def tuple_parameters_ok(_tuple: tuple):
    for elem in _tuple:
        if not isinstance(elem, str) or elem == '':
            return False
    return True
