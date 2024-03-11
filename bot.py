""" 
создаем бота и получаем данные из чата
"""
import asyncio, logging, os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from paypalsdk import Paypal
from dotenv import load_dotenv
from db_requests import create_user, check_subscribe


load_dotenv()
logging.basicConfig(level=logging.INFO)
CHANEL_ID = os.getenv('CHANEL_ID')

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    telegram_id = message.from_user.id
    if await create_user(telegram_id):
        print("Пользователь", telegram_id, "добавлен в базу")
    else:
        print("Пользователь", telegram_id, "уже был в базе")
    check = await check_subscribe(telegram_id)
    await message.answer(f"Приветствую, ваша подписка {'активна' if check else 'неактивна'}")
    if not check:
        await message.answer(f"Чтобы получить подписку вам необходимо внести платеж по нашей ссылке. Для получения ссылки на оплату введите команду /inline_url")
    
    

@dp.message(Command('inline_url'))
async def cmd_inline_url(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='PayPalPayment', url=Paypal.get_payment_link()))
    await message.answer(
        'To pay for your subscription please click below.',
        reply_markup=builder.as_markup()
    )
    

@dp.message(Command('content'))
async def cmd_content(message: types.Message):
    ...


async def main():
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())