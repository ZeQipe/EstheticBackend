from django.views.decorators.csrf import csrf_exempt
from templates.answer import answer_dict as message
from apps.dashboards.controller import *
from django.http import JsonResponse


@csrf_exempt
def dashboards(request): 
    if request.method == "POST":                                        # Create board
        response = create_dashboards(request)

    elif request.method == "GET":                                       # Get compact board list 
        response = get_boards_user_by_cookie(request)

    else:
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def post_in_boards(request):
    if request.method == "GET":                                         # Is post in Dashboards
        response = check_post_in_boards(request)

    else:
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def dashboards_delete_posts(request, boardID): 
    if request.method == "DELETE":                                      # Delete post in board
        response = remove_posts_in_board(request, boardID)
    
    else:
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def dashboards_list(request, userID): 
    if request.method == "GET":                                         # Get list information by boards
        response = get_user_dashboards(request, userID)
        
    else:
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))


@csrf_exempt
def dashboards_param(request, boardID): 
    if request.method == "GET":                                         # Get all information by board
        pass

    elif request.method == "POST":                                      # Add post in board by boardID
        pass
    
    elif request.method == "DELETE":                                    # Delete dashboard
        pass

    else:
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))
