"""Cловарь кнопок"""


menu_inline: dict[str, str] = {
    'next': "Следующее",
    'settings': "Изменить настройки",
    "support": "Поддержка",
    "about": "О боте"
}

"""Кнопки для клавиатуры с выбором района города"""
district_choose_inline: dict[str, str] = {
    "district_sov": "Советский",
    "district_okt": "Октябрьский",
    "district_zhel": "Железнодорожный",
}

"""Категория недвижимости"""
category_ned_inline: dict[str: str] = {
    "apartment": "Квартира",
    "room": "Комната",
    "house": "Частный дом",
}

"""Кнопки для клавиатуры с выбором количества комнат"""
rooms_inline: dict[str, str] = {
    "/Студия": "Студия",
    "/1": "1",
    "/2": "2",
    "/3": "3",
    "/4+": "4+"
}

"""Клавиатура для измненения настроек поиска"""
first_keyboard: dict[str, str] = {"/settings": "Настройки поиска"}

again_keyboard: dict[str, str] = {
    "/settings": "Настройки поиска",
    "/run": "Поиск"
}

"""Кнопка для свайпа значений по заданным параметрам"""
swipe: dict[str, str] = {"/run": "Следующее"}

"""Стартовая кнопка"""
first: dict[str, str] = {"/start_s_a": "Начать поиск квартиры"}

"""Кнопка возвращающая в предыдущее состояние к указанию предыдущих параметров"""
back: dict[str, str] = {"/back": "Назад"}

"""Кнопка для показа дополнительных фотографий"""
adv_buttons: dict[str, str] = {
    "/favorite": "В избранное",
    "/delete": "Удалить",
    "/more": "Больше фото",
    "/next_apart": "Еще вариант",
}

adv_buttons_without_del: dict[str, str] = {
    "/not_favorite": "Нравится❤️️️️️️️",
    "/more": "Больше фото",
}

"""Текст для автоматической ежедневной рассылки"""
time_adv: dict[str, str] = {'adv': 'Вот еще один вариант'}


"""Текст перед стартом использования бота"""
wellcome_text: str = ("Привет, {name}! Ты готов начать поиск? Ответь на несколько вопросов "
                      "и я помогу найти тебе квартиру, которую ты ищешь!")


text_for_not_start: dict[int: str] = {
                                      1: "Вперед!",
                                      2: "Начнем!",
                                      3: "Время искать!",
                                      4: "Где хочешь квартирку?",
                                      5: "Старт!",
                                      6: "Не волнуйся, я тебе помогу!",
                                      7: "Просто следуй подсказкам"
}

stick_in_edit_settings: dict[int: str] = {
    1: "CAACAgIAAxkBAAEK0AtlYPJZhBjqi0EaiauFLauJiekDBwACMAcAAoVBMhDmsLY11jzEZzME",
    2: "CAACAgIAAxkBAAEK0A1lYPJ6d9VCYn2QuNOdZV3n02W8JAACQREAAgNOCUp9w1-UJunSCTME",
    3: "CAACAgEAAxkBAAEK0A9lYPKP96XT_zr_Ai7CtVHoh2SOGwACHgEAAjgOghFGWGjXaYZe_TME",
    4: "CAACAgIAAxkBAAEK0BFlYPK2DIyMdL4EH_fPK7d_UJ4dPwACKwADWbv8JTA6_WvNgxy4MwQ",
    5: "CAACAgIAAxkBAAEK0BNlYPLa6m1MH8hoL3PjvxLVmCVmmwACKwADJHFiGpequ5SBPPClMwQ",
    6: "CAACAgIAAxkBAAEK0BVlYPMCuYv58y9yGb35mBNyf-59YQAChQADRA3PFzdmUZzeSj1jMwQ",
    7: "CAACAgIAAxkBAAEK0BdlYPMmwazECbC16lqww7vDFMXcHgACBwMAAm2wQgOH2UxeXDz3sDME",
    8: "CAACAgIAAxkBAAEK0BllYPNkZkYVCo-D356pwS9oxdnZQwACHQADlp-MDsxKEexy5xsWMwQ",
    9: "CAACAgIAAxkBAAEKz8llYNxyGtLd6-gd6w7EC7ACf3r0nQACHwkAAhhC7ggXmAaO-z88ZjME"
}


"""Кнопки для редактирования параметров поиска"""
params_inline: dict[str, str] = {
    "/metro": "Район",
    "/low_price": "Нижняя граница",
    "/high_price": "Верхняя граница",
    "/rooms": "Количество комнат",
    "/user_settings": "Мои настройки",
    "/run": "Начать поиск"
}


all_buttons: dict[str, str] = {

    "/favorite": "В избранное",
    "/delete": "Удалить",
    "/next_apart": "Еще вариант",
    "/not_favorite": "Нравится❤️️️️️️️",
    "/more": "Больше фото",

    'next': "Следующее",
    'settings': "Изменить настройки",
    "support": "Поддержка",
    "about": "О боте",

    "district_sov": "Советский",
    "district_okt": "Октябрьский",
    "district_zhel": "Железнодорожный",

    "apartment": "Квартира",
    "room": "Комната",
    "house": "Частный дом",

    "/Студия": "Студия",
    "/1": "1",
    "/2": "2",
    "/3": "3",
    "/4+": "4+",

    "/settings": "Настройки поиска",
    "/next": "Следующее",
    "/start_s_a": "Начать поиск квартиры",
    "/back": "Назад",
    'adv': 'Вот еще один вариант',

    "/metro": "Район",
    "/low_price": "Нижняя граница",
    "/high_price": "Верхняя граница",
    "/rooms": "Количество комнат",
    "/run": "Начать поиск"
}
