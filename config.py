import json
from loguru import logger
from random import choice

logger.add('logs/log_{time:DD.MM.YYYY}.log', retention='7 days')

def load(type='users'):
    if type == 'cfg':
        path = 'config.json'
    elif type == 'users':
        path = 'users.json'
    elif type == 'str':
        path = 'strings.json'
    try:
        with open(path, 'r', encoding='UTF-8') as file:
            return json.load(file)
    except FileNotFoundError:
        if type == 'users':
            return {}
        elif type == 'cfg':
            with open('config.json', 'w', encoding='UTF-8') as file:
                file.write('{'+f'\n')
                file.write(f'    "token": "{input('Enter your bot token: ')}",\n')
                file.write('    "admins": {')
                file.write(f'       "{input('Enter your telegram id: ')}": 2')
                file.write('    }')
                file.write('}')
            return load('cfg')
        elif type == 'str':
            logger.critical('STRINGS.JSON IS NOT FOUND')
            exit()
    except Exception as e:
        logger.error(e)

def save(data, path = 'users.json'):
    with open(path, 'w', encoding='UTF-8') as file:
        json.dump(data, file)