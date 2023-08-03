import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import Message
from aiogram.utils import executor
import aiohttp
import django
import os
import asyncio


class Meta:
    app_label = 'botapp'
    

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parsing_project.settings')
django.setup()
    
TOKEN = "6574387464:AAEbelWohNX8adpamp8UlGJxtm40yqQeThI"  

django.setup()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Список команд для вашего бота
COMMANDS_LIST = [
    "/start - Показать список команд",
    "/list - Показать список товаров"
]


DANGO_API_URL = 'http://localhost:8000/v1/products/'
async def get_products_from_django_api():
    async with aiohttp.ClientSession() as session:
        async with session.get(DANGO_API_URL) as response:
            products_list = await response.json()
            return products_list

@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    user_name = message.from_user.first_name
    await message.reply(
        f"Привет, {user_name}!.\n\n"
        f"Список доступных команд:\n"
        f"\n".join(COMMANDS_LIST)
    )
    logger.info(f"Отправлено приветственное сообщение пользователю {user_name}")

@dp.message_handler(commands=['list'])
async def show_product_list(message: Message):
    products_list = await get_products_from_django_api()
    
    
    products_text = "\n".join([f"{product['name']} - {product['link'][:1]}..." for product in products_list][:5])

    print(products_text)
    await message.reply(f"Список товаров:\n" + products_text)


async def main():
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':
    logger.info("Бот запущен")
    executor.start_polling(dp, skip_updates=True)