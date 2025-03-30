import random
from config import *
from random import choice
from loguru import logger

logger.add('logs/log_{time:DD.MM.YYYY}.log', retention='7 days')

def findRandom(userId: str):
    data = load()
    randomId = choice(list(data.keys()))
    data = data[randomId]
    if data['ban'] == False and randomId != userId:
        logger.info(f'{userId} нашел {data['id']}')
        return data
    else:
        return findRandom(userId)

def getById(userId: str):
    data = load()
    if userId not in data:
        return
    else:
        return data[userId]

def addUser(userId: str, description: str):
    data = load()
    if userId not in data:
        logger.info(f'{userId} создал анкету | {description}')
        data[userId] = {
            'id': userId,
            'description': description,
            'ban': False
        }
    else:
        logger.info(f'{userId} обновил анкету | {description}')
        data[userId]['description'] = description
    save(data)

def deleteUser(userId: str):
    data = load()
    if userId not in data:
        logger.error(f'Не удалось удалить анкету {userId} | 404')
        return
    else:
        data.pop(userId)
        save(data)
        logger.succes(f'Анкета {userId} удалена')
def banUser(userId: str):
    data = load()
    if userId not in data:
        logger.error(f'Не удалось забанить {userId} | 404')
        return
    else:
        data[userId]['ban'] = True
        save(data)
        logger.success(f'Пользователь {userId} забанен')

def unbanUser(userId: str):
    data = load()
    if userId not in data:
        logger.error(f'Не удалось разбанить {userId} | 404')
        return
    else:
        data[userId]['ban'] = False
        save(data)
        logger.success(f'Пользователь {userId} разбанен')

def checkUser(userId: str):
    data = load()
    if userId not in data:
        return False
    else:
        return data[userId]['ban']

def promoteUser(userId: str):
    k = 'admins' # key word
    data = load('cfg')
    if userId not in data[k]:
        data[k][userId] = 1 # admin
        save(data, 'config.json')
        logger.success(f'Пользователь {userId} повышен до уровня админа')
    elif data[k][userId] == 1:
        data[k][userId] = 2 # owner
        save(data, 'config.json')
        logger.success(f'Пользователь {userId} повышен до уровня создателя')
    elif data[k][userId] == 2:
        logger.success(f'Пользователь {userId} не повышен. Достигнут максимальный уровень')
        return

def demoteUser(userId: str):
    k = 'admins' # key word
    data = load('cfg')
    if userId not in data[k]:
        logger.success(f'Пользователь {userId} не имеет прав')
        return
    elif data[k][userId] == 1:
        data[k].pop(userId)
        save(data, 'config.json')
        logger.success(f'Пользователь {userId} снят')
        return 0
    elif data[k][userId] == 2:
        data[k][userId] = 1
        save(data, 'config.json')
        logger.succes(f'Пользователь {userId} понижен с создателя до админа')
        return 1