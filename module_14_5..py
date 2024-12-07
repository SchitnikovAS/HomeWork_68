from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from DB_BOT.crud_functions import *

products = get_all_products()

api = '**************************************************'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text="Информация")
button_3 = KeyboardButton(text="Купить")
button_4 = KeyboardButton(text="Регистрация")
kb.row(button_4, button_3)
kb.row(button, button_2)

kb_inline = InlineKeyboardMarkup()
button_in = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
button_in_2 = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
kb_inline.row(button_in, button_in_2)

kb_bye = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product4', callback_data='product_buying')]
    ],
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


# Registration
@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит): ')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    data_reg = await state.get_data()
    print(data_reg)
    if not is_included(data_reg['username']):
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя ')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст: ')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data_reg = await state.get_data()
    add_user(data_reg['username'], data_reg['email'], data_reg['age'])
    await message.answer('Регистрация прошла успешно!')
    await state.finish()


# Registration complited

@dp.message_handler(text='Рассчитать')
async def start_in(message):
    await message.answer('Выберите опцию:', reply_markup=kb_inline)


@dp.message_handler(text=['Информация'])
async def inform(message):
    await message.answer('Я расчитаю вашу дневную норму калорий! Для этого нажми кнопку расчитать!')


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    count = 0
    for product in products:
        count += 1
        with open(f'Product_{count}.jpg', 'rb') as img:
            await message.answer_photo(img, f'Название: {product[1]} | Описание: {product[2]} '
                                            f'| Цена: {product[3]}')
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_bye)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def formula(call):
    await call.message.answer('(10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161)')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст: ')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост: ')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    send = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f'Ваша норма каллорий {send}')
    await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
