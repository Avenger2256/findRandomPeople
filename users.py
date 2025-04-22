from config import *
from random import choice
from loguru import logger

logger.add('logs/log_{time:DD.MM.YYYY}.log', retention='7 days')

l = load('str')['log']

def findRandom(userId: str):
    data = load()
    randomId = choice(list(data.keys()))
    data = data[randomId]
    if data['ban'] == False and randomId != userId:
        if l['find']:
            logger.info(l['find'].format(id = userId, id2 = data['']))
        return data
    else:
        return findRandom(userId)

def getById(userId: str, fromUserId: str):
    data = load()
    if userId not in data:
        if l['errFindId']:
            logger.error(l['errFindId'].format(id = fromUserId, id2 = userId))
        return
    else:
        if l['findId']:
            logger.success(l['findId'].format(id = fromUserId, id2 = userId))
        return data[userId]

def addUser(userId: str, description: str):
    data = load()
    if userId not in data:
        if l['create']:
            logger.info(l['create'].format(id = userId, description = description))
        data[userId] = {
            'id': userId,
            'description': description,
            'ban': False
        }
    else:
        if l['update']:
            logger.info(l['update'].format(id = userId, description = description))
        data[userId]['description'] = description
    save(data)

def deleteUser(userId: str):
    data = load()
    if userId not in data:
        if l['deleteError']:
            logger.error(l['deleteError'].format(id=userId))
        return
    else:
        data.pop(userId)
        save(data)
        if l['delete']:
            logger.error(l['delete'].format(id=userId))
def banUser(userId: str):
    data = load()
    if userId not in data:
        addUser(userId, 'Auto created for ban')
        banUser(userId)
    else:
        data[userId]['ban'] = True
        save(data)
        if l['ban']:
            logger.success(l['ban'].format(id=userId))

def unbanUser(userId: str):
    data = load()
    admins = load('cfg')['admins']
    if userId not in data or admins[userId] == 2:
        if l['unbanError']:
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