from templates.answer import answer_dict as message
from django.http import JsonResponse
from apps.posts.controller import *
from django.views.decorators.csrf import csrf_exempt
from services.delService import DeletterObject


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
def posts_toggle_like(request, postID): 
    if request.method == "PUT":                                         # set like post
        response = toggle_like(request, postID)
    
    else:
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def posts_param(request, postID): 
    if request.method == "GET":                                         # Get post by postID
        response = get_post_by_id(request, postID)

    elif request.method == "DELETE":                                    # Delete post
        response = DeletterObject.del_object(request, Post, postID)

    elif request.method == "PUT":                                       # Changing post information by postID
        response = edit_post_by_id(request, postID)
    
    else:
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))