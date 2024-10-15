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
    if request.method == "POST":                                        # Create user profile
        response = registration_users(request)
    
    else:
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
@require_http_methods(["POST"])
def usersLogin(request):
    if request.method == "POST":                                        # LogIn user
        response = Authorization.login(request)

        if response.get("userId", False):
            cook_keys = Encriptions.encrypt_string(response.get("userId"))
            response = JsonResponse(response, status=200)
            response = Authorization.set_key_in_coockies(response, cook_keys)

        else:
            response = JsonResponse(response, status=response.get("status"))

    else:
        response = JsonResponse(message[405], status=405)

    return response


@csrf_exempt
@require_http_methods(["POST"])
def usersLogout(request):
    if request.method == "POST":                                        # LogOut user
        user = Authorization.is_authorization(request)
        if isinstance(user, dict):
            response = JsonResponse(message[401], status=401)
        else:
            response = JsonResponse(message[200], status=200)
            response.delete_cookie("auth_key")
        
    else:
        response = JsonResponse(message[405], status=405)

    return response


@csrf_exempt
def privateProfile(request):
    if request.method == "GET":                                         # Get Private profile by cookie
        response = user_profile(request) 
        
    else:
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def publicProfile(request, userID):
    if request.method == "GET":                                         # Get Public profile by userID
        response = user_profile(request, userID)

    else:
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def users(request):
    if request.method == "DELETE":                                      # Delete object
        response = deletter.del_object(request, User)

    elif request.method == "PUT":
        response = edit_user_data(request)                           # Edit User Profile
    
    else:
        response = message[405]

    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def usersCreatedPosts(request, userID):
    if request.method == "GET":                                         # Get created users posts
        response = user_created_post_list(request, userID)

    else:
        response = message[405]

    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def check_auth(request): 
    if request.method == "GET":                                         # Check authorization from user
        if isinstance(Authorization.is_authorization(request), dict):
            mess = {"isAuth": False}
            response = JsonResponse(mess, status=401)
        else:
            mess = {"isAuth": True}
            response = JsonResponse(mess, status=200)
    else:
        response = JsonResponse(mess[405], status=405)
        
    return response