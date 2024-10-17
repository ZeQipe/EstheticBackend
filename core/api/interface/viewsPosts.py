from templates.answer import answer_dict as message
from django.http import JsonResponse
from apps.posts.controller import *
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def posts(request): 
    if request.method == "POST":                                         # Create post
        response = create_post(request)

    else:
        response = message[405]
    
    return JsonResponse(response, status=response.get("status", 200))