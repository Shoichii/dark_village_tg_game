from datetime import datetime
import re

from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

import bot.db.common as db_common
from bot.loader import router
from bot.utils.keaboards.common_kb import female_button, male_button, select_gender
from bot.utils.other import date_pattern
from bot.utils.states.ProfileDataState import ProfileDataState


### команды в лс боту ###


# старт
@router.message(Command('start'), StateFilter('*'))
async def start_handler(msg: types.Message, state: FSMContext):
    '''Главная команда /start'''

    # если команда вызвана не в лс у бота
    if msg.chat.id != msg.from_user.id:
        return

    await state.clear()

    # есть ли такой юзер
    user = await db_common.get_user(msg.from_user.id)
    if not user:
        # процесс регистрации
        await state.update_data(registration=True)
        await msg.answer('Твой пол', reply_markup=select_gender())
    else:
        pass


@router.callback_query(lambda call: call.data == male_button or call.data == female_button)
async def select_gender_handler(call: types.CallbackQuery, state: FSMContext):
    '''Выбор пола'''
    await call.message.delete()
    data = await state.get_data()
    is_registration = data.get('registration')

    if is_registration:
        # записываем пол и спрашиваем дату рождения
        await state.update_data(gender=call.data.split('_')[0])
        await call.message.answer('Твоя дата рождения. Напиши в формате: 01.01.1970')
        await state.set_state(ProfileDataState.birthday)
    else:
        pass


@router.message(StateFilter(ProfileDataState.birthday))
async def set_birthday_handler(msg: types.Message, state: FSMContext):
    '''Установка даты рождения'''
    if not re.match(date_pattern, msg.text):
        await msg.answer('Неверный формат')
        return

    data = await state.get_data()
    gender = data.get('gender')
    birthday = datetime.strptime(msg.text, '%d.%m.%Y').date()

    await db_common.create_new_user(msg.from_user.id, gender, birthday)
    await msg.answer('Регистрация завершена')
    await state.clear()
