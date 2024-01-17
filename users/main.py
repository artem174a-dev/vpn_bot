from datetime import timedelta, datetime

from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery, WebAppInfo
from aiogram.types import InlineKeyboardButton as button
from aiogram.dispatcher import FSMContext

from database import check_and_insert_user, get_user_info
from messages import START_NEW_USER, NEW_KEY, START_OLD_USER
from vpn_api import VPN_API

SUBSCRIPTIONS_PLANS = {
    32_212_254_720: 30,
    75_161_927_680: 70,
    128_849_018_880: 120,
    536_870_912_000: 500
}


def bytes_to_gb(byte_value):
    gb_value = byte_value / (1024 ** 3)
    return '{:.2f} GB'.format(gb_value)


def days_until_next_update(registration_date):
    next_tariff_update = registration_date + timedelta(days=30)

    days_until_update = (next_tariff_update - datetime.now()).days

    return next_tariff_update, days_until_update


async def wellcome(message: Message):
    print(message.from_user.username)
    user_exists = check_and_insert_user(
        message.from_user.id,
        {
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name
        }
    )
    if user_exists is False:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(button('Получить VPN', callback_data='get_vpn'))
        await message.answer(START_NEW_USER, reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(button('Моя статистика', web_app=WebAppInfo(url=f"https://www.vpn-gptalk.ru/monitor/{message.from_user.id}")))
        data = get_user_info(message.from_user.id)
        remains = int(data['data_limit']) - int(data['used_bytes'])
        try:
            next_update_date, days_until_update = days_until_next_update(data['key_reg_time'])
            text = f'''
> VPN KEY
<code>{data['access_url']}</code>

> <b>Остаток:</b> {bytes_to_gb(remains)} Гб.
> <b>Тарифный план:</b> {SUBSCRIPTIONS_PLANS[int(data['data_limit'])]} Гб.

> <b>Трафик обновится:</b> {str(next_update_date)[:10]} ({days_until_update})
'''
            await message.answer(text, reply_markup=keyboard)
        except Exception as e:
            print(e)


async def all_callback(call: CallbackQuery, state: FSMContext):
    call_data = call.data
    try:
        await eval(f'{call_data}(call, state)')
    except Exception as e:
        print(e)


async def get_vpn(call: CallbackQuery, state: FSMContext):
    # Запись нового ключа в бд
    url = VPN_API().new_key(call.from_user.id, 'FREE_PLAN')
    await call.message.answer(NEW_KEY.format(url), disable_web_page_preview=True)
