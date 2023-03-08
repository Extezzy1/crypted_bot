import asyncio

alphabet_russian = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й',
                                'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
                                'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
alphabet_english = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                    's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


async def crypt_with_offset(phrase, offset):
    try:
        resultStr = ""
        if phrase[0] in alphabet_russian:
            for symbol in phrase:
                if symbol in alphabet_russian:
                    mesto = alphabet_russian.index(symbol)

                    new_mesto = mesto + offset
                    if new_mesto >= len(alphabet_russian):
                        new_mesto %= len(alphabet_russian)
                    resultStr += alphabet_russian[new_mesto]
                else:
                    resultStr += symbol
        elif phrase[0] in alphabet_english:
            for symbol in phrase:
                if symbol in alphabet_english:
                    mesto = alphabet_english.index(symbol)
                    new_mesto = mesto + offset
                    if new_mesto >= len(alphabet_english):
                        new_mesto %= len(alphabet_english)
                    resultStr += alphabet_english[new_mesto]
                else:
                    resultStr += symbol
        else:
            return False, 0
        return True, resultStr
    except Exception as ex:
        print(ex)
        return False, 0


async def decrypt_with_offset(phrase, offset):
    try:
        resultStr = ""
        if phrase[0] in alphabet_russian:
            for symbol in phrase:
                if symbol in alphabet_russian:
                    mesto = alphabet_russian.index(symbol)
                    new_mesto = mesto - offset
                    resultStr += alphabet_russian[new_mesto]
                else:
                    resultStr += symbol
        elif phrase[0] in alphabet_english:
            for symbol in phrase:
                if symbol in alphabet_english:
                    mesto = alphabet_english.index(symbol)
                    new_mesto = mesto - offset
                    resultStr += alphabet_english[new_mesto]
                else:
                    resultStr += symbol
        else:
            return False, 0
        print(resultStr)
        return True, resultStr
    except Exception as ex:
        print(ex)
        return False, 0


def crypt_gamma(text, gamma):
    text = text.lower()
    gamma = gamma.lower()
    textLen = len(text)
    gammaLen = len(gamma)

    # Формируем ключевое слово(растягиваем гамму на длину текста)
    keyText = []
    for i in range(textLen // gammaLen):
        for symb in gamma:
            keyText.append(symb)
    for i in range(textLen % gammaLen):
        keyText.append(gamma[i])

    # Шифрование
    code = []
    for i in range(textLen):
        if text[i] not in alphabet_russian or keyText[i] not in alphabet_russian:
            code.append(text[i])
        else:
            code.append(alphabet_russian[(alphabet_russian.index(text[i]) + alphabet_russian.index(keyText[i])) % 33])

    return "".join(code)


def decrypt_gamma(code, gamma):
    code = code.lower()
    gamma = gamma.lower()
    codeLen = len(code)
    gammaLen = len(gamma)

    # Формируем ключевое слово(растягиваем гамму на длину текста)
    keyText = []
    for i in range(codeLen // gammaLen):
        for symb in gamma:
            keyText.append(symb)
    for i in range(codeLen % gammaLen):
        keyText.append(gamma[i])

    # Расшифровка
    text = []
    for i in range(codeLen):
        if code[i] not in alphabet_russian or keyText[i] not in alphabet_russian:
            text.append(code[i])
        else:
            text.append(alphabet_russian[(alphabet_russian.index(code[i]) - alphabet_russian.index(keyText[i]) + 33) % 33])
    return "".join(text)


def crypt_with_key_word(text, keyword):
    text = text.lower()
    keyword = keyword.lower()
    start_alphabet = f'{" ".join(alphabet_russian)}'
    alphabet_decrypt = keyword
    for i in alphabet_russian:
        if i not in alphabet_decrypt:
            alphabet_decrypt += i
    crypt_alphabet = f'{" ".join(alphabet_decrypt)}'
    result = ""
    for symbol in text:
        if symbol in alphabet_russian:
            index = alphabet_russian.index(symbol)
            result += alphabet_decrypt[index]
        else:
            result += symbol
    return start_alphabet, crypt_alphabet, result


def decrypt_with_key_word(text, keyword):
    text = text.lower()
    keyword = keyword.lower()
    start_alphabet = f'{" ".join(alphabet_russian)}'
    alphabet_crypt = keyword
    for i in alphabet_russian:
        if i not in alphabet_crypt:
            alphabet_crypt += i
    crypt_alphabet = f'{" ".join(alphabet_crypt)}'
    result = ""
    for symbol in text:
        if symbol in alphabet_russian:
            index = alphabet_crypt.index(symbol)
            result += alphabet_russian[index]
        else:
            result += symbol
    return start_alphabet, crypt_alphabet, result

