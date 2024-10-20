import os
from pathlib import Path
from PIL import Image
from datetime import datetime
from services.encriptionService import Encriptions
from django.conf import settings

class Media:
    HOSTNAME = "http://localhost:8000"

    # Константы для допустимых расширений
    ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']
    ALLOWED_VIDEO_EXTENSIONS = ['mp4', 'mov', 'avi', 'mkv']

    @classmethod
    def save_media(cls, file, user_id: int, folder: str = 'avatars') -> str:
        """
        Сохранение медиа файла (изображения или видео)
        :param file: файл, переданный через MultiPartParser
        :param user_id: ID пользователя, для создания уникального имени файла
        :param folder: папка для сохранения файла ('avatars', 'content' и т.д.)
        :return: Относительный путь сохранённого файла или None, если файл пустой
        """
        if not file:
            return

        file_extension = file.name.split('.')[-1].lower()

        if file_extension in cls.ALLOWED_IMAGE_EXTENSIONS:
            # Обрабатываем изображение
            file_name = f'{user_id}{Encriptions.generate_string(4, False)}.webp'
            save_path = os.path.join(settings.MEDIA_ROOT, 'webp', folder, file_name)

            # Создаём директорию, если её нет
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Сжимаем изображение и сохраняем в формате webp 
            with Image.open(file) as img:
                img.save(save_path, format='webp', quality=90)

            # Возвращаем относительный путь к файлу
            relative_path = os.path.join('webp', folder, file_name)

            return relative_path

        elif file_extension in cls.ALLOWED_VIDEO_EXTENSIONS:
            # Заглушка для видео
            return {'message':'Video processing is not implemented yet.'}
        else:
            raise ValueError('Неподдерживаемый тип файла') 


    @classmethod
    def get_full_url(cls, path: str) -> str:
        """
        Возврат полного URL к файлу по относительному пути.
        :param path: Относительный путь к файлу
        :return: Полный URL
        """
        return f"{cls.HOSTNAME}{settings.MEDIA_URL}{path}"


    @staticmethod
    def get_file_path_from_relative(relative_path: str) -> str:
        """
        Возврат физического пути по относительному пути, который хранится в БД.
        :param relative_path: Относительный путь к файлу
        :return: Физический путь к файлу
        """
        return os.path.join(settings.MEDIA_ROOT, relative_path)


    @staticmethod
    def file_exists(file_path: str) -> bool:
        """
        Проверка существования файла
        :param file_path: Путь к файлу
        :return: True, если файл существует, иначе False
        """
        return os.path.exists(file_path)


    @staticmethod
    def get_file_info(relative_path: str) -> dict:
        """
        Возврат информации о файле
        :param relative_path: Относительный путь к файлу
        :return: Словарь с информацией о файле
        """
        file_path = Media.get_file_path_from_relative(relative_path)

        if not os.path.exists(file_path):
            return {'message': 'Файл не найден'}

        file_info = os.stat(file_path)
        file_name = os.path.basename(file_path)
        file_size_mb = round(file_info.st_size / (1024 * 1024), 2)  # Размер в МБ
        file_type = 'webp' if file_name.endswith('webp') else 'webm'  # Проверка типа файла
        date_created = datetime.fromtimestamp(file_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')

        # Для изображений получаем пропорции
        try:
            with Image.open(file_path) as img:
                width, height = img.size
        except IOError:
            width, height = 'N/A', 'N/A'  # Для видео или других файлов

        return {
            'path': file_path,
            'url': Media.get_full_url(relative_path),
            'size': f'{file_size_mb} MB',
            'type': file_type,
            'name': file_name,
            'date_create': date_created,
            'proportions': f'{width}x{height}' if width != 'N/A' else 'N/A'
        }
