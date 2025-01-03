from templates.answer import answer_dict as message
from django.http import JsonResponse
from apps.comments.controller import *
from django.views.decorators.csrf import csrf_exempt
from services.delService import DeletterObject
from services.logService import LogException


@csrf_exempt
def comments(request, ID):
    # Создание комментария
    if request.method == "POST": response = create_comments(request, ID)

    # Получение комментариев
    elif request.method == "GET": response = get_comments(request, ID)

    # Удаление комментария
    elif request.method == "DELETE": response = DeletterObject.del_object(request, Comments, ID)

    # Редактирование комментариев
    elif request.method == "PUT": response = edit_comments(request, ID)

    else: 
        LogException.write_data("Не существующий метод", "23", "viewsComments", "Не верный метод", "comments", "info", 
                                request, "comments/<str:ID>", f"запрос с методом - {request.method}", "405")
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def toggle_like(request, commentID):
    # Лайк комментария
    if request.method == "PUT": response = change_like(request, commentID)

    else: 
        LogException.write_data("Не существующий метод", "36", "viewsComments", "Не верный метод", "toggle_like", "info", 
                                request, "comments/toggle-like/<str:commentID>", f"запрос с методом - {request.method}", "405")
        response = message[405]

    return JsonResponse(response, status=response.get("status", 200))