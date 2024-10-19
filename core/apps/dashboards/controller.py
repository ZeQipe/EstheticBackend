from templates.answer import answer_dict as message
from services.authService import Authorization
from apps.dashboards.models import Board
from apps.posts.models import Post
from apps.users.models import User
from services.parserService import Separement
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


def get_boards_user_by_cookie(request):
    cookie_user = Authorization.is_authorization(request)
    
    if isinstance(cookie_user, dict):
        return message[401]
    
    offset, limit = Separement.pagination_parametrs(request)

    response = Separement.parse_dashboard_list(cookie_user, offset, limit)

    return response


def check_post_in_boards(request):
    cookie_user = Authorization.is_authorization(request)
    
    if isinstance(cookie_user, dict): return message[401]
    
    try: 
        post = Post.objects.get(id=request.GET.get("postid", "None"))

    except Exception: 
        return message[404]
    
    boards = post.boards.filter(author=cookie_user)

    return Separement.pars_dashboards_info_in(boards)


def remove_posts_in_board(request, boardID):
    cookie_user = Authorization.is_authorization(request)
    
    if isinstance(cookie_user, dict): return message[401]
    
    try:
        postID = json.loads(request.body).get("postsId")
        post = Post.objects.get(id=postID)
        
        board = Board.objects.get(id=boardID)
    except Exception as er:
        return message[404]
    
    if not board.posts.filter(id=post.id).exists(): return message[404]
    
    board.posts.remove(post)
    
    return message[200]


def get_user_dashboards(request, user_id):
    # Получаем query параметры offset и limit из запроса
    offset, limit = Separement.pagination_parametrs(request)
    
    # Поиск пользователя в базе данных
    try: user = User.objects.get(id=user_id)
    
    except Exception: return message[404]

    response = Separement.parse_dashboard_list(user, offset, limit, type="full")
        
    return response


def get_dashboard_detail(request, id_board):
    # Получаем query параметры offset и limit из запроса
    offset, limit = Separement.pagination_parametrs(request)

    # Поиск доски в базе данных
    try: boards = Board.objects.get(id=id_board).order_by('-created_at')
    except Exception: return message[404]
    
    response = Separement.parse_dashboard(boards, offset, limit)
    
    return response


def add_post_in_board(request, board_id):
    # Проверка авторизации пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]
    
    # Поиск доски в базе данных
    try: board = Board.objects.get(id=board_id, author=cookie_user)
    except Exception: return message[404]
    
    # Поиск поста в базе данных
    data = json.loads(request.body)
    try: post = Post.objects.get(id=data.get('postsId', ''))
    except Exception: return message[404]
    
    if post in board.posts.all():
        response = message[400].copy()
        response['message'] = f"This post has already been added"
        return response
    
    # Добавления поста в доску
    board.posts.add(post)
    return message[200]