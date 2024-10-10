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
    subscribers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    @staticmethod
    def create_user(data):
        pass

    
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
