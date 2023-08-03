import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from products.models import Product
import os

TOKEN = "6574387464:AAEbelWohNX8adpamp8UlGJxtm40yqQeThI"  

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Handler for the /start command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Для просмотра списка товаров используй команду /show_products.")


@dp.message_handler(commands=['show_products'])
async def show_products(message: types.Message):
    products = Product.objects.all().order_by('-id')[:10]
    if not products:
        await message.answer("Список товаров пуст. Сначала выполните парсинг.")
        return
    formatted_list = '\n'.join([f"{i+1}. [{product.name}]({product.link})" for i, product in enumerate(products)])
    await message.answer(f"Список последних {len(products)} товаров:\n{formatted_list}", parse_mode=ParseMode.MARKDOWN)


async def run_bot():
    executor.start_polling(dp, skip_updates=True)
    

