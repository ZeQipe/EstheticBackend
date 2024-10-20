from templates.answer import answer_dict as message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from apps.users.controller import *
from services.authService import Authorization
from services.delService import DeletterObject as deletter


@csrf_exempt
@require_http_methods(["POST"])
def usersRegistration(request):
    # Создание нового пользователя
    if request.method == "POST": response = registration_users(request)

    else: response = message[405]
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
@require_http_methods(["POST"])
def usersLogin(request):
    # Авторизация пользователя
    if request.method == "POST":
        response = Authorization.login(request)

        if response.get("userId", False):
            cook_keys = Encriptions.encrypt_string(response.get("userId"))
            response = JsonResponse(response, status=200)
            response = Authorization.set_key_in_coockies(response, cook_keys)

        else:
            response = JsonResponse(response, status=response.get("status"))

    else: response = JsonResponse(message[405], status=405)

    return response


@csrf_exempt
@require_http_methods(["POST"])
def usersLogout(request):
    # Выход из аккаунта
    if request.method == "POST":
        user = Authorization.is_authorization(request)
        if isinstance(user, dict):
            response = JsonResponse(message[401], status=401)

        else:
            response = JsonResponse(message[200], status=200)
            response.delete_cookie("auth_key")

    else: response = JsonResponse(message[405], status=405)

    return response


@csrf_exempt
def privateProfile(request):
    # Вернуть профиль по кукам
    if request.method == "GET": response = user_profile(request)

    else: response = message[405]
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def publicProfile(request, userID):
    # Вернуть профиль по ID
    if request.method == "GET":response = user_profile(request, userID)                             

    else: response = message[405]
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def users(request):
    # Удалить пользователя
    if request.method == "DELETE": response = deletter.del_object(request, User)

    # Изменить данные о пользователе
    elif request.method == "PUT": response = edit_user_data(request)

    else: response = message[405]
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def usersCreatedPosts(request, userID):
    # Вернуть список постов пользователя
    if request.method == "GET": response = user_created_post_list(request, userID)

    else: response = message[405]
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def check_auth(request):
    # Проверка авторизации пользователя
    if request.method == "GET": response = {"isAuth": not isinstance(Authorization.is_authorization(request), dict)}

    else: response = message[405]
    return JsonResponse(response, status=response.get("status", 200))
