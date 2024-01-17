import asyncio
import datetime
import logging
import multiprocessing
import time

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database import get_user_info, get_all_user_info, Database
from handlers import register_all_handlers
from vpn_api import VPN_API

logger = logging.getLogger(__name__)

API_TOKEN = '6856814952:AAEw-poUeuHG_5lmHEFUYCEph8JseCsWH2Q'


async def update_usage():
    time_now = int(time.time())
    while True:
        db = Database()
        if int(time.time()) - time_now >= 600:
            time_now = int(time.time())
            print('Update usages')
            usage_data_api = VPN_API().client.get_keys()
            for key in usage_data_api:
                if not key.name.isdigit():
                    continue
                insert_user_query = f"""
                        INSERT INTO vpn_bot.usage (key_id, user_id, used_bytes, add_time)
                        VALUES ('{key.key_id}', '{key.name}', '{key.used_bytes}', '{datetime.datetime.now()}');
                    """
                try:
                    db.execute(insert_user_query)
                except Exception as e:
                    print(e)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    storage = MemoryStorage()
    bot = Bot(token=API_TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


def func1():
    asyncio.run(main())


def func2():
    asyncio.run(update_usage())


if __name__ == '__main__':
    try:
        # Создаем процессы для каждой функции
        process1 = multiprocessing.Process(target=func1)
        process2 = multiprocessing.Process(target=func2)

        # Запускаем процессы
        process1.start()
        process2.start()

        process1.join()
        process2.join()
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
        pass
