from templates.answer import answer_dict as message
from django.db import models
from apps.users.models import User
from django.utils import timezone
from services.parserService import Separement
from services.mediaService import Media
from django.db.models import Q
import re


class Post(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    post_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True, null=True)
    users_liked = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    type_content = models.TextField()
    url = models.TextField(unique=True)
    url_blur = models.TextField(unique=True)
    tags_list = models.JSONField(default=list)
    aspect_ratio = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=timezone.now)


    @staticmethod
    def create_post(data):
        # Валидация данных
        result_validate, message_validate = Post.__validate_data(data, "create")
        if not result_validate:
            response = message[400].copy()
            response["message"] = message_validate
            return response
 
        # Сохранение медиа файла
        url, url_blur = Media.save_media(data["file"], data["id"], folder="content")
        if not url: return message["204"]
        type_content = "img" if url[-1] == "p" else "video"

        # Создание поста
        post = Post.objects.create(id=data["id"],
                                   author=data["author"],
                                   post_name=data["postName"],
                                   description=data["description"],
                                   type_content=type_content,
                                   url=url,
                                   url_blur=url_blur,
                                   tags_list=Separement.unpacking_tags(data["tags"]),
                                   aspect_ratio=data["aspectRatio"],
                                   link=data["link"])

        return {"postId": post.id}


    @staticmethod
    def change_data_post(post, data):
        # Валидация данных
        result_validate, message_validate = Post.__validate_data(data, "edit")
        if not result_validate:
            response = message[400].copy()
            response["message"] = message_validate
            return response

        # Установка новых данных
        if data["postName"]: post.name = data["postName"]
        if data["description"]: post.description = data["description"]
        if data["link"]: post.link = data["link"]
        if data["aspectRatio"]: post.aspect_ratio = data["aspectRatio"]

        # Подготовка и установка новых тэгов
        tags = Separement.unpacking_tags(data["tags_list"])
        if tags: post.tags_list = tags

        # Сохранение результата
        post.save()
        return message[200]


    @staticmethod
    def get_posts(user_tags: list, offset=0, limit=20) -> list:
        # Приведение тегов пользователя к нижнему регистру
        user_tags_normalized = [tag.lower() for tag in user_tags]

        # Всего постов в базе
        total_posts_count = Post.objects.all().count()

        # Режим 1: Если нет тегов, возвращаем посты от новых к старым
        if not user_tags_normalized:
            return Post._get_posts_without_tags(offset, limit, total_posts_count)

        # Режим 2: Если есть теги, ищем по тегам
        posts_by_tags = Post._get_posts_by_tags(user_tags_normalized, offset, limit)

        # Режим 3: Если offset больше количества постов — замкнутый круг
        if offset >= total_posts_count:
            return Post._get_posts_with_loop(offset, limit, total_posts_count)

        return posts_by_tags

    @staticmethod
    def _get_posts_without_tags(offset: int, limit: int, total_posts_count: int) -> list:
        # Замкнутый круг, если offset больше количества постов
        if offset >= total_posts_count:
            offset = offset % total_posts_count

        posts = Post.objects.order_by('-created_at')[offset:offset+limit]
        return list(posts)

    @staticmethod
    def _get_posts_by_tags(user_tags: list, offset: int, limit: int) -> list:
        # 1. Точное совпадение тегов
        exact_match = Q()
        for tag in user_tags:
            exact_match |= Q(tags_list__icontains=tag)

        exact_posts = Post.objects.filter(exact_match).distinct().order_by('-created_at')

        # Пропуск постов по offset
        exact_post_count = exact_posts.count()

        if exact_post_count >= offset + limit:
            # Если точных постов достаточно, просто возвращаем их с учетом offset и limit
            return list(exact_posts[offset:offset+limit])

        # Если точных постов недостаточно, включаем их все
        result_posts = list(exact_posts[offset:])

        # Уменьшаем offset на количество уже взятых точных совпадений
        offset -= min(exact_post_count, offset)

        # 2. Частичное совпадение тегов
        partial_match = Q()
        for tag in user_tags:
            partial_match |= Q(tags_list__icontains=tag[:len(tag) // 2])

        partial_posts = Post.objects.filter(partial_match).exclude(id__in=exact_posts).distinct().order_by('-created_at')
        partial_post_count = partial_posts.count()

        # Пропуск постов по offset для частичных совпадений
        if partial_post_count >= offset:
            result_posts.extend(list(partial_posts[offset:offset+limit-len(result_posts)]))
        else:
            # Если частичных постов тоже недостаточно, берем все оставшиеся
            result_posts.extend(list(partial_posts[offset:]))

        # 3. Если все еще не набрали достаточно постов, добираем случайные посты
        if len(result_posts) < limit:
            remaining_limit = limit - len(result_posts)
            random_posts = Post.objects.exclude(id__in=[post.id for post in result_posts]).order_by('?')[:remaining_limit]
            result_posts.extend(list(random_posts))

        # Применяем limit ко всем найденным постам
        return result_posts[:limit]

    @staticmethod
    def _get_posts_with_loop(offset: int, limit: int, total_posts_count: int) -> list:
        # Рассчитываем новый offset для замкнутого круга
        offset = offset % total_posts_count

        posts = Post.objects.order_by('-created_at')

        # Берем посты, начиная с пересчитанного offset
        first_batch = list(posts[offset:offset + limit])

        # Если этого недостаточно, берем посты с начала списка
        remaining_limit = limit - len(first_batch)
        if remaining_limit > 0:
            second_batch = list(posts[:remaining_limit])
            return first_batch + second_batch

        return first_batch


    @staticmethod
    def __validate_data(post_data: dict, mode: str) -> tuple:
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
