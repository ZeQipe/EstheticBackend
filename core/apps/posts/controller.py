from templates.answer import answer_dict as message
from services.authService import Authorization
from django.http.multipartparser import MultiPartParser
from apps.posts.models import Post
from services.encriptionService import Encriptions
from services.parserService import Separement


def create_post(request):
    # Поиск автора поста
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]

    # Формируем информацию о файле
    data = MultiPartParser(request.META, request, request.upload_handlers).parse()
    post_data = {
                "id": Encriptions.generate_string(35, Post),
                "author": cookie_user,
                "postName": data[0].get("name"),
                "description": data[0].get("description"),
                "link": data[0].get("link"),
                "aspectRatio": data[0].get("aspectRatio"),
                "tags": data[0].get("tags"),
                "file": data[1].get("file")
                }

    # Отправляем в базу все данные
    try: return Post.create_post(post_data) 
    
    except Exception: return message[500]


def search_posts(request):
    """
    Обрабатывает запрос на получение постов учитывая теги пользователя.
    """
    # Получаем query параметры offset и limit из запроса и пытаемся привести их к int.
    offset, limit = Separement.pagination_parametrs(request)

    # Поиск автора поста через auth_key из cookies
    cookie_user = Authorization.is_authorization(request)
    
    if isinstance(cookie_user, dict): tags_user = []
    else: tags_user = cookie_user.tags_user
    
    # Получаем посты из базы данных с учетом тегов, offset и limit
    try: result = Post.get_posts(tags_user, offset, limit)
    except Exception as er: 
        response = message[500].copy()
        response["er"] = f"{er}"
        return response

    if not result: return message[404]

    # Форматирование постов
    response = Separement.formatted_posts(result, Post.objects.all().count())
    return response


def toggle_like(request, postID):
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]
    
    try: post = Post.objects.get(id=postID)
    except Exception: return message[404]
    
    if post.users_liked.filter(id=cookie_user.id).exists():
        post.users_liked.remove(cookie_user)
    else:
        post.users_liked.add(cookie_user)
        
    return message[200]


def get_post_by_id(request, post_id):
    cookie_user = Authorization.is_authorization(request)
    
    try: post = Post.objects.get(id=post_id)
    except Exception: return message[404]
    
    return Separement.detail_info_post(post, cookie_user)