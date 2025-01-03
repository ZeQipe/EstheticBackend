from templates.answer import answer_dict as message
from services.authService import Authorization
from apps.comments.models import Comments
from apps.posts.models import Post
from services.encriptionService import Encriptions
from services.parserService import Separement
from services.logService import LogException
import json


def create_comments(request, postId):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка создать комментарий без авторизации", "14", "Controller -- comments", "Ошибка авторизации", "create_comments", 
                                "info", request, "comments/<str:ID>", "POST", "401")
        
        return message[401]

    try: post = Post.objects.get(id=postId)
    except Exception as er: 
        LogException.write_data(er, "20", "Controller -- comments", "Ошибка при поиске поста в базе данных", "create_comments", "warning", 
                                f"postId: {postId}", "comments/<str:ID>", "POST", "404")
        
        return message[404]

    # Формируем информацию о посте
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as er:
        LogException.write_data(er, "28", "Controller -- comments", "Ошибка при чтении данных из запроса", "create_comments", "warning", 
                                f"body: {request.body}", "comments/<str:ID>", "POST", "400")
        return message[400]
    
    answerId = data.get("answerCommentId")
    
    if answerId:
        try: answer = Comments.objects.get(id=answerId)

        except Exception as er: 
            response = message[404]
            response["error"] = "Комментарий, на который Вы пытались ответить, не найден."
            LogException.write_data(er, "38", "Controller -- comments", "Ошибка при поиске комментария", "create_comments", "warning", 
                                f"answerId: {answerId}", "comments/<str:ID>", "POST", "404")
            
            return response
        
        answerComment = {"id" : answer.id,
                         "firstName": answer.author.first_name,
                         "lastName": answer.author.last_name,
                         "userId" : answer.author.id}
        
    else: answerComment = {}

    comments_data = {"id" : Encriptions.generate_string(50, Comments),
                   "text" : data.get("text"),
                 "author" : cookie_user,
                 "answer" : answerComment,
                   "post" : post}
    
    try:
        result = Comments.create(comments_data)

    except Exception as er:
        LogException.write_data(er, "61", "Controller -- comments", "Ошибка при создании комментария", "create_comments", "warning", 
                                f"comments_data: {comments_data}", "comments/<str:ID>", "POST", "500")
        result = message[500]
    
    return result



def get_comments(request, postId):
    # Получаем query параметры offset и limit из запроса
    offset, limit = Separement.pagination_parametrs(request)

    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)

    try: post = Post.objects.get(id=postId)
    except Exception as er: 
        LogException.write_data(er, "80", "Controller -- comments", "Ошибка при поиске поста в базе данных", "get_comments", "warning", 
                                f"postId: {postId}", "comments/<str:ID>", "GET", "404")
        
        return message[404]

    comments = Comments.objects.filter(post=post).order_by('-created_at')

    if comments.count() == 0:
        return {"commentsAmount" : 0,
                 "commentsList" : []}
    else:
        try:
            response = Separement.formatted_comments(comments, cookie_user, offset, limit)
        
        except Exception as er:
            LogException.write_data(er, "93", "Controller -- comments", "Ошибка при формировании ответа", "get_comments", "warning", 
                                f"comments: {comments}", "comments/<str:ID>",  "GET", "500")
            
            return message[500]
        
        return response


def edit_comments(request, commentId):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка отредактировать пост без авторизации", "108", "Controller -- comments", "Ошибка авторизации", 
                                "edit_comments", "info", request, "comments/<str:ID>", "PUT", "401")
        
        return message[401]

    # Проверка на существования комментария
    try: comment = Comments.objects.get(id=commentId)
    except Exception as er: 
        LogException.write_data(er, "115", "Controller -- comments", "Ошибка при поиске комментария", "edit_comments", "warning", 
                                f"commentId: {commentId}", "comments/<str:ID>", "PUT", "404")
        
        return message[404]

    # Проверка что комментарий принадлежит пользователю
    if comment.author.id != cookie_user.id:
        LogException.write_data("Попытка изменить не свой пост", "123", "Controller -- comments", "Пост не принадлежит авторизованному пользователю", 
                                "toggle_like", "info", f"author_post: {comment.author.id} -- cookie_user: {cookie_user.id}", "comments/<str:ID>", 
                                "PUT", "403")
        
        return message[403]
    
    # Формируем информацию о посте
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as er:
        LogException.write_data(er, "131", "Controller -- comments", "Ошибка при получении данных из запроса", "edit_comments", "warning", 
                                f"request_body: {request.body}", "comments/<str:ID>", f"PUT", "400")
        
        return message[400]
    
    comment_text = data.get("text")

    try: 
        result = comment.edit(comment_text)
        return  {"postId" : result.post.id}
    
    except Exception as er: 
        LogException.write_data(er, "141", "Controller -- comments", "Ошибка при редактировании комментария", "edit_comments", "warning", 
                                f"comment_text: {comment_text}", "comments/<str:ID>", "PUT", "500")
        
        return message[500]




def change_like(request, commentsId):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка лайкнуть без авторизации", "157", "Controller -- comments", "Ошибка авторизации", "change_like", "info", 
                                request, "comments/toggle-like/<str:commentID>", "PUT", "401")
        
        return message[401]

    # Поиск поста в базе данных
    try: comment = Comments.objects.get(id=commentsId)
    except Exception as er: 
        LogException.write_data(er, "164", "Controller -- comments", "Ошибка поиска поста в базе данных", "change_like", "warning", 
                                f"commentsId: {commentsId}", "comments/toggle-like/<str:commentID>", "PUT", "404")
        
        return message[404]

    # Установка или удаление лайка
    if comment.users_liked.filter(id=cookie_user.id).exists():
        comment.users_liked.remove(cookie_user)
    else:
        comment.users_liked.add(cookie_user)

    return message[200]