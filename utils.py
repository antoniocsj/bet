import json


def write_json(filename: str, _dict: dict):
    with open(filename, 'w') as file:
        json.dump(_dict, file, indent=4, ensure_ascii=False)

