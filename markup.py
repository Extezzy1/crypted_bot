from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


btn_cancel = InlineKeyboardButton(text="Назад ⏪", callback_data="back")

start_markup = InlineKeyboardMarkup(row_width=1)
cipher_with_offset = InlineKeyboardButton(text="Шифр цезаря со сдвигом", callback_data="cipher_with_offset")
cipher_with_key = InlineKeyboardButton(text="Шифр цезаря с ключом", callback_data="cipher_with_key")
cipher_gamma = InlineKeyboardButton(text="Шифр гаммирование", callback_data="cipher_gamma")
start_markup.add(cipher_with_offset, cipher_with_key, cipher_gamma)


markup_cipher_with_offset = InlineKeyboardMarkup(row_width=1)
btn_crypt = InlineKeyboardButton(text="Зашифровать", callback_data="crypt_with_offset")
btn_decrypt = InlineKeyboardButton(text="Расшифровать", callback_data="decrypt_with_offset")
markup_cipher_with_offset.add(btn_crypt, btn_decrypt, btn_cancel)


markup_cipher_with_key = InlineKeyboardMarkup(row_width=1)
btn_crypt = InlineKeyboardButton(text="Зашифровать", callback_data="crypt_with_key")
btn_decrypt = InlineKeyboardButton(text="Расшифровать", callback_data="decrypt_with_key")
markup_cipher_with_key.add(btn_crypt, btn_decrypt, btn_cancel)


markup_cipher_gamma = InlineKeyboardMarkup(row_width=1)
btn_crypt = InlineKeyboardButton(text="Зашифровать", callback_data="crypt_gamma")
btn_decrypt = InlineKeyboardButton(text="Расшифровать", callback_data="decrypt_gamma")
markup_cipher_gamma.add(btn_crypt, btn_decrypt, btn_cancel)

