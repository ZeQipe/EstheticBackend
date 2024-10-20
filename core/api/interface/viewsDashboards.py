from django.views.decorators.csrf import csrf_exempt
from templates.answer import answer_dict as message
from apps.dashboards.controller import *
from django.http import JsonResponse
from services.delService import DeletterObject


@csrf_exempt
def dashboards(request):
    # Создание досок
    if request.method == "POST": response = create_dashboards(request)

    # Получение досок по кукам
    elif request.method == "GET": response = get_boards_user_by_cookie(request)

    else: response = message[405]
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def post_in_boards(request):
    # Наличие поста в досках пользователя
    if request.method == "GET": response = check_post_in_boards(request)

    else: response = message[405]
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def dashboards_delete_posts(request, boardID):
    # Удаление поста из доски
    if request.method == "DELETE": response = remove_posts_in_board(request, boardID)

    else: response = message[405]
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def dashboards_list(request, userID):
    # Вернуть информацию о досках
    if request.method == "GET": response = get_user_dashboards(request, userID)

    else: response = message[405]
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def dashboards_param(request, boardID):
    # Вернуть детализированную информацию о доске
    if request.method == "GET": response = get_dashboard_detail(request, boardID)                               

    # Добавить пост в доску
    elif request.method == "POST": response = add_post_in_board(request, boardID)                               

    # Удаление доски
    elif request.method == "DELETE": response = DeletterObject.del_object(request, Board, boardID)              

    else: response = message[405]
    return JsonResponse(response, status=response.get("status", 200))
