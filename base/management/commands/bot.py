import asyncio

from aiogram import BaseMiddleware, types
from django.core.management.base import BaseCommand

import bot.handlers
from bot.loader import bot, dp


class Command(BaseCommand):
    help = 'Запуск бота'

    async def start_bot(self):
        try:
            await dp.start_polling(bot)
        finally:
            await bot.session.close()

    def handle(self, *args, **options):
        asyncio.run(self.start_bot())
