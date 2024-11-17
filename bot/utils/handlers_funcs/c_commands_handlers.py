import bot.db.common as db_common


async def check_reg_and_commands(*args):
    '''Проверка регистрации пользователя
    и место выполнения команды'''

    msg, user_id, chat_id = args
    accept = True

    # зареган ли пользователь
    user = await db_common.get_user(user_id)
    if not user:
        await msg.reply('Пожалуйста, сначала зарегистрируйся(пиши в лс)')
        accept = False

    # если команда вызвана в лс у бота
    if chat_id == user_id:
        await msg.answer('Команда выполняется только в общем чате')
        accept = False

    return accept
