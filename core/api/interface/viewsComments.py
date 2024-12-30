from templates.answer import answer_dict as message
from django.http import JsonResponse
from apps.comments.controller import *
from django.views.decorators.csrf import csrf_exempt
from services.delService import DeletterObject


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

    else: response = message[405]
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def toggle_like(request, commentID):
    # Лайк комментария
    if request.method == "PUT": response = change_like(request, commentID)

    else: response = message[405]
    return JsonResponse(response, status=response.get("status", 200))