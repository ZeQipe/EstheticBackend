from templates.answer import answer_dict as message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from apps.users.controller import *


@csrf_exempt
@require_http_methods(["POST"])
def usersRegistration(request): 
    if request.method == "POST":                                        # Create user profile
        response = registration_users(request)
    
    else:
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))