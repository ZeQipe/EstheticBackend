from templates.answer import answer_dict as message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from apps.users.controller import *
from services.authService import Authorization
from services.delService import DeletterObject as deletter
from services.logService import LogException


@csrf_exempt
@require_http_methods(["POST"])
def usersRegistration(request):
    # Создание нового пользователя
    if request.method == "POST": response = registration_users(request)

    else: 
        response = message[405]
        LogException.write_data("Не существующий метод", "17", "viewsUsers", "Не верный метод", "usersRegistration", "info", request,
                                "users/registration", f"запрос с методом - {request.method}", "405")
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
@require_http_methods(["POST"])
def usersLogin(request):
    # Авторизация пользователя
    if request.method == "POST":
        response = Authorization.login(request)
        
        if response.get("userId", False): # Установка кук, в случае, если авторизация прошла успешно
            cook_keys = Encriptions.encrypt_string(response.get("userId"))
            response = JsonResponse(response, status=200)
            response = Authorization.set_key_in_coockies(response, cook_keys)

        else:
            response = JsonResponse(response, status=response.get("status"))

    else: 
        response = JsonResponse(message[405], status=405)
        LogException.write_data("Не существующий метод", "40", "viewsUsers", "Не верный метод", "usersLogin", "info", request,
                                "users/login", f"запрос с методом - {request.method}", "405")

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
            response = JsonResponse(message[200], status=200) # Удаление кук, если пользователь авторизован
            response.set_cookie(key='auth_key',
                                value="cookie_key",
                                httponly=True,
                                secure=True,
                                samesite='None',
                                max_age=1)

    else: 
        response = JsonResponse(message[405], status=405)
        LogException.write_data("Не существующий метод", "66", "viewsUsers", "Не верный метод", "usersLogout", "info", request,
                                "users/logout", f"запрос с методом - {request.method}", "405")

    return response


@csrf_exempt
def privateProfile(request):
    # Вернуть профиль по кукам
    if request.method == "GET": response = user_profile(request)

    else: 
        response = message[405]
        LogException.write_data("Не существующий метод", "79", "viewsUsers", "Не верный метод", "privateProfile", "info", request,
                                "users/private-profile", f"запрос с методом - {request.method}", "405")
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def publicProfile(request, userID):
    # Вернуть профиль по ID пользователя
    if request.method == "GET": response = user_profile(request, userID)                             

    else: 
        response = message[405]
        LogException.write_data("Не существующий метод", "92", "viewsUsers", "Не верный метод", "publicProfile", "info", request,
                                "users/public-profile/<str:userID>", f"запрос с методом - {request.method}", "405")

    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def users(request):
    # Удалить пользователя
    if request.method == "DELETE": response = deletter.del_object(request, User)

    # Изменить данные о пользователе
    elif request.method == "PUT": response = edit_user_data(request)

    else: 
        response = message[405]
        LogException.write_data("Не существующий метод", "108", "viewsUsers", "Не верный метод", "publicProfile", "info", request,
                                "users/", f"запрос с методом - {request.method}", "405")
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def usersCreatedPosts(request, userID):
    # Вернуть список постов пользователя
    if request.method == "GET": response = user_created_post_list(request, userID)

    else: 
        response = message[405]
        LogException.write_data("Не существующий метод", "121", "viewsUsers", "Не верный метод", "usersCreatedPosts", "info", 
                                request, "users/<str:userID>/created-posts", f"запрос с методом - {request.method}", "405")
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def check_auth(request):
    # Проверка авторизации пользователя
    try:
        if request.method == "GET": response = {"isAuth": not isinstance(Authorization.is_authorization(request), dict)}

        else: 
            response = message[405]
            LogException.write_data("Не существующий метод", "135", "viewsUsers", "Не верный метод", "check_auth", "info", 
                                    request, "auth/check", f"запрос с методом - {request.method}", "405")
        
        return JsonResponse(response, status=response.get("status", 200))
        
    except Exception: return  JsonResponse({"isAuth": False}, status=200)
