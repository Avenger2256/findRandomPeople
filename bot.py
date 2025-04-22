import asyncio
import config
import admin

from users import *

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


class Form(StatesGroup):
    description = State()


cfg = config.load('cfg')
l = config.load('str')

dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    await message.answer(l['bot']['start'].format(name=message.from_user.first_name))


@dp.message(lambda message: message.text.startswith('/find'))
async def find_command(message: Message):
    user_id = str(message.from_user.id)
    data = findRandom(user_id)
    await message.answer(l['bot']['user'].format(id=data['id'], description=data['description']))


@dp.message(Command('new'))
async def new_command(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    await message.answer(l['bot']['new'])
    await state.set_state(Form.description)


@dp.message(Form.description)
async def process_description(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    description = message.text
    createUser(user_id, description)
    await state.clear()
    await message.answer(l['bot']['create'].format(description=description))

@dp.message(Command('my'))
async def my_command(message: Message):
    user_id = str(message.from_user.id)
    findUser(user_id)

@dp.message(Command('delete'))
async def delete_command(message: Message):
    user_id = str(message.from_user.id)
    deleteUser(user_id)

async def main():
    bot = Bot(token=cfg['token'], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logger.success(l['log']['bot_on'])
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.critical(l['log']['bot_off_by_user'])
    except Exception as e:
        logger.critical(l['log']['bot_off_incident'].format(error=str(e)))