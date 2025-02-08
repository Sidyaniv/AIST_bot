import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from credentials import BOT_API
from content_type import ContentTypeFilter


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_API)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Определяем состояния диалога
class Form(StatesGroup):
    name = State()
    city = State()
    age = State()
    school_class = State()
    interests = State()
    test = State()
    final = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.reply(
        "Привет! Давай знакомиться! Меня зовут Аист! Я виртуальный персональный репетитор.\n\n"
        "Теперь, расскажи немного о себе. Как тебя зовут?"
    )
    await state.set_state(Form.name)


@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply("Из какого ты города?")
    await state.set_state(Form.city)


@dp.message(Form.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.reply("Сколько тебе лет?")
    await state.set_state(Form.age)


@dp.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply("Пожалуйста, введи число для возраста.")
        return
    await state.update_data(age=int(message.text))
    await message.reply("В каком классе ты учишься?")
    await state.set_state(Form.school_class)


@dp.message(Form.school_class)
async def process_school_class(message: types.Message, state: FSMContext):
    await state.update_data(school_class=message.text)
    await message.reply("Что тебе нравится?")
    await state.set_state(Form.interests)


@dp.message(Form.interests)
async def process_interests(message: types.Message, state: FSMContext):
    await state.update_data(interests=message.text)
    await message.reply(
        "Чтобы я мог лучше понять, как лучше тебе помочь, ответь еще на несколько вопросов:\n"
        "Какой твой любимый предмет в школе?"
    )
    await state.set_state(Form.test)


@dp.message(Form.test)
async def process_test(message: types.Message, state: FSMContext):
    await state.update_data(fav_subject=message.text)
    await message.reply(
        "Теперь, когда мы с тобой знакомы, ты можешь задать свой вопрос или скинуть фотографию своего задания, чтобы я мог его проверить."
    )
    await state.set_state(Form.final)


@dp.message(Form.final, ContentTypeFilter([ContentType.TEXT, ContentType.PHOTO]))
async def process_final(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    logging.info(f"Данные пользователя: {user_data}")

    if message.photo:
        await message.reply("Спасибо за фотографию! Я постараюсь проверить задание как можно скорее.")
    else:
        await message.reply("Спасибо за вопрос! Я постараюсь ответить как можно скорее.")
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
