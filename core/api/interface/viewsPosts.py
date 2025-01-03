from templates.answer import answer_dict as message
from django.http import JsonResponse
from apps.posts.controller import *
from django.views.decorators.csrf import csrf_exempt
from services.delService import DeletterObject
from services.logService import LogException


@csrf_exempt
def posts(request):
    # Создание поста
    if request.method == "POST": response = create_post(request)

    # Вернуть посты по тэгам
    elif request.method == "GET": response = search_posts(request)

    else: 
        LogException.write_data("Не существующий метод", "17", "viewsPosts", "Не верный метод", "posts", "info", 
                                    request, "posts/", f"запрос с методом - {request.method}", "405")
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def posts_toggle_like(request, postID):
    # Установка лайка посту
    if request.method == "PUT": response = toggle_like(request, postID)

    else: 
        LogException.write_data("Не существующий метод", "30", "viewsPosts", "Не верный метод", "posts_toggle_like", "info", 
                                    request, "posts/toggle-like/<str:ID>", f"запрос с методом - {request.method}", "405")
        response = message[405]

    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def posts_param(request, postID):
    # Вернуть детализированную информацию поста
    if request.method == "GET": response = get_post_by_id(request, postID)

    # Удалить пост
    elif request.method == "DELETE": response = DeletterObject.del_object(request, Post, postID)

    # Изменить данные о посте
    elif request.method == "PUT": response = edit_post_by_id(request, postID)

    else: 
        LogException.write_data("Не существующий метод", "49", "viewsPosts", "Не верный метод", "posts_param", "info", 
                                    request, "posts/<str:postID>", f"запрос с методом - {request.method}", "405")
        response = message[405]

    return JsonResponse(response, status=response.get("status", 200))
