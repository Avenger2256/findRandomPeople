import json
from loguru import logger
import sys

def load(type='users'):
    if type == 'cfg':
        path = 'config.json'
    else:
        path = 'users.json'
    try:
        with open(path, 'r', encoding='UTF-8') as file:
            return json.load(file)
    except FileNotFoundError:
        if type != 'cfg':
            return {}
        else:
            with open('config.json', 'w', encoding='UTF-8') as file:
                file.write('{'+f'\n')
                file.write(f'    "token": "{input('Enter your bot token: ')}"\n')
                file.write('}')
            return load('cfg')
    except Exception as e:
        logger.add('log.log', retention='7 days')
        logger.error(e)

def save(data):
    with open('users.json', 'w', encoding='UTF-8') as file:
        json.dump(data, file)