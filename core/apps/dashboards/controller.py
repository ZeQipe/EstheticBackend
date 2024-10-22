from templates.answer import answer_dict as message
from services.authService import Authorization
from apps.dashboards.models import Board
from apps.posts.models import Post
from apps.users.models import User
from services.parserService import Separement
import json


def create_dashboards(request):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]
    
    # Извлечение данных доски из формы
    request_data = json.loads(request.body)
    boardName = request_data.get("dashboardName", False)
    if not boardName: return message[400]

    # Проверка на существование такой доски
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
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]
    
    # Получение параметров offset и limit для пагинации
    offset, limit = Separement.pagination_parametrs(request)

    # Формирование ответа с помощью парсера
    response = Separement.parse_dashboard_list(cookie_user, offset, limit)
    return response


def check_post_in_boards(request):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]

    # Поиск поста в базе данных
    try: post = Post.objects.get(id=request.GET.get("postid", "None"))
    except Exception: return message[404]
    
    # Получение всех досок пользователя
    boards = post.boards.filter(author=cookie_user)
    return Separement.pars_dashboards_info_in(boards)


def remove_posts_in_board(request, boardID):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]
    
    # Поиск поста и доски в базе данных
    try:
        postID = json.loads(request.body).get("postsId")
        post = Post.objects.get(id=postID)
        
        board = Board.objects.get(id=boardID)

    except Exception: return message[404]
    
    # Проверка наличия поста в доске
    if not board.posts.filter(id=post.id).exists(): return message[404]
    
    # Удаления поста из доски
    board.posts.remove(post)
    return message[200]


def get_user_dashboards(request, user_id):
    # Получаем query параметры offset и limit из запроса
    offset, limit = Separement.pagination_parametrs(request)
    
    # Поиск пользователя в базе данных
    try: user = User.objects.get(id=user_id)
    except Exception: return message[404]

    # Формирование ответа с помощью парсера
    response = Separement.parse_dashboard_list(user, offset, limit, type="full")
    return response


def get_dashboard_detail(request, id_board):
    # Поиск доски в базе данных
    try: boards = Board.objects.get(id=id_board)
    except Exception: return message[404]

    # Формирование ответа с помощью парсера
    response = Separement.parse_dashboard(boards)
    return response


def add_post_in_board(request, board_id):
    # Проверка авторизации пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]

    # Поиск поста и доски в базе данных
    try:
        postID = json.loads(request.body).get("postsId")
        post = Post.objects.get(id=postID)
        
        board = Board.objects.get(id=board_id, author=cookie_user)

    except Exception: return message[404]
    
    # Проверка наличия поста в доске
    if post in board.posts.all():
        response = message[400].copy()
        response['message'] = f"This post has already been added"
        return response
    
    # Добавления поста в доску
    board.posts.add(post)
    return message[200]