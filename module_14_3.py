from aiogram import executor, Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from crud_functions import *

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

initiate_db()
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
button3 = KeyboardButton(text="Купить")
button4 = KeyboardButton(text="Регистрация")
kb.row(button1, button2, button3, button4)

ik = InlineKeyboardMarkup(resize_keyboard=True)
bt1 = InlineKeyboardButton(text="рассчитать норму каллорий", callback_data="calories")
bt2 = InlineKeyboardButton(text='Формулы рассчёта', callback_data="formulas")
ik.row(bt1, bt2)

ik3 = InlineKeyboardMarkup(resize_keyboard=True)
btt1 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
btt2 = InlineKeyboardButton(text="Product2", callback_data="product_buying")
btt3 = InlineKeyboardButton(text="Product3", callback_data="product_buying")
btt4 = InlineKeyboardButton(text="Product4", callback_data="product_buying")
ik3.row(btt1, btt2, btt3, btt4)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!!")


@dp.message_handler(text="Купить")
async def get_buying_list(call):
    for i in range(0, 4):
        await call.answer(
            f"Название: {get_all_products()[i][1]}| Описание: {get_all_products()[i][2]}| Цена: {get_all_products()[i][3]}")
        product = f'product ({i}).jpg'
        with open(product, "rb") as picture:
            await call.answer_photo(picture)

    await call.answer("Выберите продукт для покупки: ", reply_markup=ik3)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")


@dp.message_handler(text="Рассчитать")
async def Main_Menu(message):
    await message.answer("Выберете опцию", reply_markup=ik)


@dp.message_handler(commands="start")
async def show_kb(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb)


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    calories = 10 * int(data.get("weight")) + 6.25 * int(data.get("growth")) - 5 * int(data.get("age")) + 5

    await message.answer(f"Ваша норма каллорий равна {calories}")


@dp.message_handler(text = "Регистрация")
async def sign_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя ")
        await RegistrationState.username.set()

    else:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    if is_includ_email(message.text):
        await message.answer("Данный email уже есть в базе, введите другой!")
        await RegistrationState.email.set()

    else:

        await state.update_data(email=message.text)
        await message.answer("Введите свой возраст")
        await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_users(data.get('username'), data.get('email'),data.get('age'))
    await state.finish()




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
