from templates.answer import answer_dict as message
from services.authService import Authorization
from django.http.multipartparser import MultiPartParser
from apps.posts.models import Post
from services.encriptionService import Encriptions


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
    try:
        Post.create_new_posts(post_data)
        return message[200]
        
    except Exception as er:
        return message[500]