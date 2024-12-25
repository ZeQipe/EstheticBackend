from templates.answer import answer_dict as message
from services.authService import Authorization
from django.http.multipartparser import MultiPartParser
from apps.posts.models import Post
from services.encriptionService import Encriptions
from services.parserService import Separement


def create_post(request):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]

    # Формируем информацию о посте
    data = MultiPartParser(request.META, request, request.upload_handlers).parse()
    post_data = {"id" : Encriptions.generate_string(35, Post),
             "author" : cookie_user,
           "postName" : data[0].get("name"),
        "description" : data[0].get("description"),
               "link" : data[0].get("link"),
        "aspectRatio" : data[0].get("aspectRatio"),
               "tags" : data[0].get("tags"),
               "file" : data[1].get("file")}

    # Отправляем в базу данных запрос
    try: return Post.create_post(post_data)
    except Exception: return message[500]


def edit_post_by_id(request, post_id):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]

    # Ищем пост, который необходимо изменить
    try: post = Post.objects.get(id=post_id)
    except: return message[404]

    # Проверка на то, что запрос выполнил автор
    if cookie_user.id != post.author.id: return message[403]

    # Формируем информацию о посте
    data = MultiPartParser(request.META, request, request.upload_handlers).parse()
    post_data = {"postName" : data[0].get("name"),
              "description" : data[0].get("description"),
                     "link" : data[0].get("link"),
              "aspectRatio" : data[0].get("aspectRatio"),
                "tags_list" : data[0].get("tag")}

    # Отправляем в базу данных запрос
    try: return Post.change_data_post(post, post_data)
    except Exception: return message[500]


def search_posts(request):
    # Получаем query параметры offset и limit из запроса
    offset, limit = Separement.pagination_parametrs(request)

    # Формирование тэгов для выборки постов
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): tags_user = []
    else: tags_user = cookie_user.tags_user

    # Получаем посты из базы данных с учетом тегов, offset и limit
    try: result = Post.get_posts(tags_user, offset, limit)
    except Exception: return message[500]

    # Формирование ответа с помощью парсера
    response = Separement.formatted_posts(result, Post.objects.all().count())
    return response


def toggle_like(request, postID):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]

    # Поиск поста в базе данных
    try: post = Post.objects.get(id=postID)
    except Exception: return message[404]

    # Установка или удаление лайка
    if post.users_liked.filter(id=cookie_user.id).exists():
        post.users_liked.remove(cookie_user)
    else:
        post.users_liked.add(cookie_user)

    return message[200]


def get_post_by_id(request, post_id):
    # Поиск пользователя в базе данных по кукам
    cookie_user = Authorization.is_authorization(request)

    # Поиск поста в базе данных
    try: post = Post.objects.get(id=post_id)
    except Exception: return message[404]

    # Формирование ответа с помощью парсера
    response = Separement.detail_info_post(post, cookie_user)
    return response
