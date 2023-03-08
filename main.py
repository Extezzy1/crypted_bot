import logging
import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.database import Database
import markup
import FSM
import cipher


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.api_token)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database("database/database.sqlite")


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    if not db.exist_user(message.chat.id):
        db.add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await bot.send_message(message.chat.id, "Привет! Выбери алгоритм шифрования ⬇⬇⬇", reply_markup=markup.start_markup)


@dp.callback_query_handler(lambda c: c.data == "back")
async def back(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup(markup.start_markup)


@dp.callback_query_handler(lambda c: c.data == "cipher_with_offset")
async def cipher_with_offset(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup(markup.markup_cipher_with_offset)


@dp.callback_query_handler(lambda c: c.data == "cipher_with_key")
async def cipher_with_key(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup(markup.markup_cipher_with_key)


@dp.callback_query_handler(lambda c: c.data == "cipher_gamma")
async def cipher_gamma(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup(markup.markup_cipher_gamma)


@dp.callback_query_handler(lambda c: c.data == "crypt_with_offset")
async def crypt_with_offset(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введи фразу для шифрования ⬇⬇⬇")
    await FSM.FSMOffset.enter_phrase.set()
    async with state.proxy() as data:
        data["type_of_procedure"] = "crypt_offset"


@dp.callback_query_handler(lambda c: c.data == "decrypt_with_offset")
async def decrypt_with_offset(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введи фразу для расшифрования ⬇⬇⬇")
    await FSM.FSMOffset.enter_phrase.set()
    async with state.proxy() as data:
        data["type_of_procedure"] = "decrypt_offset"


@dp.callback_query_handler(lambda c: c.data == "crypt_with_key")
async def crypt_with_key(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введи фразу для шифрования ⬇⬇⬇")
    await FSM.FSMOffset.enter_phrase.set()
    async with state.proxy() as data:
        data["type_of_procedure"] = "crypt_key"


@dp.callback_query_handler(lambda c: c.data == "decrypt_with_key")
async def decrypt_with_key(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введи фразу для расшифрования ⬇⬇⬇")
    await FSM.FSMOffset.enter_phrase.set()
    async with state.proxy() as data:
        data["type_of_procedure"] = "decrypt_key"


@dp.callback_query_handler(lambda c: c.data == "crypt_gamma")
async def crypt_gamma(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введи фразу для шифрования ⬇⬇⬇")
    await FSM.FSMOffset.enter_phrase.set()
    async with state.proxy() as data:
        data["type_of_procedure"] = "crypt_gamma"


@dp.callback_query_handler(lambda c: c.data == "decrypt_gamma")
async def decrypt_gamma(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введи фразу для расшифрования ⬇⬇⬇")
    await FSM.FSMOffset.enter_phrase.set()
    async with state.proxy() as data:
        data["type_of_procedure"] = "decrypt_gamma"


@dp.message_handler(state=FSM.FSMOffset.enter_phrase)
async def enter_phrase(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phrase"] = message.text.strip()
    type_of_procedure = data["type_of_procedure"]
    if type_of_procedure == "crypt_offset" or type_of_procedure == "decrypt_offset":
        await bot.send_message(message.chat.id, "Записал! Теперь введи сдвиг (целое число) ⬇⬇⬇")
    elif type_of_procedure == "crypt_key" or type_of_procedure == "decrypt_key":
        await bot.send_message(message.chat.id, "Записал! Теперь введи ключевое слово ⬇⬇⬇")
    elif type_of_procedure == "crypt_gamma" or type_of_procedure == "decrypt_gamma":
        await bot.send_message(message.chat.id, "Записал! Теперь введи гамму ⬇⬇⬇")
    await FSM.FSMOffset.enter_offset.set()


@dp.message_handler(state=FSM.FSMOffset.enter_offset)
async def enter_offset(message: types.Message, state: FSMContext):
    msg = message.text.strip()
    async with state.proxy() as data:
        phrase = data.get("phrase", "")
        if data["type_of_procedure"] == "crypt_offset":
            if message.text.strip().isdigit():
                result = await cipher.crypt_with_offset(phrase, int(msg))
                if result[0]:
                    await bot.send_message(message.chat.id, f"Удалось зашифровать! Зашифрованная фраза: {result[1]}",
                                           reply_markup=markup.start_markup)
                else:
                    await bot.send_message(message.chat.id, f"Не удалось зашифровать! Проверь введенные данные!",
                                           reply_markup=markup.start_markup)
            else:
                await bot.send_message(message.chat.id, "Сдвиг должен быть целым числом! Повтори ввод!")
        elif data["type_of_procedure"] == "decrypt_offset":
            if message.text.strip().isdigit():
                result = await cipher.decrypt_with_offset(phrase, int(msg))
                if result[0]:
                    await bot.send_message(message.chat.id, f"Удалось расшифровать! Расшифрованная фраза: {result[1]}",
                                           reply_markup=markup.start_markup)
                else:
                    await bot.send_message(message.chat.id, f"Не удалось расшифровать! Проверь введенные данные!",
                                           reply_markup=markup.start_markup)
            else:
                await bot.send_message(message.chat.id, "Сдвиг должен быть целым числом! Повтори ввод!")
        elif data["type_of_procedure"] == "crypt_key":
            result = cipher.crypt_with_key_word(phrase, msg)
            await bot.send_message(message.chat.id, f"Изначальный алфавит: {result[0]}\n"
                                                    f"Алфавит с ключевым словом: {result[1]}\n"
                                                    f"Зашифрованная фраза: {result[2]}\n",
                                   reply_markup=markup.start_markup)
        elif data["type_of_procedure"] == "decrypt_key":
            result = cipher.decrypt_with_key_word(phrase, msg)
            await bot.send_message(message.chat.id, f"Изначальный алфавит: {result[0]}\n"
                                                    f"Алфавит с ключевым словом: {result[1]}\n"
                                                    f"Расшифрованная фраза: {result[2]}\n",
                                   reply_markup=markup.start_markup)
        elif data["type_of_procedure"] == "crypt_gamma":
            result = cipher.crypt_gamma(phrase, msg)
            await bot.send_message(message.chat.id, f"Зашифрованная фраза: {result}\n",
                                   reply_markup=markup.start_markup)
        elif data["type_of_procedure"] == "decrypt_gamma":
            result = cipher.decrypt_gamma(phrase, msg)
            await bot.send_message(message.chat.id, f"Расшифрованная фраза: {result}\n",
                                   reply_markup=markup.start_markup)
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)