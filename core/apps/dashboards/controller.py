from templates.answer import answer_dict as message
from services.authService import Authorization
from apps.dashboards.models import Board, BoardPost
from apps.posts.models import Post
from apps.users.models import User
from services.parserService import Separement
from services.logService import LogException
import json


def create_dashboards(request) -> dict:
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка создать доску без авторизации", "14", "dashboards -- controller", 
                    "Ошибка авторизации", "create_dashboards", "info", request, "dashboards/", "POST", "401")
        
        return message[401]
    
    # Извлечение данных из запроса
    request_data = json.loads(request.body)
    boardName = request_data.get("dashboardName", False)
    if not boardName: 
        LogException.write_data("Отсутсвует имя доски", "23", "dashboards -- controller", "Ошибка при обработке запроса", 
                                "create_dashboards", "info", request.body, "dashboards/", "POST", "400")
        
        return message[400]

    # Проверка на существование доски
    result = Board.check_board_name(cookie_user, boardName)
    if result:
        response = message[400].copy()
        response['message'] = "It's dashboard name is busy."
        LogException.write_data("Имя доски занято", "31", "dashboards -- controller", "Ошибка при обращении к модели", 
                                "create_dashboards", "info",  boardName, "dashboards/", "POST", "400")
        
        return response
    
    # Создание доски
    try: 
        response = Board.create_board(cookie_user, boardName)

    except Exception as er: 
        LogException.write_data(er, "40", "dashboards -- controller", "Ошибка при обращении к модели", 
                                "create_dashboards", "warning",  boardName, "dashboards/", "POST", "500")
        
        response = message[500]
    
    return response


def get_boards_user_by_cookie(request) -> dict:
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка получить доски по кукам без авторизации", "55", "dashboards -- controller", 
                    "Ошибка авторизации", "get_boards_user_by_cookie", "info", request, "dashboards/", "GET", "401")
        
        return message[401]
    
    # Получение параметров offset и limit для пагинации
    offset, limit = Separement.pagination_parametrs(request) 

    # Формирование ответа с помощью парсера
    try:
        response = Separement.parse_dashboard_list(cookie_user, offset, limit, BoardPost=BoardPost)

    except Exception as er:
        LogException.write_data(er, "65", "dashboards -- controller", "Ошибка при формировании ответа", 
                        "get_boards_user_by_cookie", "warning", request, "dashboards/", "GET", "500")
        
        response = message[500]

    return response


def check_post_in_boards(request) -> dict:
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка проверить наличие поста в доске без авторизации", "80", "dashboards -- controller", 
                    "Ошибка авторизации", "check_post_in_boards", "info", request, "dashboards/check-posts", "GET", "401")
        
        return message[401]

    # Поиск поста в базе данных
    try:  
        post = Post.objects.get(id=request.GET.get("postid", "None"))

    except Exception as er: 
        LogException.write_data(er, "87", "dashboards -- controller", "Ошибка при обращении к базе данных", 
            "check_post_in_boards", "info", request.GET.get("postid"), "dashboards/check-posts", "GET", "404")
        
        return message[404]
    
    # Получение всех досок пользователя
    boards = post.boards.filter(author=cookie_user)
    
    # Формирование ответа
    try:
        response = Separement.pars_dashboards_info_in(boards)

    except Exception as er:
        LogException.write_data(er, "100", "dashboards -- controller", "Ошибка при формировании ответа", 
                        "check_post_in_boards", "warning", boards, "dashboards/check-posts", "GET", "500")
        
        response = message[500]

    return response


def remove_posts_in_board(request, boardID: str) -> dict:
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка удалить пост из доски без авторизации ", "115", "dashboards -- controller", "Ошибка авторизации", 
                                "remove_posts_in_board", "info", request, "dashboards/<str:boardID>/delete-posts", "DELETE", "401")
        
        return message[401]
    
    # Извлечение данных из запроса
    try:
        postID = json.loads(request.body).get("postsId")

    except Exception as er:
        LogException.write_data(er, "122", "dashboards -- controller", "Ошибка при обработке запроса", "remove_posts_in_board", 
                                "info", f"request_body: {request.body}", "dashboards/<str:boardID>/delete-posts", "DELETE", "404")
        
        return message[404]
    
    # Поиск поста и доски в базе данных
    try:
        post = Post.objects.get(id=postID)
        board = Board.objects.get(id=boardID)

    except Exception as er: 
        LogException.write_data(er, "132", "dashboards -- controller", "Ошибка при обращении к базе данных", "remove_posts_in_board", 
                                "info", f"postId: {postID} -- boardID: {boardID}", "dashboards/<str:boardID>/delete-posts", "DELETE", "404")
        
        return message[404]
    
    # Проверка наличия поста в доске
    if not board.posts.filter(id=post.id).exists(): 
        LogException.write_data("Отсутсвует пост в доске", "143", "dashboards -- controller", "Ошибка доступа", 
                                "remove_posts_in_board", "info", f"postId: {postID} -- boardID: {boardID}", 
                                "dashboards/<str:boardID>/delete-posts", "DELETE", "404")
        
        return message[404]
    
    # Удаления поста из доски
    try:
        board.posts.remove(post)
        BoardPost.objects.filter(board=board, post=post).delete()
    
    except Exception as er:
        LogException.write_data("Отсутсвует пост в доске", "151", "dashboards -- controller", "Ошибка при обращении к базе данных", 
                                "remove_posts_in_board", "info", f"postId: {postID} -- boardID: {boardID}", 
                                "dashboards/<str:boardID>/delete-posts", "DELETE", "404")
        
    return message[200]


def get_user_dashboards(request, user_id: str) -> dict:
    # Получаем query параметры offset и limit из запроса
    offset, limit = Separement.pagination_parametrs(request)

    # Поиск пользователя в базе данных
    try: 
        user = User.objects.get(id=user_id)

    except Exception as er: 
        LogException.write_data(er, "168", "dashboards -- controller", "Ошибка при обращении к базе данных", 
                                "get_user_dashboards", "warning", f"user_id: {user_id}", 
                                "dashboards/<str:userID>/list", "GET", "404")
        
        return message[404]

    # Формирование ответа с помощью парсера
    try:
        response = Separement.parse_dashboard_list(user, offset, limit, BoardPost=BoardPost, type="full")
    
    except Exception as er:
        LogException.write_data(er, "179", "dashboards -- controller", "Ошибка при формировании ответа", 
            "get_user_dashboards", "warning", f"user_id: {user_id}", "dashboards/<str:userID>/list", "GET", "500")
        
        response = message[500]
    
    return response


def get_dashboard_detail(request, id_board: str) -> dict:
    # Поиск доски в базе данных
    try: 
        boards = Board.objects.get(id=id_board)

    except Exception as er: 
        LogException.write_data(er, "193", "dashboards -- controller", "Ошибка при обращении к базе данных", 
            "get_dashboard_detail", "warning", f"id_board: {id_board}", "dashboards/<str:boardID>", "GET", "404")
        
        return message[404]

    # Формирование ответа с помощью парсера
    try:
        response = Separement.parse_dashboard(boards, BoardPost)

    except Exception as er:
        LogException.write_data(er, "203", "dashboards -- controller", "Ошибка при формировании ответа", 
            "get_dashboard_detail", "warning", f"id_board: {id_board}", "dashboards/<str:boardID>", "GET", "500")
        
        response = message[500]

    return response


def add_post_in_board(request, board_id: str) -> dict:
    # Проверка авторизации пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка добавить пост в доску без авторизации", "218", "dashboards -- controller", "Ошибка авторизации", 
                        "add_post_in_board", "info", f"cookie_user: {type(cookie_user)}", "dashboards/<str:boardID>", "POST", "401")
        
        return message[401]

    # Извлечение данных из запроса
    try:
        postID = json.loads(request.body).get("postsId")

    except Exception as er:
        LogException.write_data(er, "225", "dashboards -- controller", "Ошибка при обработке запроса", 
                                "add_post_in_board", "info", f"board_id: {board_id} -- postID: {postID}", 
                                "dashboards/<str:boardID>", "POST", "404")
        
        return message[404]
    
    # Поиск поста и доски в базе данных
    try:
        post = Post.objects.get(id=postID)
        board = Board.objects.get(id=board_id, author=cookie_user)

    except Exception as er: 
        LogException.write_data(er, "236", "dashboards -- controller", "Ошибка при обращении к базе данных", 
                                "add_post_in_board", "info", f"board_id: {board_id} -- postID: {postID}", 
                                "dashboards/<str:boardID>", "POST", "404")
        
        return message[404]
    
    # Проверка наличия поста в доске
    if post in board.posts.all():
        response = message[400].copy()
        response['message'] = f"This post has already been added"
        LogException.write_data(er, "248", "dashboards -- controller", "Ошибка доступа", "add_post_in_board", 
                "info", f"board_id: {board_id} -- postID: {postID}", "dashboards/<str:boardID>", "POST", "400")

        return response
    
    try:
        # Добавления поста в доску
        board.posts.add(post)

        # Добавление записи в BoardPost
        BoardPost.objects.create(board=board, post=post)

    except Exception as er:
        LogException.write_data(er, "256", "dashboards -- controller", "Ошибка при обращении к базе данных", "add_post_in_board", 
                                "info", f"board_id: {board_id} -- postID: {postID}", "dashboards/<str:boardID>", "POST", "500")
        
        return message[500]
    
    return message[200]


def put_dashboards_name(request, board_id: str):
    # Проверка авторизации пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка изменить доску без авторизации", "218", "dashboards -- controller", "Ошибка авторизации", 
                        "add_post_in_board", "info", f"cookie_user: {type(cookie_user)}", "dashboards/<str:boardID>", "POST", "401")

    # Поиск поста и доски в базе данных
    try:
        board = Board.objects.get(id=board_id, author=cookie_user)

    except Exception as er: 
        LogException.write_data(er, "236", "dashboards -- controller", "Ошибка при обращении к базе данных", 
                                "add_post_in_board", "info", f"board_id: {board_id}", 
                                "dashboards/<str:boardID>", "POST", "404")
        
        return message[404]

    # Извлечение данных из запроса
    request_data = json.loads(request.body)
    boardName = request_data.get("dashboardName", False)
    if not boardName: 
        LogException.write_data("Отсутсвует имя доски", "282", "dashboards -- controller", "Ошибка при обработке запроса", 
                                "create_dashboards", "info", request.body, "dashboards/", "POST", "400")
        
        return message[400]
    
    mess = board.edit_name(boardName)

    if mess:
        message_response = message[200]
        message_response["userId"] = cookie_user.id
        message_response["dashboardId"] = board.id

        return message_response
    
    else:
        return message[400]

    