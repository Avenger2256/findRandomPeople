import asyncio
import config
import admin

from loguru import logger
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

token = config.load('cfg')['token']
l = config.load('str')
logger.add('log_{time:DD.MM.YYYY}.log', rotation='1 day')

dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message):
    await message.answer(l['start'].format(name=message.from_user.first_name))

async def main() -> None:
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logger.info('STARTED')
    await dp.start_polling(bot)
    logger.critical('END')


if __name__ == "__main__":
    asyncio.run(main())