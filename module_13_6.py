from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

API_TOKEN = '7787493433:AAGBdEiUhUvCcydfXXxFbbS_F_T_Ca5Tfbk'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Рассчитать"), KeyboardButton(text="Информация")],
        [KeyboardButton(text="Купить")]
    ],
    resize_keyboard=True
)


inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")],
        [InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")]
    ]
)


inline_product_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product2", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product3", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product4", callback_data="product_buying")]
    ]
)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=keyboard)

@dp.message(lambda message: message.text == "Рассчитать")
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=inline_keyboard)

@dp.callback_query(lambda call: call.data == "calories")
async def set_age(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)

@dp.callback_query(lambda call: call.data == "formulas")
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer("Формула Миффлина-Сан Жеора:\nBMR = 10 * вес + 6.25 * рост - 5 * возраст - 161")

@dp.message(UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост (в сантиметрах):")
    await state.set_state(UserState.growth)

@dp.message(UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес (в килограммах):")
    await state.set_state(UserState.weight)

@dp.message(UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']
    bmr = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f"Ваша норма калорий: {bmr:.2f} ккал.")
    await state.clear()

@dp.message(lambda message: message.text == "Информация")
async def info_command(message: types.Message):
    await message.answer("Я помогу вам рассчитать норму калорий на основе вашего возраста, роста и веса.")

@dp.message(lambda message: message.text == "Купить")
async def get_buying_list(message: types.Message):
    products = [
        {"name": "Product1", "description": "описание 1", "price": 100, "image_url": "https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fpixy.org%2Fsrc%2F476%2F4766947.jpg&lr=973&pos=2&rpt=simage&text=таблетки"},
        {"name": "Product2", "description": "описание 2", "price": 200, "image_url": "https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fpixy.org%2Fsrc%2F476%2F4766947.jpg&lr=973&pos=2&rpt=simage&text=таблетки"},
        {"name": "Product3", "description": "описание 3", "price": 300, "image_url": "https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fpixy.org%2Fsrc%2F476%2F4766947.jpg&lr=973&pos=2&rpt=simage&text=таблетки"},
        {"name": "Product4", "description": "описание 4", "price": 400, "image_url": "https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fpixy.org%2Fsrc%2F476%2F4766947.jpg&lr=973&pos=2&rpt=simage&text=таблетки"}
    ]
    
    for product in products:

        await bot.send_photo(
            chat_id=message.chat.id,
            photo=product["image_url"],
            caption=f"Название: {product['name']} | Описание: {product['description']} | Цена: {product['price']} рублей."
        )
    

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_product_keyboard)



@dp.callback_query(lambda call: call.data == "product_buying")
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")

async def main():
    print("Bot is running...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
