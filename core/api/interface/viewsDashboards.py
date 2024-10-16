from django.views.decorators.csrf import csrf_exempt
from templates.answer import answer_dict as message
from apps.dashboards.controller import *
from django.http import JsonResponse


@csrf_exempt
def dashboards(request): 
    if request.method == "POST":                                        # Create board
        response = create_dashboards(request)

    else:
        response = message[405]
        
    return JsonResponse(response, status=response.get("status", 200))