from aiogram.types import InputMediaPhoto


def links_images(dict_links):
    """Функция получения списка ссылок фотографий объявления для отправки нескольких фотографий в одном сообщении
    при нажатии кнопки 'Больше фото' в клавиатуре под фото"""
    media = []
    for num_photo, dict_urls in enumerate(dict_links):
        if num_photo != 0:
            for key, i_url in dict_urls.items():
                media.append(InputMediaPhoto(media=i_url))
    return media

