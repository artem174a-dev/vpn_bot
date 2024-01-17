from aiogram import Dispatcher
from aiogram.types import ContentType

from users.main import wellcome, get_vpn, all_callback


def register_all_handlers(dp: Dispatcher):
    dp.register_message_handler(wellcome, commands=["start"], state="*", content_types=ContentType.ANY)
    dp.register_callback_query_handler(all_callback, state='*')
