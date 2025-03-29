from config import *
from random import choice

def findRandom(userId: str):
    data = load()
    randomId = choice(data)
    data = data[randomId]
    if data['ban'] != False and randomId != userId:
        return data
    else:
        return findRandom(userId)
def getById(userId: str):
    data = load()
    if userId not in data:
        return 'NotFound'
    else:
        return data[userId]
def addUser(userId: str, description: str):
    data = load()
    if userId not in data:
        data[userId] = {
            'id': userId,
            'description': description,
            'ban': False
        }
    else:
        data[userId]['description'] = description
    save(data)