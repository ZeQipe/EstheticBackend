from templates.answer import answer_dict as message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from apps.users.controller import *
from services.authService import Authorization


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