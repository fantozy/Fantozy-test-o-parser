import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import Message
from aiogram.utils import executor
import aiohttp
import django
import os



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

COMMANDS_LIST = [
    "/list - Показать список товаров"
]

from based_sigma import Client
 
DANGO_API_URL = 'http://localhost:8000/v1/products/'


async def get_products_from_django_api():
    async with aiohttp.ClientSession() as session:
        async with session.get(DANGO_API_URL) as response:
            products_list = await response.json()
            return products_list


async def get_response_from_django_api():
    async with aiohttp.ClientSession() as session:
        async with session.get(DANGO_API_URL) as response:
            status = response.status
            return status


async def finished_parsing(count: int):
    chat_id = Client.get_client_id()
    print(chat_id)
    await bot.send_message(chat_id, f"FINISHED {count}")
        
    
@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    user_name = message.from_user.first_name
    chat_id = message.chat.id
    Client.save_client_id(chat_id)
    await message.reply(
        f"Привет, {user_name}!.\n\n"
        f"Список доступных команд:\n"
        f"\n".join(COMMANDS_LIST)
    )
    logger.info(f"{Client.get_client_id()}")
        
@dp.message_handler(commands=['list'])
async def show_product_list(message: Message):
    products_list = await get_products_from_django_api()
    products_text = "\n".join([f"\n{i + 1}\n {product['name']} - {product['link'][:40]}..." for i, product in enumerate(products_list)][:10])
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