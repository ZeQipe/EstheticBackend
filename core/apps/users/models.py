from templates.answer import answer_dict as message
from services.encriptionService import Encriptions
from services.parserService import Separement
from services.mediaService import Media
from django.db import models
from django.utils import timezone
import re


class User(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    user_name = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    password = models.TextField()
    avatar = models.TextField(unique=True, blank=True, null=True)
    tags_user = models.JSONField(default=list)
    subscribers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(default="active")

    @staticmethod
    def create_user(data):
        # Валидация входных данных на создание пользователя
        result_validate, message_validate = User.__validate_data(data, "create")

        if not result_validate:
            response = message[400].copy()
            response["message"] = message_validate
            return response
        
        try:
            url = Media.save_media(data["media"], data["id"], "avatars")
            User.objects.create(
                                id=data["id"],
                                first_name=data["first_name"],
                                last_name=data["last_name"],
                                user_name=data["user_name"],
                                email=data["email"],
                                password=Encriptions.encrypt_string(data["password"]),
                                avatar=url,
                                tags_user=Separement.unpacking_tags(data["tags_list"])
                                )
            
            return message[200]

        except Exception as error:
            return message[500]
        
    @staticmethod
    def change_user(user, data):
        result_validate, message_validate = User.__validate_data(data, "edit")

        if not result_validate:
            response = message[400].copy()
            response["message"] = message_validate
            return response
        
        tags = Separement.unpacking_tags(data["tags_list"])

        try:
            url = Media.save_media(data["media"], user.id, "avatars")
        
        except:
            url = False
        
        if data.get('first_name', False):
            user.first_name = data["first_name"]

        if data.get('last_name', False):
            user.last_name = data["last_name"]

        if data.get('user_name', False):
            user.user_name = data["user_name"]

        if tags:
            user.tags_user = tags

        if url:
            user.avatar = url

        user.save()
        
        return message[200]

    
    @staticmethod
    def __validate_data(data: dict, mode: str) -> tuple:
        """
        Валидация данных пользователя при создании или редактировании, включая проверку уникальности user_name и email.
        :param data: словарь с данными пользователя
        :param mode: режим, либо "create" (создание), либо "edit" (редактирование)
        :return: кортеж - булево значение результата и сообщение об ошибке
        """

        # Регулярные выражения для полей
        regex_patterns = {
            'first_name': r'^.{2,20}$',
            'last_name': r'^.{0,20}$',
            'user_name': r'^.{2,20}$',
            'email': r'^.{8,20}$',
            'password': r'^.{8,20}$'
        }
        
        # Список обязательных полей для режима "create"
        required_fields = ['first_name', 'last_name', 'user_name', 'email']
        if mode == 'create':
            required_fields.append('password')
        
        # Проверка наличия всех обязательных полей в режиме "create"
        if mode == 'create':
            for field in required_fields:
                if not data.get(field):
                    return False, f'Ошибка запроса. Поле {field} не может быть пустым при регистрации'
        
        # Итерация по полям и их валидация
        for field, value in data.items():
            # Пропуск значений None в режиме "edit"
            if mode == 'edit' and value is None:
                continue
            
            # Преобразование пустой строки для last_name в None
            if field == 'last_name' and value == '':
                data[field] = None
                continue  # Пропуск дальнейшей проверки для этого поля
            
            # Пропуск проверки password в режиме "edit"
            if mode == 'edit' and field == 'password':
                continue

            # Проверка, является ли значение строкой, и соответствует ли оно регулярному выражению
            if value and not isinstance(value, str):
                return False, f'Ошибка запроса. Поле {field} должно быть строкой'
            
            if value and not re.match(regex_patterns[field], value):
                return False, f'Ошибка запроса. Неверное значение для поля {field}'

        # Если все проверки пройдены, выполняем проверку уникальности user_name и email
        if mode == 'create':
            # Проверка уникальности user_name и email при создании
            if User.objects.filter(user_name=data['user_name']).exists():
                return False, 'Ошибка запроса. Имя пользователя уже занято'

            if User.objects.filter(email=data['email']).exists():
                return False, 'Ошибка запроса. Адрес электронной почты уже занят'
        
        if mode == 'edit' and data.get('user_name') is not None:
            # Проверка уникальности user_name при редактировании (если оно присутствует)
            if User.objects.filter(user_name=data['user_name']).exists():
                return False, 'Ошибка запроса. Имя пользователя уже занято'
        
        return True, "All data correct"
