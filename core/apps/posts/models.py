from templates.answer import answer_dict as message
from django.db import models
from apps.users.models import User
from django.utils import timezone
from services.parserService import Separement
from services.mediaService import Media
import re


class Post(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    post_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True, null=True)
    users_liked = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    type_content = models.TextField()
    url = models.TextField(unique=True)
    tags_list = models.JSONField(default=list)
    aspect_ratio = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    @staticmethod
    def create_post(data):
        result_validate, message_validate = Post.__validate_data(data, "create")

        if not result_validate:
            response = message[400].copy()
            response["message"] = message_validate
            return response
 
        url = Media.save_media(data["file"], data["id"], folder="content")
        if not url: return message["204"] 

        type_content = "img" if url[-1] == "p" else "video" 

        post = Post.objects.create(
                        id=data["id"],  # ID поста
                        author=data["author"],  # ID автора поста
                        post_name=data["postName"],  # Название поста
                        description=data["description"],  # Описание поста
                        type_content=type_content,  # Тип поста
                        url=url,  # URL файла на сервере
                        tags_list=Separement.unpacking_tags(data["tags"]), # Список комментариев
                        aspect_ratio=data["aspectRatio"], # параметр, которые передается с фронта
                        link=data["link"] # Ссылка для сохранения
                        )

        return {"postId": post.id}


    @staticmethod
    def get_posts(tags_user, offset, limit):
        pass    

    
    @staticmethod
    def __validate_data(post_data: dict, mode: str) -> tuple:
        """
        Валидация данных поста при создании или редактировании.
        :param post_data: словарь с данными поста
        :param mode: режим, либо "create" (создание), либо "edit" (редактирование)
        :return: кортеж - булево значение результата и сообщение об ошибке
        """
        # Поля, которые необходимо валидировать
        fields_to_validate = ['postName', 'description', 'aspectRatio', 'link']

        # Регулярные выражения для полей
        regex_patterns = {
            'postName': r'^.{2,20}$',  # Название поста от 2 до 20 символов
            'description': r'^.{0,100}$',  # Описание до 100 символов (может быть пустым)
            'aspectRatio': r'^.*$',  # Любая строка
            'link': r'^.{0,100}$'  # Ссылка до 100 символов
        }

        # Список обязательных полей для режима "create"
        required_fields = ['postName', 'aspectRatio']
        
        # Фильтрация данных — оставляем только те, которые нужно валидировать
        filtered_data = {field: post_data.get(field) for field in fields_to_validate}

        # Проверка наличия всех обязательных полей в режиме "create"
        if mode == 'create':
            for field in required_fields:
                if not filtered_data.get(field):
                    return False, f'Ошибка запроса. Поле {field} не может быть пустым при создании поста'

        # Итерация по полям и их валидация
        for field, value in filtered_data.items():
            # Пропуск значений None в режиме "edit"
            if mode == 'edit' and value is None:
                continue

            # Преобразование пустой строки для description в None
            if field == 'description' and value == '':
                filtered_data[field] = None
                continue  # Пропуск дальнейшей проверки для этого поля

            # Проверка, является ли значение строкой
            if value and not isinstance(value, str):
                return False, f'Ошибка запроса. Поле {field} должно быть строкой'

            # Проверка соответствия регулярному выражению
            if value and not re.match(regex_patterns[field], value):
                return False, f'Ошибка запроса. Неверное значение для поля {field}'

        return True, "Все данные корректны"