from templates.answer import answer_dict as message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def posts(request): 
    if request.method == "GET":                                         # Get all posts
        pass

    else:
        response = message[405]
    
    return JsonResponse(response, status=response.get("status", 200))