import asyncio
import config
import admin
from users import *

from loguru import logger
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

cfg = config.load('cfg')
l = config.load('str')
logger.add('logs/log_{time:DD.MM.YYYY}.log')

dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message):
    logger.info(str(message.from_user.id)+' /start')
    await message.answer(l['bot']['start'].format(name=message.from_user.first_name))

@dp.message()
async def message_handler(message):
    logger.info(str(message.from_user.id)+' '+message.text)
    if message.text.startswith('/find'):
        data = findRandom(str(message.from_user.id))
        await message.answer(l['bot']['user'].format(id=data['id'], description=data['description']))

async def main():
    bot = Bot(token=cfg['token'], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logger.success('STARTED')
    await dp.start_polling(bot)
    logger.critical('END')

if __name__ == "__main__":
    asyncio.run(main())