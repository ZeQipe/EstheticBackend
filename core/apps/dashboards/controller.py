from templates.answer import answer_dict as message
from services.authService import Authorization
from apps.dashboards.models import Board, BoardPost
from apps.posts.models import Post
from apps.users.models import User
from services.parserService import Separement
from services.logService import LogException
import json


def create_dashboards(request):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка создать доску без авторизации", "14", "controller -- dashboards", "Не авторизованный пользователь", 
                                "create_dashboards", "info", request, "dashboards/", "POST", "401")
        return message[401]
    
    # Извлечение данных доски из формы
    request_data = json.loads(request.body)
    boardName = request_data.get("dashboardName", False)
    if not boardName: 
        LogException.write_data("Отсутсвует имя доски", "22", "controller -- dashboards", "Не Найдено имя доски в зпросе", 
                                "create_dashboards", "info", request.body, "dashboards/", "POST", "400")
        
        return message[400]

    # Проверка на существование такой доски
    result = Board.check_board_name(cookie_user, boardName)
    if result:
        response = message[400].copy()
        response['message'] = "It's dashboard name is busy."
        LogException.write_data("Имя доски занято", "30", "controller -- dashboards", "Имя доски занято", 
                                "create_dashboards", "info",  boardName, "dashboards/", "POST", "400")
        
        return response
    
    # Создание доски
    try: response = Board.create_board(cookie_user, boardName)
    except Exception as er: 
        LogException.write_data(er, "39", "controller -- dashboards", "Ошибка при создании доски", 
                                "create_dashboards", "warning",  boardName, "dashboards/", "POST", "500")
        
        response = message[500]
    
    return response


def get_boards_user_by_cookie(request):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка получить доски по кукам без авторизации", "52", "controller -- dashboards", "Не авторизованный пользователь", 
                                "get_boards_user_by_cookie", "info", request, "dashboards/", "GET", "401")
        
        return message[401]
    
    # Получение параметров offset и limit для пагинации
    offset, limit = Separement.pagination_parametrs(request) 

    # Формирование ответа с помощью парсера
    try:
        response = Separement.parse_dashboard_list(cookie_user, offset, limit, BoardPost=BoardPost)
    except Exception as er:
        LogException.write_data(er, "62", "controller -- dashboards", "Ошибка при формировании ответа", 
                        "get_boards_user_by_cookie", "warning", request, "dashboards/", "GET", "500")
        
        response = message[500]

    return response


def check_post_in_boards(request):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка проверить наличие поста в доске без авторизации", "76", "controller -- dashboards", 
                                "Не авторизованный пользователь", "check_post_in_boards", "info", request, "dashboards/check-posts", "GET", "401")
        
        return message[401]

    # Поиск поста в базе данных
    try: post = Post.objects.get(id=request.GET.get("postid", "None"))
    except Exception as er: 
        LogException.write_data(er, "83", "controller -- dashboards", "Ошибка при поиске поста в базе данных ", "check_post_in_boards", 
                                "info", request.GET.get("postid"), "dashboards/check-posts", "GET", "404")
        
        return message[404]
    
    # Получение всех досок пользователя
    boards = post.boards.filter(author=cookie_user)
    
    try:
        response = Separement.pars_dashboards_info_in(boards)

    except Exception as er:
        LogException.write_data(er, "93", "controller -- dashboards", "Ошибка при формировании ответа", "check_post_in_boards", 
                                "warning", boards, "dashboards/check-posts", "GET", "500")
        
        response = message[500]


    return response


def remove_posts_in_board(request, boardID):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка удалить пост из доски без авторизации ", "109", "controller -- dashboards", "Отсутсвует авторизация", 
                                "remove_posts_in_board", "info", request, "dashboards/<str:boardID>/delete-posts", "DELETE", "401")
        
        return message[401]
    
    # Поиск поста и доски в базе данных
    try:
        postID = json.loads(request.body).get("postsId")
        post = Post.objects.get(id=postID)
        
        board = Board.objects.get(id=boardID)

    except Exception as er: 
        LogException.write_data(er, "116", "controller -- dashboards", "Ошибка при поиске поста и доски в базе данных", "remove_posts_in_board", 
                                "info", f"postId: {postID} -- boardID: {boardID}", "dashboards/<str:boardID>/delete-posts", "DELETE", "404")
        
        return message[404]
    
    # Проверка наличия поста в доске
    if not board.posts.filter(id=post.id).exists(): 
        LogException.write_data("Отсутсвует пост в доске", "129", "controller -- dashboards", "Ошибка при поиске поста в доске ", 
                                "remove_posts_in_board", "info", f"postId: {postID} -- boardID: {boardID}", 
                                "dashboards/<str:boardID>/delete-posts", "DELETE", "404")
        
        return message[404]
    
    # Удаления поста из доски
    board.posts.remove(post)
    BoardPost.objects.filter(board=board, post=post).delete()
    return message[200]


def get_user_dashboards(request, user_id):
    # Получаем query параметры offset и limit из запроса
    offset, limit = Separement.pagination_parametrs(request)

    # Поиск пользователя в базе данных
    try: user = User.objects.get(id=user_id)

    except Exception as er: 
        LogException.write_data(er, "148", "controller -- dashboards", "Ошибка при поиске пользователя в базе данных", 
                                "get_user_dashboards", "warning", f"user_id: {user_id}", 
                                "dashboards/<str:userID>/list", "GET", "404")
        
        
        return message[404]

    # Формирование ответа с помощью парсера
    try:
        response = Separement.parse_dashboard_list(user, offset, limit, BoardPost=BoardPost, type="full")
    
    except Exception as er:
        LogException.write_data(er, "158", "controller -- dashboards", "Ошибка при формировании ответа", "get_user_dashboards", 
                                "warning", f"user_id: {user_id}", "dashboards/<str:userID>/list", "GET", "500")
        response = message[500]
    
    return response


def get_dashboard_detail(request, id_board):
    # Поиск доски в базе данных
    try: boards = Board.objects.get(id=id_board)
    except Exception as er: 
        LogException.write_data(er, "171", "controller -- dashboards", "Ошибка при поиске доски в базе данных", 
                                "get_dashboard_detail", "warning", f"id_board: {id_board}", 
                                "dashboards/<str:boardID>", "GET", "404")
        
        return message[404]

    # Формирование ответа с помощью парсера
    try:
        response = Separement.parse_dashboard(boards, BoardPost)

    except Exception as er:
        LogException.write_data(er, "180", "controller -- dashboards", "Ошибка при формировании ответа", 
                        "get_dashboard_detail", "warning", f"id_board: {id_board}", 
                        "dashboards/<str:boardID>", "GET", "500")
        
        response = message[500]

    return response


def add_post_in_board(request, board_id):
    # Проверка авторизации пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка добавить пост в доску без авторизации", "196", "controller -- dashboards", "Отсутсвует авторизация", 
                        "add_post_in_board", "info", f"cookie_user: {type(cookie_user)}", "dashboards/<str:boardID>", "POST", "401")
        
        return message[401]

    # Поиск поста и доски в базе данных
    try:
        postID = json.loads(request.body).get("postsId")
        post = Post.objects.get(id=postID)
        
        board = Board.objects.get(id=board_id, author=cookie_user)

    except Exception as er: 
        LogException.write_data(er, "203", "controller -- dashboards", "Ошибка при поиске доски или поста в базе данных", 
                                "add_post_in_board", "info", f"board_id: {board_id} -- postID: {postID}", 
                                "dashboards/<str:boardID>", "POST", "404")
        
        return message[404]
    
    # Проверка наличия поста в доске
    if post in board.posts.all():
        response = message[400].copy()
        response['message'] = f"This post has already been added"
        LogException.write_data(er, "217", "controller -- dashboards", "Пост в доске уже есть", "add_post_in_board", "info", 
                                f"board_id: {board_id} -- postID: {postID}", "dashboards/<str:boardID>", "POST", "400")


        return response
    
    # Добавления поста в доску
    board.posts.add(post)

    # Добавление записи в BoardPost
    BoardPost.objects.create(board=board, post=post)
    
    return message[200]