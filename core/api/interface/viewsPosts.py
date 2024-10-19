from templates.answer import answer_dict as message
from django.http import JsonResponse
from apps.posts.controller import *
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def posts(request): 
    if request.method == "POST":                                         # Create post
        response = create_post(request)
    
    elif request.method == "GET":                                         # Get all posts
        response = search_posts(request)

    else:
        response = message[405]
    
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def postsToggleLike(request, postID): 
    if request.method == "PUT":                                         # set like post
        pass
    
    else:
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))