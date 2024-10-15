import pathlib

from aiogram import Bot, Dispatcher
import decouple
from aiogram import Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

path = pathlib.Path().absolute()
bot = Bot(token=decouple.config('TOKEN'),
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()
dp = Dispatcher()
dp.include_router(router)
