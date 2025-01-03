from templates.answer import answer_dict as message
from services.authService import Authorization
from django.http.multipartparser import MultiPartParser
from apps.posts.models import Post
from services.encriptionService import Encriptions
from services.parserService import Separement
from services.logService import LogException


def create_post(request):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка создать пост без авторизации", "13", "posts -- controller", 
                        "Ошибка авторизации", "create_post", "info", request, "posts/", "POST", "401")
        
        return message[401]

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
    try: 
        return Post.create_post(post_data)
    
    except Exception as er:
        LogException.write_data(er, "31", "posts -- controller", "Ошибка при обращении к модели", 
                    "create_post", "warning", f"post_data: {post_data}", "posts/", "POST", "500")
        
        return message[500]


def edit_post_by_id(request, post_id):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка отредактировать пост без авторизации", "44", "posts -- controller", 
                "Ошибка авторизации", "edit_post_by_id", "info", request, "posts/<str:postID>", "PUT", "401")
        
        return message[401]

    # Ищем пост, который необходимо изменить
    try: 
        post = Post.objects.get(id=post_id)
    
    except Exception as er: 
        LogException.write_data(er, "51", "posts -- controller", "Ошибка при обращении к базе данных", 
                "edit_post_by_id", "warning", f"post_id: {post_id}", "posts/<str:postID>", "PUT", "404")
        
        return message[404]

    # Проверка на то, что запрос выполнил автор
    if cookie_user.id != post.author.id: 
        LogException.write_data("Попытка редактирование не своего поста", "61", "posts -- controller", 
            "Ошибка доступа", "edit_post_by_id", "info", f"cookie_user_id: {cookie_user.id} -- post_author_id: {post.author.id}", 
            "posts/<str:postID>", "PUT", "403")
        
        return message[403]

    # Формируем информацию о посте
    data = MultiPartParser(request.META, request, request.upload_handlers).parse()
    post_data = {"postName" : data[0].get("name"),
              "description" : data[0].get("description"),
                     "link" : data[0].get("link"),
              "aspectRatio" : data[0].get("aspectRatio"),
                "tags_list" : data[0].get("tag")}

    # Отправляем в базу данных запрос
    try: 
        return Post.change_data_post(post, post_data)
    
    except Exception as er: 
        LogException.write_data(er, "77", "posts -- controller", "Ошибка при обращении модели", 
            "edit_post_by_id", "warning", f"post_data: {post_data}", "posts/<str:postID>", "PUT", "500")
        
        return message[500]


def search_posts(request):
    # Получаем query параметры offset и limit из запроса
    offset, limit = Separement.pagination_parametrs(request)

    # Формирование тэгов для выборки постов
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): tags_user = []
    else: tags_user = cookie_user.tags_user

    # Получаем посты из базы данных с учетом тегов, offset и limit
    try: 
        result = Post.get_posts(tags_user, offset, limit)
    
    except Exception as er: 
        LogException.write_data(er, "97", "posts -- controller", "Ошибка при обращении к модели", "search_posts", 
                    "warning", f"tags: {tags_user} -- offset: {offset} -- limit {limit}", "posts/", "GET", "500")

        return message[500]

    # Формирование ответа с помощью парсера
    try:
        response = Separement.formatted_posts(result, Post.objects.all().count())

    except Exception as er:
        LogException.write_data(er, "107", "posts -- controller", "Ошибка при формировании ответа", 
                            "search_posts", "warning", f"result: {result}", "posts/", "GET", "500")
        
        return message[500]

    return response


def toggle_like(request, postID):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка поставить лайк без авторизации", "122", "posts -- controller", 
            "Ошибка авторизации", "toggle_like", "info", request, "posts/toggle-like/<str:ID>", "PUT", "401")
        
        return message[401]

    # Поиск поста в базе данных
    try: 
        post = Post.objects.get(id=postID)

    except Exception as er: 
        LogException.write_data(er, "128", "posts -- controller", "Ошибка при обращении к базе данных", 
            "toggle_like", "warning", f"postID: {postID}", "posts/toggle-like/<str:ID>", "PUT", "404")
        
        return message[404]
    try:
        # Установка или удаление лайка
        if post.users_liked.filter(id=cookie_user.id).exists():
            post.users_liked.remove(cookie_user)

        else:
            post.users_liked.add(cookie_user)

    except Exception as er:
        LogException.write_data(er, "136", "posts -- controller", "Ошибка при обращении к базе данных", 
                "toggle_like", "warning", f"postID: {postID}", "posts/toggle-like/<str:ID>", "PUT", "404")

    return message[200]


def get_post_by_id(request, post_id):
    # Поиск пользователя в базе данных по кукам
    cookie_user = Authorization.is_authorization(request)

    # Поиск поста в базе данных
    try: 
        post = Post.objects.get(id=post_id)
    
    except Exception: 
        LogException.write_data(er, "156", "controller -- posts", "Ошибка при обращении к базе данных", 
                "get_post_by_id", "warning", f"post_id: {post_id}", "posts/<str:postID>", "GET", "404")
        
        return message[404]

    # Формирование ответа с помощью парсера
    try:
        response = Separement.detail_info_post(post, cookie_user)
    
    except Exception as er:
        LogException.write_data(er, "166", "controller -- posts", "Ошибка при формировании ответа", 
                    "get_post_by_id", "warning", f"post: {post}", "posts/<str:postID>", "GET", "500")
        
        return message[500]
    
    return response
