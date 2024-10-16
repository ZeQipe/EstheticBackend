from templates.answer import answer_dict as message
from services.authService import Authorization
from apps.dashboards.models import Board
from django.http.multipartparser import MultiPartParser
import json


def create_dashboards(request):
    # Поиск автора доски
    cookie_user = Authorization.is_authorization(request)
    
    if isinstance(cookie_user, dict): return message[401]
    
    # Извлечение данных доски из формы
    request_data = json.loads(request.body)
    boardName = request_data.get("dashboardName", False)
    if not boardName: return message[400]

    result = Board.check_board_name(cookie_user, boardName)
    if result:
        response = message[400].copy()
        response['message'] = "It's dashboard name is busy."
        return response
    
    # Создание доски
    try: response = Board.create_board(cookie_user, boardName)
    except Exception: response = message[500]
    
    return response